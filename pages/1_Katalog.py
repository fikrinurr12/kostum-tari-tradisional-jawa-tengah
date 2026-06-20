"""
pages/1_Katalog.py
Halaman katalog seluruh jenis kostum tari, gaya editorial/majalah
(kartu foto besar di atas, teks rapi di bawah) sesuai referensi visual.
Jika diakses dari halaman hasil klasifikasi (lewat
session_state['catalog_focus']), kartu kelas yang relevan otomatis
ditampilkan terbuka/disorot di bagian atas.
"""

import streamlit as st

import config
from utils import styling

st.set_page_config(
    page_title="Katalog · TariJateng",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

styling.inject_global_css()

with st.sidebar:
    st.markdown("### Tari Jateng")
    st.markdown("---")
    if st.button("⬅️ Kembali ke Beranda", use_container_width=True):
        st.switch_page("app.py")

styling.render_navbar(active_page="Katalog")


# ─────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="center-text">', unsafe_allow_html=True
)
st.markdown("# Katalog Kostum & Tari")
st.markdown(
    '<p class="lead-text" style="margin:0 auto; text-align:center;">'
    "Sistem cerdas berbasis Machine Learning untuk mengidentifikasi "
    "kostum tari tradisional Jawa Tengah secara instan."
    "</p>",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

focus_key = st.session_state.get("catalog_focus")

if focus_key and focus_key in config.DANCE_CATALOG:
    info = config.DANCE_CATALOG[focus_key]
    accent = info["warna_aksen"]
    styling.eyebrow("Hasil Klasifikasi Terakhir Kamu")

    st.markdown(
        f"""
        <div class="result-card" style="--accent-color:{accent};">
            <div class="pred-title" style="color:{accent};">{info['nama_tampilan']}</div>
            <p style="margin-bottom:0.6rem;">{info['deskripsi']}</p>
            <p class="muted-text" style="margin-bottom:0.4rem;"><strong>Ciri khas kostum:</strong></p>
            <ul style="margin-top:0;">
                {''.join(f"<li>{ciri}</li>" for ciri in info['ciri_kostum'])}
            </ul>
            <p class="muted-text" style="font-style:italic; margin-top:0.6rem;">💡 {info['fakta_singkat']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Tutup sorotan ini"):
        del st.session_state["catalog_focus"]
        st.rerun()

    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# FILTER / PENCARIAN SEDERHANA
# ─────────────────────────────────────────────────────────────────
search_query = st.text_input(
    "Cari nama tari...",
    placeholder="🔍  Cari nama tari, misalnya Bedhaya atau Gambyong...",
    label_visibility="collapsed",
)

display_keys = [
    k for k in config.CLASS_ORDER
    if not focus_key or k != focus_key  # jangan tampilkan dua kali kelas yang sudah disorot
]

if search_query.strip():
    display_keys = [
        k for k in display_keys
        if search_query.strip().lower() in config.DANCE_CATALOG[k]["nama_tampilan"].lower()
    ]

if not display_keys:
    st.info("Tidak ada tarian yang cocok dengan pencarian kamu.")

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# GRID KATALOG -- gaya majalah, ASIMETRIS: 2 kartu besar di baris
# pertama, sisanya 3 kartu lebih kecil di baris kedua (sesuai acuan)
# ─────────────────────────────────────────────────────────────────
PLACEHOLDER_ICONS = {
    "Tari_Bedhaya": "🕊️",
    "Tari_Dolalak": "🎖️",
    "Tari_Gambyong": "🌸",
    "Tari_Golek": "💄",
    "Tari_Srimpi": "🍃",
}


def render_catalog_card(key):
    info = config.DANCE_CATALOG[key]
    accent = info["warna_aksen"]
    photo_path = config.get_catalog_image_path(key)

    st.markdown('<div class="catalog-card">', unsafe_allow_html=True)

    if photo_path:
        st.markdown('<div class="catalog-card-image">', unsafe_allow_html=True)
        st.image(photo_path)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        icon = PLACEHOLDER_ICONS.get(key, "🪭")
        st.markdown(
            f'<div class="catalog-card-image" style="color:{accent};">{icon}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="catalog-card-title">{info['nama_tampilan']}</div>
        <p class="catalog-card-desc">{info['ringkasan']}</p>
        <span class="badge" style="margin-top:0.5rem;">{info['asal']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander(f"Lihat detail {info['nama_tampilan']}"):
        st.markdown(info["deskripsi"])
        st.markdown("**Ciri khas kostum:**")
        for ciri in info["ciri_kostum"]:
            st.markdown(f"- {ciri}")
        st.markdown(f"*💡 {info['fakta_singkat']}*")


# Baris pertama: 2 kartu besar (jika tersedia minimal 2 item)
first_row = display_keys[:2]
remaining = display_keys[2:]

if first_row:
    cols = st.columns(len(first_row) if len(first_row) < 2 else 2, gap="medium")
    for col, key in zip(cols, first_row):
        with col:
            render_catalog_card(key)

# Baris berikutnya: kartu lebih kecil, 3 per baris
if remaining:
    rows = [remaining[i:i + 3] for i in range(0, len(remaining), 3)]
    for row in rows:
        cols = st.columns(3, gap="medium")
        for col, key in zip(cols, row):
            with col:
                render_catalog_card(key)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
st.caption(
    "Konten katalog dirangkum dari kajian pustaka skripsi "
    "*Pengembangan Model CNN Menggunakan Transfer Learning untuk "
    "Klasifikasi Kostum Tari Tradisional Jawa Tengah* (Fasya Maulinada, "
    "Universitas Muria Kudus, 2025)."
)

styling.render_footer()
