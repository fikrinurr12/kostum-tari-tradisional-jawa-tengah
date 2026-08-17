"""
utils/model_loader.py  —  TariJateng
Memuat model klasifikasi CNN MobileNetV2 dan menjalankan prediksi.

Deteksi gambar di luar cakupan menggunakan metode Maximum Softmax
Probability (MSP): dua sinyal dari output softmax model (confidence
dan margin) digunakan sebagai indikator apakah gambar kemungkinan
bukan salah satu dari 5 kostum tari yang dilatihkan. Pendekatan ini
tidak memerlukan model atau library tambahan selain TensorFlow/Keras
yang sudah digunakan untuk klasifikasi utama.
"""

import json
import os

import numpy as np
import streamlit as st
from PIL import Image

import config


@st.cache_resource(show_spinner=False)
def load_class_mapping():
    """Memuat pemetaan indeks kelas dari file JSON."""
    if not os.path.exists(config.CLASS_MAPPING_PATH):
        return None
    try:
        with open(config.CLASS_MAPPING_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def load_model():
    """
    Memuat model CNN MobileNetV2 dari file .h5 atau .keras.

    st.cache_resource memastikan model hanya dimuat sekali per sesi
    server, bukan setiap kali pengguna mengunggah gambar baru —
    penting untuk efisiensi memori dan kecepatan respons di environment
    hosting dengan sumber daya terbatas (Railway/Streamlit Cloud).

    compile=False digunakan karena untuk inferensi tidak dibutuhkan
    optimizer/loss/metrics, dan menghindari error deserializasi custom
    metric objects antar versi TensorFlow.
    """
    try:
        import tensorflow as tf
        if os.path.exists(config.MODEL_PATH):
            model = tf.keras.models.load_model(config.MODEL_PATH, compile=False)
            return model, None
        elif os.path.exists(config.MODEL_PATH_KERAS):
            model = tf.keras.models.load_model(config.MODEL_PATH_KERAS, compile=False)
            return model, None
        else:
            return None, (
                "File model tidak ditemukan. Pastikan `model_final.h5` "
                "atau `model_final.keras` tersedia di folder `models/`."
            )
    except Exception as e:
        return None, f"Gagal memuat model: {str(e)}"


def predict(model, mapping, image: Image.Image) -> dict:
    """
    Melakukan prediksi kelas kostum tari dari objek PIL.Image.

    Pipeline:
      1. Preprocessing: resize ke 224×224 px, preprocess_input MobileNetV2
         (normalisasi ke rentang [-1, 1] sesuai spesifikasi arsitektur).
      2. Inferensi: model.predict() menghasilkan vektor probabilitas softmax
         untuk N kelas (5 kostum tari + Non_Tari, dibaca dinamis dari
         class_mapping.json — bukan di-hardcode).
      3. Deteksi di luar cakupan, dua lapis:
           a. LAPIS 1: model memprediksi langsung kelas eksplisit
              config.NEGATIVE_CLASS_KEY ("Non_Tari") — lihat is_non_tari.
           b. LAPIS 2 (jaring pengaman): threshold confidence/margin MSP
              untuk gambar yang tidak tercakup data latih Non_Tari —
              lihat likely_out_of_scope (logika OR, config.py).

    Returns:
        dict dengan kunci:
          pred_class_key       : str  — key kelas prediksi
          pred_label           : str  — nama tampilan kelas prediksi
          confidence           : float — probabilitas kelas teratas (%)
          margin               : float — selisih top-1 vs top-2 (%)
          all_probabilities    : dict  — {class_key: prob%} semua kelas
          is_non_tari          : bool  — True jika model memprediksi
                                          langsung kelas Non_Tari (lapis 1)
          likely_out_of_scope  : bool  — True jika lolos threshold MSP
                                          (lapis 2 — lihat catatan di app.py:
                                          lapis ini diabaikan kalau is_non_tari
                                          sudah True, supaya tidak dobel pesan)
          reason               : str  — "low_confidence", "low_margin", atau
                                         "low_confidence_and_margin"
    """
    # ── 1. Import preprocessing function ─────────────────────────
    try:
        from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    except ImportError:
        from keras.applications.mobilenet_v2 import preprocess_input

    # ── 2. Preprocessing ─────────────────────────────────────────
    img = image.convert("RGB").resize(config.IMG_SIZE)
    arr = np.array(img, dtype=np.float32)
    arr = preprocess_input(arr)                # → rentang [-1, 1]
    arr = np.expand_dims(arr, axis=0)          # → shape (1, 224, 224, 3)

    # ── 3. Inferensi ─────────────────────────────────────────────
    preds = model.predict(arr, verbose=0)[0]   # → shape (5,)

    # ── 4. Susun probabilitas per kelas ──────────────────────────
    idx_to_class = {int(k): v for k, v in mapping["idx_to_class"].items()}
    all_probs = {
        idx_to_class[i]: float(preds[i]) * 100
        for i in range(len(preds))
    }

    # ── 5. Hitung confidence dan margin ──────────────────────────
    sorted_probs = sorted(all_probs.values(), reverse=True)
    confidence   = sorted_probs[0]
    margin       = sorted_probs[0] - sorted_probs[1]
    pred_key     = max(all_probs, key=all_probs.get)

    # ── 6. Deteksi OOD via MSP + margin (logika OR) ──────────────
    conf_fail   = confidence < config.OOD_CONFIDENCE_THRESHOLD
    margin_fail = margin     < config.OOD_MARGIN_THRESHOLD
    likely_ood  = conf_fail or margin_fail

    if conf_fail and margin_fail:
        reason = "low_confidence_and_margin"
    elif conf_fail:
        reason = "low_confidence"
    elif margin_fail:
        reason = "low_margin"
    else:
        reason = None

    # ── 7. Susun label prediksi ───────────────────────────────────
    class_labels = mapping.get("class_labels", {})
    pred_label   = class_labels.get(pred_key, pred_key.replace("_", " "))

    # ── 8. Lapis 1: apakah model langsung memprediksi kelas Non_Tari? ──
    is_non_tari = (pred_key == config.NEGATIVE_CLASS_KEY)

    return {
        "pred_class_key"    : pred_key,
        "pred_label"        : pred_label,
        "confidence"        : confidence,
        "margin"            : margin,
        "all_probabilities" : all_probs,
        "is_non_tari"       : is_non_tari,
        "likely_out_of_scope": likely_ood,
        "reason"            : reason,
    }
