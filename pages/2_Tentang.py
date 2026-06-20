"""
pages/2_Tentang.py
Halaman informasi tentang model, metodologi, dan performa evaluasi —
dirangkum dari BAB III & IV skripsi. Layout direvisi mengikuti referensi
visual: kartu metrik kotak-kotak + diagram arsitektur model bergaya
flowchart sederhana (kotak-kotak terhubung secara vertikal).
"""

import json
import os

import streamlit as st

import config
from utils import styling

st.set_page_config(
    page_title="Tentang · TariJateng",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

styling.inject_global_css()

with st.sidebar:
    st.markdown("### Tari Jateng")
    st.markdown("---")
    if st.button("⬅️ Kembali ke Beranda", use_container_width=True):
        st.switch_page("app.py")

styling.render_navbar(active_page="Tentang")


# ─────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────
st.markdown('<div class="center-text">', unsafe_allow_html=True)
st.markdown("# Spesifikasi & Performa Model")
st.markdown(
    '<p class="lead-text" style="margin:0 auto; text-align:center;">'
    "Sistem cerdas berbasis Machine Learning untuk mengidentifikasi "
    "kostum tari tradisional Jawa Tengah secara instan."
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Muat data evaluasi (dipakai di beberapa kartu di bawah)
eval_data = None
if os.path.exists(config.MODEL_CONFIG_PATH):
    try:
        with open(config.MODEL_CONFIG_PATH, "r", encoding="utf-8") as f:
            model_config_json = json.load(f)
        eval_data = model_config_json.get("evaluation")
    except Exception:
        eval_data = None


# ─────────────────────────────────────────────────────────────────
# BARIS KARTU UTAMA: Arsitektur Model | Key Metrics | Inference
# ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1.1, 1, 1], gap="medium")

with col1:
    st.markdown(
        """
        <div class="metric-box">
            <div class="metric-label">1. Model Architecture</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Diagram arsitektur sederhana, kotak terhubung vertikal
    st.markdown(
        f"""
        <div class="arch-box highlight">MobileNetV2 (Pretrained)</div>
        <div class="arch-arrow">↓</div>
        <div class="arch-box">Global Average Pooling</div>
        <div class="arch-arrow">↓</div>
        <div class="arch-box">Dense 256 + BatchNorm + ReLU</div>
        <div class="arch-arrow">↓</div>
        <div class="arch-box">Dropout 0.3</div>
        <div class="arch-arrow">↓</div>
        <div class="arch-box">Dense 128 + BatchNorm + ReLU</div>
        <div class="arch-arrow">↓</div>
        <div class="arch-box">Dropout 0.15</div>
        <div class="arch-arrow">↓</div>
        <div class="arch-box highlight">Dense 5 (Softmax)</div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    datasets_total = "1335+ Gambar"
    if eval_data and eval_data.get("dataset_total"):
        datasets_total = f"{eval_data['dataset_total']} Gambar"

    accuracy_pct = f"{eval_data.get('accuracy', 0) * 100:.1f}%" if eval_data else "—"
    precision_pct = f"{eval_data.get('precision', 0) * 100:.1f}%" if eval_data else "—"
    recall_pct = f"{eval_data.get('recall', 0) * 100:.1f}%" if eval_data else "—"

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">2. Key Metrics</div>
            <p class="muted-text" style="margin-bottom:0.2rem;">Dataset</p>
            <div class="metric-value" style="font-size:1.3rem; margin-bottom:0.9rem;">{datasets_total}</div>
            <p class="muted-text" style="margin-bottom:0.2rem;">Accuracy</p>
            <div class="metric-value" style="font-size:1.3rem; margin-bottom:0.9rem;">{accuracy_pct}</div>
            <p class="muted-text" style="margin-bottom:0.2rem;">Precision</p>
            <div class="metric-value" style="font-size:1.3rem; margin-bottom:0.9rem;">{precision_pct}</div>
            <p class="muted-text" style="margin-bottom:0.2rem;">Recall</p>
            <div class="metric-value" style="font-size:1.3rem;">{recall_pct}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    f1_pct = f"{eval_data.get('f1_score', 0) * 100:.1f}%" if eval_data else "—"
    epoch_total = eval_data.get("epoch_total", "—") if eval_data else "—"

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">3. Hasil Pelatihan</div>
            <p class="muted-text" style="margin-bottom:0.2rem;">F1-Score</p>
            <div class="metric-value" style="margin-bottom:1.2rem;">{f1_pct}</div>
            <p class="muted-text" style="margin-bottom:0.2rem;">Total Epoch</p>
            <div class="metric-value">{epoch_total}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if eval_data:
        target_met = (eval_data.get("accuracy") or 0) >= 0.80
        if target_met:
            st.success("✅ Target akurasi ≥80% tercapai.")
        else:
            st.warning("⚠️ Akurasi di bawah target 80%.")

if not eval_data:
    st.info(
        "Data evaluasi model (`model_config.json`) belum tersedia di "
        "folder `models/`. Unggah file tersebut untuk menampilkan "
        "metrik performa lengkap di sini."
    )

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# AKURASI PER KELAS
# ─────────────────────────────────────────────────────────────────
if eval_data and eval_data.get("per_class_accuracy"):
    styling.eyebrow("Detail Evaluasi")
    st.markdown("## Akurasi per Kelas Kostum")
    per_class = eval_data["per_class_accuracy"]

    for label, val in per_class.items():
        class_key = label.replace(" ", "_")
        accent = config.DANCE_CATALOG.get(class_key, {}).get("warna_aksen", styling.COLORS["terracotta"])
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between; font-size:0.95rem; margin-bottom:0.2rem;">
                <span style="font-weight:600;">{label}</span><span style="font-weight:700;">{val * 100:.1f}%</span>
            </div>
            <div class="confidence-bar-track" style="height:8px; margin-bottom:0.9rem;">
                <div class="confidence-bar-fill" style="width:{val * 100:.1f}%; background-color:{accent};"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# METODOLOGI SINGKAT
# ─────────────────────────────────────────────────────────────────
styling.eyebrow("Metodologi")
st.markdown("## Cara Kerja Sistem")

step_col1, step_col2, step_col3, step_col4 = st.columns(4)
steps = [
    ("📷", "Input Gambar", "Pengguna mengunggah atau memotret foto kostum tari yang ingin diidentifikasi."),
    ("🧹", "Preprocessing", "Gambar diubah ukurannya menjadi 224×224 piksel dan dinormalisasi."),
    ("🧠", "Klasifikasi CNN", "Model MobileNetV2 mengekstraksi fitur visual dan memprediksi kelas."),
    ("📖", "Hasil & Edukasi", "Sistem menampilkan jenis tari beserta informasi budayanya."),
]
for col, (icon, title, desc) in zip([step_col1, step_col2, step_col3, step_col4], steps):
    with col:
        st.markdown(
            f"""
            <div class="metric-box" style="text-align:center; min-height:175px;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-weight:700; margin:0.4rem 0;">{title}</div>
                <p class="muted-text" style="font-size:0.85rem;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
st.caption(
    "Skripsi: *Pengembangan Model CNN Menggunakan Transfer Learning untuk "
    "Klasifikasi Kostum Tari Tradisional Jawa Tengah* — Fasya Maulinada "
    "(NIM. 202251155), Program Studi Teknik Informatika, Fakultas Teknik, "
    "Universitas Muria Kudus, 2025."
)

styling.render_footer()
