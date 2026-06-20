"""
pages/2_Tentang.py
Halaman informasi tentang model, metodologi, dan performa evaluasi —
dirangkum dari BAB III & IV skripsi.
"""

import json
import os

import streamlit as st

import config
from utils import styling

st.set_page_config(
    page_title="Tentang · Tari Jawa Tengah",
    page_icon="ℹ️",
    layout="wide",
)

styling.inject_global_css()

with st.sidebar:
    st.markdown("### 🩰 Tari Jawa Tengah")
    st.markdown("---")
    if st.button("⬅️ Kembali ke Beranda", use_container_width=True):
        st.switch_page("app.py")


styling.eyebrow("Tentang Sistem")
st.markdown("# Metodologi & Performa Model")
st.markdown(
    '<p class="muted-text" style="max-width:680px;">'
    "Ringkasan teknis di balik sistem klasifikasi ini, dirangkum dari "
    "penelitian skripsi <em>Pengembangan Model CNN Menggunakan Transfer "
    "Learning untuk Klasifikasi Kostum Tari Tradisional Jawa Tengah</em>."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# RINGKASAN MODEL
# ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="card">
            <div class="eyebrow">Arsitektur</div>
            <div style="font-size:1.3rem; font-weight:700;">MobileNetV2</div>
            <p class="muted-text">+ Custom Dense Head</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="card">
            <div class="eyebrow">Metode</div>
            <div style="font-size:1.3rem; font-weight:700;">Transfer Learning</div>
            <p class="muted-text">Feature Extraction + Fine-Tuning</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="card">
            <div class="eyebrow">Jumlah Kelas</div>
            <div style="font-size:1.3rem; font-weight:700;">5 Jenis Kostum</div>
            <p class="muted-text">Tari Tradisional Jawa Tengah</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# METRIK EVALUASI (dibaca dari model_config.json jika tersedia)
# ─────────────────────────────────────────────────────────────────
styling.eyebrow("Hasil Evaluasi")
st.markdown("## Performa Model pada Data Uji")

eval_data = None
if os.path.exists(config.MODEL_CONFIG_PATH):
    try:
        with open(config.MODEL_CONFIG_PATH, "r", encoding="utf-8") as f:
            model_config = json.load(f)
        eval_data = model_config.get("evaluation")
    except Exception:
        eval_data = None

if eval_data:
    m1, m2, m3, m4 = st.columns(4)
    metrics_display = [
        ("Akurasi", eval_data.get("accuracy")),
        ("Presisi", eval_data.get("precision")),
        ("Recall", eval_data.get("recall")),
        ("F1-Score", eval_data.get("f1_score")),
    ]
    for col, (label, value) in zip([m1, m2, m3, m4], metrics_display):
        with col:
            pct = f"{value * 100:.2f}%" if value is not None else "—"
            st.markdown(
                f"""
                <div class="card" style="text-align:center;">
                    <div class="eyebrow">{label}</div>
                    <div style="font-size:1.8rem; font-weight:700; color:{styling.COLORS['sogan']};">{pct}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    target_met = (eval_data.get("accuracy") or 0) >= 0.80
    if target_met:
        st.success("✅ Model mencapai target akurasi minimal 80% yang ditetapkan dalam penelitian.")
    else:
        st.warning(
            "⚠️ Akurasi model saat ini berada di bawah target 80% yang "
            "ditetapkan dalam penelitian. Hasil klasifikasi tetap "
            "ditampilkan sebagai estimasi terbaik model."
        )

    per_class = eval_data.get("per_class_accuracy")
    if per_class:
        st.markdown("#### Akurasi per Kelas")
        for label, val in per_class.items():
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; font-size:0.92rem; margin-bottom:0.15rem;">
                    <span>{label}</span><span style="font-weight:600;">{val * 100:.1f}%</span>
                </div>
                <div class="confidence-bar-track" style="height:6px; margin-bottom:0.6rem;">
                    <div class="confidence-bar-fill" style="width:{val * 100:.1f}%; background-color:{styling.COLORS['sogan']};"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info(
        "Data evaluasi model (`model_config.json`) belum tersedia di "
        "folder `models/`. Unggah file tersebut untuk menampilkan "
        "metrik performa di sini."
    )

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# METODOLOGI SINGKAT
# ─────────────────────────────────────────────────────────────────
styling.eyebrow("Metodologi")
st.markdown("## Cara Kerja Sistem")

step_col1, step_col2, step_col3, step_col4 = st.columns(4)
steps = [
    ("📷", "Unggah Gambar", "Pengguna mengunggah foto kostum tari yang ingin diidentifikasi."),
    ("🧹", "Preprocessing", "Gambar diubah ukurannya menjadi 224×224 piksel dan dinormalisasi."),
    ("🧠", "Klasifikasi CNN", "Model MobileNetV2 mengekstraksi fitur visual dan memprediksi kelas."),
    ("📖", "Hasil & Edukasi", "Sistem menampilkan jenis tari beserta informasi budayanya."),
]
for col, (icon, title, desc) in zip([step_col1, step_col2, step_col3, step_col4], steps):
    with col:
        st.markdown(
            f"""
            <div class="card" style="text-align:center; min-height:170px;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-weight:700; margin:0.3rem 0;">{title}</div>
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
