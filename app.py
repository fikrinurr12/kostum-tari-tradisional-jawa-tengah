"""
app.py
Halaman utama aplikasi: beranda + upload & klasifikasi gambar kostum tari.

Setelah klasifikasi berhasil, hasil disimpan ke st.session_state dan
pengguna diarahkan (via tombol) ke halaman Katalog dengan kelas yang
relevan sudah terbuka otomatis.
"""

import time

import streamlit as st
from PIL import Image

import config
from utils import model_loader, styling

st.set_page_config(
    page_title="Klasifikasi Kostum Tari Jawa Tengah",
    page_icon="🩰",
    layout="wide",
    initial_sidebar_state="expanded",
)

styling.inject_global_css()


# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🩰 Tari Jawa Tengah")
    st.markdown(
        '<span class="muted-text">Klasifikasi kostum tari tradisional '
        "berbasis Deep Learning</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        '<span class="muted-text">'
        "Model: CNN MobileNetV2 (Transfer Learning)<br>"
        "5 kelas kostum tari Jawa Tengah"
        "</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption(
        "Skripsi: *Pengembangan Model CNN Menggunakan Transfer Learning "
        "untuk Klasifikasi Kostum Tari Tradisional Jawa Tengah*"
    )
    st.caption("Fasya Maulinada · Universitas Muria Kudus · 2025")


# ─────────────────────────────────────────────────────────────────
# HERO / BERANDA
# ─────────────────────────────────────────────────────────────────
col_hero_text, col_hero_visual = st.columns([1.3, 1], gap="large")

with col_hero_text:
    styling.eyebrow("Pelestarian Budaya · Kecerdasan Buatan")
    st.markdown("# Kenali Kostum Tari Tradisional Jawa Tengah")
    st.markdown(
        '<p style="font-size:1.05rem; line-height:1.6; max-width:560px;">'
        "Unggah foto kostum tari, dan sistem akan mengenali jenisnya "
        "secara otomatis menggunakan model Convolutional Neural Network "
        "(CNN) dengan pendekatan Transfer Learning arsitektur "
        "MobileNetV2 — dilatih untuk mengenali lima kostum tari khas "
        "Jawa Tengah."
        "</p>",
        unsafe_allow_html=True,
    )
    badges = " ".join(
        f'<span class="badge">{config.DANCE_CATALOG[k]["nama_tampilan"]}</span>'
        for k in config.CLASS_ORDER
    )
    st.markdown(badges, unsafe_allow_html=True)

with col_hero_visual:
    st.markdown(
        f"""
        <div class="card" style="text-align:center; padding:2rem 1.5rem;">
            <div style="font-size:3rem;">🪭</div>
            <div class="eyebrow" style="margin-top:0.5rem;">Lima Kelas Kostum</div>
            <div style="font-family:{styling.FONT_DISPLAY}; font-size:1.4rem; font-weight:700;">
                Bedhaya · Dolalak · Gambyong<br>Golek · Srimpi
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# MUAT MODEL & MAPPING KELAS
# ─────────────────────────────────────────────────────────────────
mapping = model_loader.load_class_mapping()

if mapping is None:
    st.error(
        "⚠️ File `class_mapping.json` tidak ditemukan di folder `models/`. "
        "Pastikan file tersebut sudah diunggah ke repository sebelum "
        "melakukan klasifikasi gambar."
    )
    st.stop()

with st.spinner("Memuat model klasifikasi..."):
    model, model_error = model_loader.load_model()

if model_error:
    st.error(f"⚠️ {model_error}")
    st.info(
        "Klasifikasi gambar belum bisa dijalankan, tapi kamu tetap bisa "
        "menjelajahi halaman **Katalog** di menu sebelah kiri."
    )
    st.stop()


# ─────────────────────────────────────────────────────────────────
# BAGIAN UPLOAD & KLASIFIKASI
# ─────────────────────────────────────────────────────────────────
styling.eyebrow("Coba Sekarang")
st.markdown("## Unggah Foto Kostum Tari")
st.markdown(
    '<p class="muted-text">Gunakan foto yang jelas, dengan kostum tari '
    "terlihat penuh dan tidak tertutup objek lain, untuk hasil terbaik.</p>",
    unsafe_allow_html=True,
)

col_upload, col_preview = st.columns([1, 1], gap="large")

uploaded_file = col_upload.file_uploader(
    "Pilih gambar (JPG, JPEG, atau PNG)",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
    except Exception:
        st.error("⚠️ Gambar tidak bisa dibuka. Coba unggah file gambar lain.")
        st.stop()

    with col_preview:
        st.image(image, caption="Pratinjau gambar yang diunggah")

    with col_upload:
        classify_clicked = st.button("🔍 Klasifikasikan Gambar", use_container_width=True)

    if classify_clicked:
        with st.spinner("Menganalisis pola visual kostum..."):
            time.sleep(0.4)  # jeda kecil agar transisi terasa, bukan instan
            result = model_loader.predict(model, mapping, image)

        st.session_state["last_result"] = result
        st.session_state["last_image_caption"] = uploaded_file.name
        st.rerun()

# ─────────────────────────────────────────────────────────────────
# TAMPILKAN HASIL (jika ada hasil tersimpan di session_state)
# ─────────────────────────────────────────────────────────────────
if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    pred_key = result["pred_class_key"]
    pred_info = config.DANCE_CATALOG.get(pred_key, {})
    accent = pred_info.get("warna_aksen", "#8B5A2B")
    confidence = result["confidence"]

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
    styling.eyebrow("Hasil Klasifikasi")

    if confidence < config.CONFIDENCE_THRESHOLD:
        st.warning(
            f"Model kurang yakin dengan prediksi ini (keyakinan "
            f"{confidence:.1f}%). Tetap ditampilkan sebagai tebakan "
            f"terbaik, tapi pertimbangkan untuk mengunggah foto lain "
            f"yang lebih jelas."
        )

    st.markdown(
        f"""
        <div class="result-card" style="--accent-color:{accent};">
            <div class="eyebrow" style="color:{accent};">Jenis Kostum Terdeteksi</div>
            <div class="pred-title" style="color:{accent};">{pred_info.get('nama_tampilan', result['pred_label'])}</div>
            <p class="muted-text" style="margin-bottom:0.8rem;">
                Asal: {pred_info.get('asal', '-')} &nbsp;·&nbsp; Karakter: {pred_info.get('karakter', '-')}
            </p>
            <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:0.2rem;">
                <span>Tingkat Keyakinan</span>
                <span style="font-weight:700;">{confidence:.1f}%</span>
            </div>
            <div class="confidence-bar-track">
                <div class="confidence-bar-fill" style="width:{confidence:.1f}%; background-color:{accent};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Rincian probabilitas semua kelas
    with st.expander("Lihat rincian probabilitas semua kelas"):
        for cls_key, prob in result["all_probabilities"].items():
            cls_info = config.DANCE_CATALOG.get(cls_key, {})
            label = cls_info.get("nama_tampilan", cls_key)
            cls_accent = cls_info.get("warna_aksen", "#8B5A2B")
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; font-size:0.9rem; margin-bottom:0.15rem;">
                    <span>{label}</span><span style="font-weight:600;">{prob:.1f}%</span>
                </div>
                <div class="confidence-bar-track" style="height:6px; margin-bottom:0.6rem;">
                    <div class="confidence-bar-fill" style="width:{prob:.1f}%; background-color:{cls_accent};"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("📖 Lihat Detail Lengkap di Katalog", use_container_width=True):
            st.session_state["catalog_focus"] = pred_key
            st.switch_page("pages/1_Katalog.py")
    with col_b:
        if st.button("🔄 Klasifikasikan Gambar Lain", use_container_width=True):
            del st.session_state["last_result"]
            st.rerun()
