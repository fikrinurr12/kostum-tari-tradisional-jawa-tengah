"""
utils/model_loader.py
Modul untuk memuat model klasifikasi dan menjalankan prediksi.

Catatan penting kompatibilitas deployment:
- Model dimuat dengan compile=False karena untuk inferensi saja kita
  tidak butuh optimizer/loss/metrics ter-reattach. Ini juga menghindari
  error langka terkait custom metric objects (mis. keras.metrics.Precision
  dengan nama custom) yang kadang gagal di-deserialize otomatis saat
  versi TensorFlow runtime sedikit berbeda dari versi training.
- st.cache_resource memastikan model hanya dimuat sekali per sesi server,
  bukan setiap kali pengguna upload gambar (penting untuk kecepatan &
  memori di Streamlit Cloud free tier).
"""

import json
import os

import numpy as np
import streamlit as st
from PIL import Image

import config


@st.cache_resource(show_spinner=False)
def load_class_mapping():
    """
    Memuat mapping kelas dari class_mapping.json yang dihasilkan notebook
    training. Mengembalikan dict dengan key: idx_to_class, class_names,
    class_labels, img_size.
    """
    if not os.path.exists(config.CLASS_MAPPING_PATH):
        return None

    with open(config.CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    # idx_to_class disimpan dengan key string angka ("0", "1", ...) karena
    # JSON tidak mendukung integer sebagai key — konversi balik ke int.
    idx_to_class_raw = mapping.get("idx_to_class", {})
    idx_to_class = {int(k): v for k, v in idx_to_class_raw.items()}

    return {
        "idx_to_class": idx_to_class,
        "class_names": mapping.get("class_names", config.CLASS_ORDER),
        "class_labels": mapping.get("class_labels", {}),
        "img_size": tuple(mapping.get("img_size", list(config.IMG_SIZE))),
    }


@st.cache_resource(show_spinner=False)
def load_model():
    """
    Memuat model Keras untuk inferensi.
    Mencoba .h5 dahulu (lebih portable antar versi TF minor), lalu
    fallback ke .keras jika .h5 tidak ditemukan.

    Mengembalikan tuple (model, error_message). Jika error_message bukan
    None, model bernilai None dan pesan error siap ditampilkan ke user.
    """
    # Import TensorFlow di dalam fungsi (bukan di top-level module) agar
    # error import tidak langsung meledak saat module di-import — bisa
    # ditangani dengan pesan yang ramah di UI.
    try:
        import tensorflow as tf
    except ImportError as e:
        return None, (
            "TensorFlow gagal diimpor. Pastikan `tensorflow-cpu` "
            f"tercantum di requirements.txt. Detail: {e}"
        )

    model_path = None
    if os.path.exists(config.MODEL_PATH):
        model_path = config.MODEL_PATH
    elif os.path.exists(config.MODEL_PATH_KERAS):
        model_path = config.MODEL_PATH_KERAS

    if model_path is None:
        return None, (
            "File model tidak ditemukan di folder `models/`. "
            "Pastikan `model_final.h5` (atau `model_final.keras`) sudah "
            "diunggah ke folder models/ pada repository."
        )

    try:
        model = tf.keras.models.load_model(model_path, compile=False)
        return model, None
    except Exception as e:
        return None, (
            f"Gagal memuat model dari `{os.path.basename(model_path)}`. "
            f"Detail teknis: {e}"
        )


def preprocess_image(image: Image.Image, target_size):
    """
    Mengubah gambar PIL menjadi array siap pakai untuk MobileNetV2.
    Preprocessing harus identik dengan preprocess_input MobileNetV2
    yang dipakai saat training (skala piksel ke rentang [-1, 1]).
    """
    image = image.convert("RGB").resize(target_size)
    arr = np.array(image).astype(np.float32)

    # Setara tf.keras.applications.mobilenet_v2.preprocess_input
    # (scaling manual ditulis langsung agar tidak perlu import berat
    # 'applications' module hanya untuk satu fungsi ini).
    arr = (arr / 127.5) - 1.0

    return np.expand_dims(arr, axis=0)


def predict(model, mapping, image: Image.Image):
    """
    Menjalankan prediksi pada satu gambar.

    Mengembalikan dict:
      {
        'pred_class_key'   : 'Tari_Bedhaya',   # key internal (folder/JSON)
        'pred_label'       : 'Tari Bedhaya',   # label tampilan
        'confidence'       : 92.4,             # persen
        'all_probabilities': {key: persen, ...}  # semua kelas, terurut desc
        'margin'           : 78.1,             # selisih top-1 vs top-2 (persen)
        'likely_out_of_scope': False,          # True jika kemungkinan bukan
                                                # salah satu dari 5 kelas yang
                                                # dilatih (lihat config.py)
      }
    """
    img_size = mapping["img_size"]
    arr = preprocess_image(image, img_size)

    probs = model.predict(arr, verbose=0)[0]
    pred_idx = int(np.argmax(probs))

    idx_to_class = mapping["idx_to_class"]
    class_labels = mapping["class_labels"]

    pred_class_key = idx_to_class.get(pred_idx, config.CLASS_ORDER[pred_idx])
    pred_label = class_labels.get(pred_class_key, pred_class_key.replace("_", " "))
    confidence = float(probs[pred_idx]) * 100

    all_probs = {}
    for idx, prob in enumerate(probs):
        class_key = idx_to_class.get(idx, config.CLASS_ORDER[idx] if idx < len(config.CLASS_ORDER) else str(idx))
        all_probs[class_key] = float(prob) * 100

    # Urutkan dari probabilitas tertinggi
    all_probs = dict(sorted(all_probs.items(), key=lambda x: x[1], reverse=True))

    # ── Sinyal deteksi "kemungkinan di luar 5 kelas yang dilatih" ──
    # Model softmax SELALU mengeluarkan total probabilitas 100% dibagi
    # ke 5 kelas, walau gambarnya sama sekali bukan kostum tari (misal
    # foto kucing) -- jadi tidak ada cara langsung model bilang "tidak
    # tahu". Dua sinyal tidak langsung dipakai sebagai pendekatan:
    sorted_probs = list(all_probs.values())
    top1 = sorted_probs[0]
    top2 = sorted_probs[1] if len(sorted_probs) > 1 else 0.0
    margin = top1 - top2

    likely_out_of_scope = (
        top1 < config.OOD_CONFIDENCE_THRESHOLD
        or margin < config.OOD_MARGIN_THRESHOLD
    )

    return {
        "pred_class_key": pred_class_key,
        "pred_label": pred_label,
        "confidence": confidence,
        "all_probabilities": all_probs,
        "margin": margin,
        "likely_out_of_scope": likely_out_of_scope,
    }
