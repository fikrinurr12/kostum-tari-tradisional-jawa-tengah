"""
pages/2_Tentang.py
Halaman informasi tentang model, metodologi, dan performa evaluasi —
dirangkum dari BAB III & IV skripsi. Layout direvisi mengikuti referensi
visual: kartu metrik kotak-kotak + diagram arsitektur model bergaya
flowchart sederhana (kotak-kotak terhubung secara vertikal).
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
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


def render_confusion_matrix_chart(cm, labels):
    """Heatmap confusion matrix bergaya tema terracotta aplikasi."""
    fig, ax = plt.subplots(figsize=(5, 4.2))
    cmap = plt.cm.Oranges
    im = ax.imshow(cm, cmap=cmap)

    short_labels = [lbl.replace("Tari_", "").replace("Tari ", "") for lbl in labels]
    ax.set_xticks(range(len(short_labels)))
    ax.set_yticks(range(len(short_labels)))
    ax.set_xticklabels(short_labels, rotation=35, ha="right", fontsize=8)
    ax.set_yticklabels(short_labels, fontsize=8)
    ax.set_xlabel("Prediksi", fontsize=9, color=styling.COLORS["ink_soft"])
    ax.set_ylabel("Label Asli", fontsize=9, color=styling.COLORS["ink_soft"])

    cm_arr = np.array(cm)
    max_val = cm_arr.max() if cm_arr.size else 1
    for i in range(cm_arr.shape[0]):
        for j in range(cm_arr.shape[1]):
            val = cm_arr[i, j]
            text_color = "white" if val > max_val * 0.55 else styling.COLORS["ink"]
            ax.text(j, i, str(val), ha="center", va="center", fontsize=8, color=text_color)

    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    return fig


def render_accuracy_chart(acc_history, val_acc_history=None):
    """Line/area chart accuracy training bergaya tema terracotta aplikasi."""
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    epochs = range(1, len(acc_history) + 1)

    ax.fill_between(epochs, [a * 100 for a in acc_history],
                     color=styling.COLORS["terracotta"], alpha=0.25)
    ax.plot(epochs, [a * 100 for a in acc_history],
            color=styling.COLORS["terracotta"], linewidth=2, label="Training")

    if val_acc_history:
        ax.plot(epochs, [a * 100 for a in val_acc_history],
                color=styling.COLORS["ink_soft"], linewidth=1.6,
                linestyle="--", label="Validasi")
        ax.legend(fontsize=8, frameon=False)

    ax.set_xlabel("Epoch", fontsize=9, color=styling.COLORS["ink_soft"])
    ax.set_ylabel("Akurasi (%)", fontsize=9, color=styling.COLORS["ink_soft"])
    ax.set_ylim(0, 100)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=8)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    fig.tight_layout()
    return fig

with st.sidebar:
    st.markdown("### Tari Jateng")
    st.markdown("---")
    if st.button("⬅️ Kembali ke Beranda", use_container_width=True):
        st.switch_page("app.py")

_switched = styling.render_navbar(active_page="Tentang ML")
if _switched:
    st.stop()


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
# SECTION 1: RINGKASAN ARSITEKTUR (st.info + teks naratif)
# ─────────────────────────────────────────────────────────────────
styling.eyebrow("Arsitektur")
col_arch_left, col_arch_right = st.columns([1, 2], gap="large")

with col_arch_left:
    st.info("**MobileNetV2** (Fine-tuned)")

with col_arch_right:
    st.markdown(
        '<p class="lead-text">MobileNetV2 dipilih karena ukurannya yang '
        "ringan namun tetap akurat untuk klasifikasi citra, menjadikannya "
        "ideal untuk diterapkan pada aplikasi web seperti ini. Model "
        "dilatih ulang (transfer learning) dengan dua fase: ekstraksi "
        "fitur pada lapisan dasar yang dibekukan, lalu fine-tuning pada "
        "lapisan akhir agar dapat mengenali pola visual khas lima "
        "kostum tari tradisional Jawa Tengah.</p>",
        unsafe_allow_html=True,
    )

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SECTION 2: METRIK PERFORMA (Bento Grid -- st.metric 4 kolom)
# ─────────────────────────────────────────────────────────────────
styling.eyebrow("Performa")
st.markdown("## Metrik Evaluasi Model")

dataset_total = eval_data.get("dataset_total") if eval_data else None
accuracy_val = eval_data.get("accuracy") if eval_data else None
precision_val = eval_data.get("precision") if eval_data else None
recall_val = eval_data.get("recall") if eval_data else None

m1, m2, m3, m4 = st.columns(4)
with m1:
    with st.container(border=True):
        st.metric(label="Total Dataset", value=f"{dataset_total}+ Gambar" if dataset_total else "—")
with m2:
    with st.container(border=True):
        st.metric(label="Akurasi Model", value=f"{accuracy_val * 100:.1f}%" if accuracy_val else "—")
with m3:
    with st.container(border=True):
        st.metric(label="Precision", value=f"{precision_val * 100:.1f}%" if precision_val else "—")
with m4:
    with st.container(border=True):
        st.metric(label="Recall", value=f"{recall_val * 100:.1f}%" if recall_val else "—")

if eval_data:
    target_met = (eval_data.get("accuracy") or 0) >= 0.80
    if target_met:
        st.success("✅ Model mencapai target akurasi minimal 80% yang ditetapkan dalam penelitian.")
    else:
        st.warning("⚠️ Akurasi model saat ini berada di bawah target 80% yang ditetapkan dalam penelitian.")
else:
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
# CHART VISUAL: Confusion Matrix & Accuracy Training
# ─────────────────────────────────────────────────────────────────
has_cm = eval_data and eval_data.get("confusion_matrix") and eval_data.get("confusion_matrix_labels")
has_history = eval_data and eval_data.get("accuracy_history")

if has_cm or has_history:
    styling.eyebrow("Visualisasi Hasil")
    st.markdown("## Confusion Matrix & Kurva Akurasi")

    chart_col1, chart_col2 = st.columns(2, gap="medium")

    with chart_col1:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Confusion Matrix</div>', unsafe_allow_html=True)
        if has_cm:
            fig_cm = render_confusion_matrix_chart(
                eval_data["confusion_matrix"], eval_data["confusion_matrix_labels"]
            )
            st.pyplot(fig_cm)
        else:
            st.markdown(
                '<p class="muted-text">Data confusion matrix belum tersedia '
                "di model_config.json.</p>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Kurva Akurasi Training</div>', unsafe_allow_html=True)
        if has_history:
            fig_acc = render_accuracy_chart(
                eval_data["accuracy_history"], eval_data.get("val_accuracy_history")
            )
            st.pyplot(fig_acc)
        else:
            st.markdown(
                '<p class="muted-text">Data riwayat akurasi training belum '
                "tersedia di model_config.json.</p>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

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
