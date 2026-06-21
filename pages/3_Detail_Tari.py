"""
pages/3_Detail_Tari.py
Halaman detail untuk satu jenis tari, diakses dari kartu di halaman
Katalog (bukan dropdown/expander, sesuai revisi tata letak). Tari yang
ditampilkan ditentukan lewat st.session_state['detail_tari_key'], yang
diisi oleh tombol "Lihat Detail" di kartu katalog sebelum switch_page.
"""

import streamlit as st

import config
from utils import styling

st.set_page_config(
    page_title="Detail Tari · TariJateng",
    page_icon="🪭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

styling.inject_global_css()

_switched = styling.render_navbar(active_page="Katalog")
if _switched:
    st.stop()


# ─────────────────────────────────────────────────────────────────
# AMBIL DATA TARI YANG DIPILIH
# ─────────────────────────────────────────────────────────────────
detail_key = st.session_state.get("detail_tari_key")

if not detail_key or detail_key not in config.DANCE_CATALOG:
    st.warning(
        "Tidak ada tarian yang dipilih untuk ditampilkan detailnya. "
        "Silakan pilih salah satu tarian dari halaman Katalog."
    )
    if st.button("📖 Kembali ke Katalog"):
        st.switch_page("pages/1_Katalog.py")
    st.stop()

info = config.DANCE_CATALOG[detail_key]
accent = info["warna_aksen"]
photo_path = config.get_catalog_image_path(detail_key)

PLACEHOLDER_ICONS = {
    "Tari_Bedhaya": "🕊️",
    "Tari_Dolalak": "🎖️",
    "Tari_Gambyong": "🌸",
    "Tari_Golek": "💄",
    "Tari_Srimpi": "🍃",
}


# ─────────────────────────────────────────────────────────────────
# TOMBOL KEMBALI
# ─────────────────────────────────────────────────────────────────
if st.button("← Kembali ke Katalog"):
    st.switch_page("pages/1_Katalog.py")

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# KONTEN DETAIL -- 2 kolom: foto kiri, info kanan
# ─────────────────────────────────────────────────────────────────
col_photo, col_info = st.columns([1, 1.2], gap="large")

with col_photo:
    if photo_path:
        st.image(photo_path)
    else:
        icon = PLACEHOLDER_ICONS.get(detail_key, "🪭")
        st.markdown(
            f'<div class="catalog-card-image" style="color:{accent}; aspect-ratio:1/1;">{icon}</div>',
            unsafe_allow_html=True,
        )

with col_info:
    st.markdown(f'<span class="badge">{info["asal"]}</span>', unsafe_allow_html=True)
    st.markdown(
        f'<h1 style="text-align:left; margin-top:0.6rem;">{info["nama_tampilan"]}</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<p class="muted-text" style="margin-bottom:1rem;">'
        f'Karakter: <strong>{info["karakter"]}</strong></p>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="lead-text" style="text-align:left;">{info["deskripsi"]}</p>', unsafe_allow_html=True)

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# CIRI KHAS KOSTUM & FAKTA SINGKAT
# ─────────────────────────────────────────────────────────────────
col_ciri, col_fakta = st.columns([1.2, 1], gap="large")

with col_ciri:
    styling.eyebrow("Ciri Khas Kostum")
    for ciri in info["ciri_kostum"]:
        st.markdown(f"- {ciri}")

with col_fakta:
    with st.container(border=True):
        styling.eyebrow("Tahukah Kamu?")
        st.markdown(f"*{info['fakta_singkat']}*")

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# NAVIGASI ANTAR TARI (sebelumnya/selanjutnya dalam urutan katalog)
# ─────────────────────────────────────────────────────────────────
current_idx = config.CLASS_ORDER.index(detail_key)
prev_key = config.CLASS_ORDER[current_idx - 1] if current_idx > 0 else None
next_key = config.CLASS_ORDER[(current_idx + 1) % len(config.CLASS_ORDER)]

col_prev, col_next = st.columns(2)
with col_prev:
    if prev_key:
        prev_name = config.DANCE_CATALOG[prev_key]["nama_tampilan"]
        if st.button(f"← {prev_name}", use_container_width=True):
            st.session_state["detail_tari_key"] = prev_key
            st.rerun()
with col_next:
    next_name = config.DANCE_CATALOG[next_key]["nama_tampilan"]
    if st.button(f"{next_name} →", use_container_width=True):
        st.session_state["detail_tari_key"] = next_key
        st.rerun()

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
styling.render_footer()
