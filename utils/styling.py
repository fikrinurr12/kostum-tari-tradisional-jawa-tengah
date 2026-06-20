"""
utils/styling.py
CSS kustom terpusat untuk seluruh aplikasi.

Arah desain (revisi sesuai referensi visual): editorial/majalah minimalis
-- latar putih bersih dominan, navbar tipis dengan brand text, judul
serif besar tebal, kartu katalog gaya portfolio (foto besar di atas,
teks rapi di bawah), dan kartu metrik kotak-kotak untuk halaman teknis.
Aksen warna terracotta/soga merujuk pada warna kostum tari itu sendiri,
bukan tema "kertas krem" yang lebih gelap seperti revisi sebelumnya.
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────────
# TOKEN DESAIN
# ─────────────────────────────────────────────────────────────────
COLORS = {
    "ink": "#1A1A1A",          # teks utama, hampir hitam (bukan coklat lagi)
    "paper": "#FFFFFF",        # latar utama, putih bersih
    "paper_alt": "#F7F5F2",    # latar sekunder/section pemisah
    "terracotta": "#B5663F",   # aksen utama -- warna kostum/selendang
    "terracotta_dark": "#8F4D2C",
    "terracotta_soft": "#F1E2D8",  # tint lembut untuk background badge/chip
    "ink_soft": "#6B6B6B",     # teks sekunder/muted
    "border": "#E8E5E0",
    "success": "#4A7857",
    "warning": "#B5663F",
}

FONT_DISPLAY = "'Playfair Display', Georgia, serif"
FONT_BODY = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"


def inject_global_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: {FONT_BODY};
        }}

        /* ── Latar & kontainer utama ───────────────────────────── */
        .stApp {{
            background-color: {COLORS['paper']};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {COLORS['paper']};
            border-right: 1px solid {COLORS['border']};
        }}

        /* ── Navbar kustom (brand + menu) ──────────────────────── */
        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.9rem 0 0.9rem 0;
            border-bottom: 1px solid {COLORS['border']};
            margin-bottom: 2.5rem;
        }}
        .navbar-brand {{
            font-family: {FONT_DISPLAY};
            font-size: 1.4rem;
            font-weight: 700;
            color: {COLORS['ink']};
            letter-spacing: -0.01em;
        }}
        .navbar-brand span {{
            color: {COLORS['terracotta']};
        }}
        .navbar-menu a {{
            font-size: 0.92rem;
            font-weight: 500;
            color: {COLORS['ink_soft']};
            margin-left: 1.8rem;
            text-decoration: none;
        }}

        /* ── Tipografi ──────────────────────────────────────────── */
        h1, h2, h3 {{
            font-family: {FONT_DISPLAY};
            color: {COLORS['ink']};
            font-weight: 700;
            letter-spacing: -0.015em;
            line-height: 1.15;
        }}

        h1 {{
            font-size: 2.7rem !important;
            text-align: center;
        }}

        p, span, div, label {{
            color: {COLORS['ink']};
        }}

        .lead-text {{
            color: {COLORS['ink_soft']};
            font-size: 1.05rem;
            line-height: 1.65;
            max-width: 560px;
        }}

        .muted-text {{
            color: {COLORS['ink_soft']};
            font-size: 0.92rem;
        }}

        .center-text {{
            text-align: center;
        }}

        /* ── Eyebrow label (kecil di atas judul) ───────────────── */
        .eyebrow {{
            font-family: {FONT_BODY};
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: {COLORS['terracotta']};
            margin-bottom: 0.5rem;
        }}

        /* ── Tombol ─────────────────────────────────────────────── */
        .stButton > button, .stDownloadButton > button {{
            background-color: {COLORS['terracotta']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            font-family: {FONT_BODY};
            transition: background-color 0.15s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            background-color: {COLORS['terracotta_dark']};
            color: white;
        }}
        .stButton > button[kind="secondary"] {{
            background-color: white;
            color: {COLORS['ink']};
            border: 1.5px solid {COLORS['border']};
        }}
        .stButton > button[kind="secondary"]:hover {{
            border-color: {COLORS['terracotta']};
            color: {COLORS['terracotta']};
            background-color: white;
        }}

        /* ── Kartu generik ──────────────────────────────────────── */
        .card {{
            background-color: white;
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1.5rem 1.6rem;
            margin-bottom: 1rem;
        }}

        /* ── Kartu metrik kotak (gaya halaman Tentang/ML) ──────── */
        .metric-box {{
            background-color: white;
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1.3rem 1.4rem;
            margin-bottom: 1rem;
            height: 100%;
        }}
        .metric-box .metric-label {{
            font-size: 0.78rem;
            font-weight: 600;
            color: {COLORS['ink_soft']};
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.5rem;
        }}
        .metric-box .metric-value {{
            font-family: {FONT_DISPLAY};
            font-size: 1.9rem;
            font-weight: 700;
            color: {COLORS['ink']};
        }}

        /* ── Kartu hasil klasifikasi (signature element) ───────── */
        .result-card {{
            background: white;
            border: 1px solid {COLORS['border']};
            border-left: 5px solid var(--accent-color, {COLORS['terracotta']});
            border-radius: 12px;
            padding: 1.9rem 2.1rem;
            margin: 1rem 0 1.5rem 0;
        }}

        .result-card .pred-title {{
            font-family: {FONT_DISPLAY};
            font-size: 2rem;
            font-weight: 700;
            margin: 0.2rem 0 0.4rem 0;
        }}

        .confidence-bar-track {{
            background-color: {COLORS['paper_alt']};
            border-radius: 999px;
            height: 10px;
            width: 100%;
            overflow: hidden;
            margin-top: 0.4rem;
        }}
        .confidence-bar-fill {{
            height: 100%;
            border-radius: 999px;
        }}

        /* ── Badge / chip kecil ─────────────────────────────────── */
        .badge {{
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            background-color: {COLORS['terracotta_soft']};
            color: {COLORS['terracotta_dark']};
            margin-right: 0.4rem;
            margin-bottom: 0.4rem;
        }}

        /* ── Kartu katalog gaya majalah (foto besar + teks bawah) ── */
        .catalog-card {{
            background-color: white;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 1.8rem;
        }}
        .catalog-card-image {{
            width: 100%;
            aspect-ratio: 4/3;
            background-color: {COLORS['paper_alt']};
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            margin-bottom: 1rem;
            font-size: 3rem;
        }}
        .catalog-card-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        .catalog-card-title {{
            font-family: {FONT_DISPLAY};
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }}
        .catalog-card-desc {{
            color: {COLORS['ink_soft']};
            font-size: 0.9rem;
            line-height: 1.55;
        }}

        /* ── Divider tipis ──────────────────────────────────────── */
        .thin-divider {{
            border: none;
            border-top: 1px solid {COLORS['border']};
            margin: 2rem 0;
        }}

        /* ── Sembunyikan elemen default Streamlit yang kurang perlu */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background-color: transparent;}}

        /* ── Upload box & camera kustom (gaya kartu terpusat) ──── */
        [data-testid="stFileUploader"], [data-testid="stCameraInput"] {{
            background-color: {COLORS['paper_alt']};
            border: 1.5px dashed {COLORS['border']};
            border-radius: 14px;
            padding: 1rem;
        }}
        [data-testid="stFileUploaderDropzone"] {{
            background-color: transparent;
        }}

        /* ── Kartu pembungkus upload terpusat (signature hero) ─── */
        .upload-card-wrapper {{
            background-color: {COLORS['paper_alt']};
            border: 1.5px dashed {COLORS['border']};
            border-radius: 16px;
            padding: 1.6rem 1.8rem;
            max-width: 420px;
        }}
        .upload-card-icon {{
            text-align: center;
            font-size: 2.2rem;
            color: {COLORS['terracotta']};
            margin-bottom: 0.4rem;
        }}
        .upload-card-hint {{
            text-align: center;
            color: {COLORS['ink_soft']};
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }}

        /* ── Tabs kustom ────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 1.5rem;
            justify-content: center;
        }}
        .stTabs [data-baseweb="tab"] {{
            font-weight: 600;
            color: {COLORS['ink_soft']};
        }}
        .stTabs [aria-selected="true"] {{
            color: {COLORS['terracotta']} !important;
        }}

        /* ── Navbar radio (st.radio yang disulap jadi menu teks) ── */
        /* st.radio TIDAK punya kotak/border solid seperti st.button,
           jadi pendekatan ini jauh lebih simpel: cukup sembunyikan
           bulatan radio bawaan dan styling label teksnya. */

        /* Susun opsi radio jadi horizontal rapat, rata kanan */
        div[data-testid="stRadio"] > div[role="radiogroup"] {{
            display: flex;
            flex-direction: row;
            justify-content: flex-end;
            gap: 1.6rem;
            flex-wrap: wrap;
        }}

        /* Sembunyikan bulatan radio (elemen visual lingkaran) */
        div[data-testid="stRadio"] label > div:first-child {{
            display: none !important;
        }}

        /* Styling label teks supaya terlihat seperti menu link */
        div[data-testid="stRadio"] label {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0.3rem 0 !important;
            margin: 0 !important;
            cursor: pointer;
        }}
        div[data-testid="stRadio"] label p {{
            font-weight: 600;
            font-size: 0.95rem;
            color: {COLORS['ink_soft']};
        }}
        /* Opsi yang sedang dipilih (aktif) ditandai Streamlit lewat
           atribut aria-checked pada elemen radio di dalam label. */
        div[data-testid="stRadio"] label:has(input:checked) p {{
            color: {COLORS['terracotta']} !important;
            font-weight: 700;
        }}
        div[data-testid="stRadio"] label:hover p {{
            color: {COLORS['terracotta']} !important;
        }}

        /* Sembunyikan elemen radio asli (input) tapi tetap ada di DOM
           supaya tetap bisa diklik/fungsional, hanya visualnya hilang. */
        div[data-testid="stRadio"] input[type="radio"] {{
            position: absolute;
            opacity: 0;
            width: 1px;
            height: 1px;
        }}

        /* ── Navbar responsif di mobile: paksa tetap horizontal ──── */
        @media (max-width: 640px) {{
            div[data-testid="stRadio"] > div[role="radiogroup"] {{
                gap: 0.9rem;
                justify-content: flex-start;
            }}
            div[data-testid="stRadio"] label p {{
                font-size: 0.82rem;
            }}
            .navbar-brand {{
                font-size: 1.15rem !important;
            }}
        }}

        /* ── Chart container (Confusion Matrix / Accuracy) ──────── */
        .chart-box {{
            background-color: white;
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 1.3rem 1.4rem 0.8rem 1.4rem;
            margin-bottom: 1rem;
        }}
        .chart-box .chart-title {{
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 0.6rem;
        }}

        /* ── Footer kustom ──────────────────────────────────────── */
        .site-footer {{
            border-top: 1px solid {COLORS['border']};
            padding-top: 1.5rem;
            margin-top: 3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: {COLORS['ink_soft']};
            font-size: 0.85rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def eyebrow(text: str):
    st.markdown(f'<div class="eyebrow">{text}</div>', unsafe_allow_html=True)


def render_navbar(active_page: str = "Home"):
    """
    Navbar FUNGSIONAL: brand kiri (HTML statis) + menu kanan berupa
    st.radio horizontal yang bulatannya disembunyikan lewat CSS,
    sehingga terlihat seperti menu teks biasa.

    st.radio dipilih (bukan <a> HTML atau st.button) karena pendekatan
    button sebelumnya tetap menyisakan border/box yang sulit dihapus
    sepenuhnya di semua kondisi (hover/focus/active) tanpa mengetahui
    persis struktur CSS internal Streamlit. st.radio horizontal lebih
    predictable untuk displai sebagai menu teks polos.

    Mengembalikan True jika terjadi perpindahan halaman (supaya kode
    pemanggil tahu harus st.stop() / tidak lanjut render lebih jauh).
    """
    page_files = {
        "Home": "app.py",
        "Katalog": "pages/1_Katalog.py",
        "Tentang ML": "pages/2_Tentang.py",
    }
    pages = list(page_files.keys())

    # Normalisasi: kalau dipanggil dengan "Tentang" (label lama),
    # tetap cocokkan ke "Tentang ML".
    if active_page == "Tentang":
        active_page = "Tentang ML"

    col_brand, col_menu = st.columns([2, 3])

    with col_brand:
        st.markdown(
            '<div class="navbar-brand" style="padding-top:0.5rem;">Tari<span>Jateng</span></div>',
            unsafe_allow_html=True,
        )

    with col_menu:
        selected = st.radio(
            "Navigasi",
            options=pages,
            index=pages.index(active_page) if active_page in pages else 0,
            horizontal=True,
            label_visibility="collapsed",
            key="main_navbar_radio",
        )

    st.markdown('<hr class="thin-divider" style="margin-top:0.5rem;">', unsafe_allow_html=True)

    if selected != active_page:
        target_file = page_files[selected]
        st.switch_page(target_file)
        return True
    return False


def render_footer():
    st.markdown(
        """
        <div class="site-footer">
            <div><strong>TariJateng</strong> &nbsp;·&nbsp; Skripsi Fasya Maulinada, 2025</div>
            <div>Universitas Muria Kudus</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
