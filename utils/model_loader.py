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
def load_face_detector():
    """
    Memuat Haar Cascade classifier untuk deteksi wajah (bawaan OpenCV,
    tidak perlu file model tambahan -- sudah ter-bundle di paket
    opencv-python-headless itu sendiri).

    Mengembalikan tuple (detector, error_message).
    """
    try:
        import cv2
    except ImportError as e:
        return None, (
            "OpenCV gagal diimpor. Pastikan `opencv-python-headless` "
            f"tercantum di requirements.txt. Detail: {e}"
        )

    cascade_path = os.path.join(
        cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
    )
    detector = cv2.CascadeClassifier(cascade_path)

    if detector.empty():
        return None, "Gagal memuat file Haar Cascade untuk deteksi wajah."

    return detector, None


def detect_dominant_face(image: Image.Image, detector, area_threshold=None):
    """
    Mendeteksi apakah ada wajah yang DOMINAN (cukup besar relatif
    terhadap ukuran gambar) di dalam foto -- indikasi kuat ini adalah
    foto selfie/wajah, bukan foto kostum tari.

    area_threshold: proporsi minimum (luas wajah / luas gambar) untuk
    dianggap "dominan". Default diambil dari config.FACE_AREA_THRESHOLD
    jika tidak diberikan secara eksplisit.

    Mengembalikan dict: {'face_detected': bool, 'dominant_face': bool,
                          'largest_face_ratio': float}
    """
    import cv2

    if area_threshold is None:
        area_threshold = config.FACE_AREA_THRESHOLD

    img_array = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    faces = detector.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )

    if len(faces) == 0:
        return {"face_detected": False, "dominant_face": False, "largest_face_ratio": 0.0}

    image_area = gray.shape[0] * gray.shape[1]
    largest_face_area = max(w * h for (x, y, w, h) in faces)
    largest_face_ratio = largest_face_area / image_area

    return {
        "face_detected": True,
        "dominant_face": largest_face_ratio >= area_threshold,
        "largest_face_ratio": largest_face_ratio,
    }


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


def predict(model, mapping, image: Image.Image, face_detector=None):
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
        'reason'           : None / 'dominant_face' / 'low_confidence',
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

    # ── Sinyal 1: deteksi wajah dominan (foto selfie/wajah) ───────
    # Dijalankan & dicek LEBIH DULU karena ini sinyal yang independen
    # dari confidence model -- model softmax tetap bisa sangat "yakin"
    # (>90%) terhadap foto wajah yang sebenarnya sama sekali bukan
    # kostum tari, karena ia hanya dilatih membedakan 5 kelas tari satu
    # sama lain, bukan membedakan "tari" vs "bukan tari" secara umum.
    face_info = {"face_detected": False, "dominant_face": False, "largest_face_ratio": 0.0}
    if face_detector is not None:
        try:
            face_info = detect_dominant_face(image, face_detector)
        except Exception:
            # Jika deteksi wajah gagal karena alasan apapun (gambar
            # korup, dll), JANGAN blokir prediksi utama -- lanjut
            # dengan sinyal confidence/margin saja sebagai fallback.
            pass

    # ── Sinyal 2: confidence & margin (pendekatan sebelumnya) ─────
    sorted_probs = list(all_probs.values())
    top1 = sorted_probs[0]
    top2 = sorted_probs[1] if len(sorted_probs) > 1 else 0.0
    margin = top1 - top2

    low_confidence = (
        top1 < config.OOD_CONFIDENCE_THRESHOLD
        or margin < config.OOD_MARGIN_THRESHOLD
    )

    if face_info["dominant_face"]:
        likely_out_of_scope = True
        reason = "dominant_face"
    elif low_confidence:
        likely_out_of_scope = True
        reason = "low_confidence"
    else:
        likely_out_of_scope = False
        reason = None

    return {
        "pred_class_key": pred_class_key,
        "pred_label": pred_label,
        "confidence": confidence,
        "all_probabilities": all_probs,
        "margin": margin,
        "likely_out_of_scope": likely_out_of_scope,
        "reason": reason,
        "face_info": face_info,
    }
