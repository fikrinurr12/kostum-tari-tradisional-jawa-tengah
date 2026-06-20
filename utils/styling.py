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

        /* ── Navbar link button (st.button disulap jadi link teks) ── */
        /* Selector dikonfirmasi LANGSUNG dari hasil inspect element
           browser: tombol Streamlit punya data-testid="baseButton-secondary"
           pada elemen <button> itu sendiri (bukan pada div pembungkusnya). */

        /* Kecilkan gap antar kolom KHUSUS di dalam wrapper menu navbar. */
        div.navbar-menu-wrapper [data-testid="stHorizontalBlock"] {{
            gap: 0.2rem !important;
        }}
        div.navbar-menu-wrapper [data-testid="stColumn"] {{
            width: fit-content !important;
            flex: 0 0 auto !important;
            min-width: 0 !important;
            padding: 0 0.4rem !important;
        }}

        /* Reset border/box langsung di elemen <button> via testid yang
           sudah dikonfirmasi -- ini selector paling pasti, tidak
           bergantung pada class Emotion yang acak/dinamis. */
        div.navbar-menu-wrapper button[data-testid="baseButton-secondary"] {{
            background-color: transparent !important;
            background: transparent !important;
            border: 0 !important;
            border-style: none !important;
            border-width: 0 !important;
            border-color: transparent !important;
            box-shadow: none !important;
            outline: none !important;
            padding: 0.3rem 0.5rem !important;
            font-weight: 600;
            font-size: 0.95rem;
            white-space: nowrap;
        }}
        div.navbar-menu-wrapper button[data-testid="baseButton-secondary"]:hover,
        div.navbar-menu-wrapper button[data-testid="baseButton-secondary"]:focus,
        div.navbar-menu-wrapper button[data-testid="baseButton-secondary"]:active,
        div.navbar-menu-wrapper button[data-testid="baseButton-secondary"]:focus:not(:active) {{
            background-color: transparent !important;
            background: transparent !important;
            border: 0 !important;
            border-style: none !important;
            box-shadow: none !important;
            outline: none !important;
            color: {COLORS['terracotta']} !important;
        }}
        div.navbar-menu-wrapper button[data-testid="baseButton-secondary"] p {{
            margin: 0;
        }}
        div.navbar-menu-wrapper button[data-testid="baseButton-secondary"]:hover p,
        div.navbar-menu-wrapper button[data-testid="baseButton-secondary"]:focus p {{
            color: {COLORS['terracotta']} !important;
        }}

        /* Warna aktif vs inactive lewat marker sibling div */
        div.navbtn-active + div[data-testid="stButton"] button,
        div.navbtn-active + div[data-testid="stButton"] button p {{
            color: {COLORS['terracotta']} !important;
            font-weight: 700;
        }}
        div.navbtn-inactive + div[data-testid="stButton"] button,
        div.navbtn-inactive + div[data-testid="stButton"] button p {{
            color: {COLORS['ink_soft']} !important;
        }}

        /* ── Navbar responsif di mobile: paksa tetap horizontal ──── */
        /* Streamlit secara default men-stack st.columns jadi vertikal
           di layar sempit (<~640px). Aturan ini menimpa perilaku itu
           KHUSUS untuk wrapper menu navbar, supaya 3 tombol tetap
           sejajar horizontal meski dibuka di HP. */
        @media (max-width: 640px) {{
            div.navbar-menu-wrapper [data-testid="stHorizontalBlock"] {{
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                gap: 0.1rem !important;
            }}
            div.navbar-menu-wrapper [data-testid="stColumn"] {{
                width: fit-content !important;
                flex: 0 0 auto !important;
                padding: 0 0.15rem !important;
            }}
            div.navbar-menu-wrapper button[data-testid="baseButton-secondary"] {{
                font-size: 0.78rem !important;
                padding: 0.2rem 0.3rem !important;
            }}
            /* Baris terluar (brand + grup menu) juga dipaksa tetap
               horizontal di mobile, supaya brand tidak terpisah jauh
               ke atas sendirian seperti pada layout default Streamlit.
               Ditarget lewat sibling selector dari marker div, karena
               st.container(key=...) TIDAK didukung di Streamlit 1.36.0. */
            div.navbar-outer-marker + [data-testid="stHorizontalBlock"] {{
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                align-items: center !important;
            }}
            div.navbar-outer-marker + [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {{
                width: auto !important;
                min-width: 0 !important;
            }}
            .navbar-brand {{
                font-size: 1.1rem !important;
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
    st.button yang di-styling ulang lewat CSS agar terlihat seperti
    link teks biasa (tanpa kotak tombol solid), warna berubah saat
    halaman tersebut sedang aktif.

    st.button dipilih (bukan <a> HTML) karena Streamlit TIDAK mendukung
    navigasi antar-halaman lewat tag HTML murni di multipage app --
    perlu komponen native Streamlit yang bisa memicu st.switch_page().

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

    # Catatan: TIDAK memakai st.container(key=...) karena parameter
    # 'key' pada st.container() belum tersedia di Streamlit 1.36.0
    # yang dipin di requirements.txt (fitur ini baru di versi lebih
    # baru). Dipakai marker div sederhana + sibling selector CSS
    # sebagai gantinya -- konsisten dengan pendekatan yang sudah
    # terbukti aman di bagian lain navbar ini.
    st.markdown('<div class="navbar-outer-marker"></div>', unsafe_allow_html=True)
    col_brand, col_menu = st.columns([3, 2.2])

    with col_brand:
        st.markdown(
            '<div class="navbar-brand" style="padding-top:0.3rem;">Tari<span>Jateng</span></div>',
            unsafe_allow_html=True,
        )

    switched_to = None
    with col_menu:
        st.markdown('<div class="navbar-menu-wrapper">', unsafe_allow_html=True)
        btn_cols = st.columns(len(pages))
        for col, page_name in zip(btn_cols, pages):
            with col:
                is_active = (page_name == active_page)
                btn_class_marker = "navbtn-active" if is_active else "navbtn-inactive"
                st.markdown(f'<div class="{btn_class_marker}">', unsafe_allow_html=True)
                if st.button(page_name, key=f"navbtn_{page_name}", type="secondary"):
                    switched_to = page_name
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr class="thin-divider" style="margin-top:0.5rem;">', unsafe_allow_html=True)

    if switched_to and switched_to != active_page:
        target_file = page_files[switched_to]
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
