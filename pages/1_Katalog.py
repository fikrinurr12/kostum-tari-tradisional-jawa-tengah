"""
pages/1_Katalog.py
Halaman katalog seluruh jenis kostum tari. Jika diakses dari halaman
hasil klasifikasi (lewat session_state['catalog_focus']), kartu kelas
yang relevan otomatis ditampilkan terbuka/disorot di bagian atas.
"""

import streamlit as st

import config
from utils import styling

st.set_page_config(
    page_title="Katalog Kostum Tari · Tari Jawa Tengah",
    page_icon="📖",
    layout="wide",
)

styling.inject_global_css()

with st.sidebar:
    st.markdown("### 🩰 Tari Jawa Tengah")
    st.markdown(
        '<span class="muted-text">Klasifikasi kostum tari tradisional '
        "berbasis Deep Learning</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    if st.button("⬅️ Kembali ke Beranda", width="stretch"):
        st.switch_page("app.py")


# ─────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────
styling.eyebrow("Referensi Budaya")
st.markdown("# Katalog Kostum Tari Tradisional")
st.markdown(
    '<p class="muted-text" style="max-width:680px;">'
    "Jelajahi lima jenis kostum tari tradisional Jawa Tengah yang "
    "dikenali oleh sistem ini, lengkap dengan asal daerah, makna "
    "budaya, dan ciri khas kostumnya."
    "</p>",
    unsafe_allow_html=True,
)

focus_key = st.session_state.get("catalog_focus")

if focus_key and focus_key in config.DANCE_CATALOG:
    info = config.DANCE_CATALOG[focus_key]
    accent = info["warna_aksen"]
    st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
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
    st.markdown("### Semua Kostum Tari Lainnya")


# ─────────────────────────────────────────────────────────────────
# FILTER / PENCARIAN SEDERHANA
# ─────────────────────────────────────────────────────────────────
search_query = st.text_input(
    "Cari nama tari...",
    placeholder="Contoh: Bedhaya, Dolalak, Gambyong...",
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


# ─────────────────────────────────────────────────────────────────
# GRID KATALOG
# ─────────────────────────────────────────────────────────────────
cols_per_row = 2
rows = [display_keys[i:i + cols_per_row] for i in range(0, len(display_keys), cols_per_row)]

for row in rows:
    cols = st.columns(cols_per_row, gap="medium")
    for col, key in zip(cols, row):
        info = config.DANCE_CATALOG[key]
        accent = info["warna_aksen"]
        with col:
            st.markdown(
                f"""
                <div class="catalog-card">
                    <div class="catalog-card-header" style="border-top: 4px solid {accent};">
                        <div class="eyebrow" style="color:{accent};">{info['asal']}</div>
                        <div style="font-family:{styling.FONT_DISPLAY}; font-size:1.4rem; font-weight:700;">
                            {info['nama_tampilan']}
                        </div>
                        <span class="badge">{info['karakter']}</span>
                    </div>
                    <div class="catalog-card-body">
                        <p style="margin-top:0;">{info['ringkasan']}</p>
                    </div>
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

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
st.caption(
    "Konten katalog dirangkum dari kajian pustaka skripsi "
    "*Pengembangan Model CNN Menggunakan Transfer Learning untuk "
    "Klasifikasi Kostum Tari Tradisional Jawa Tengah* (Fasya Maulinada, "
    "Universitas Muria Kudus, 2025)."
)
