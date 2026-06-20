"""
utils/styling.py
CSS kustom terpusat untuk seluruh aplikasi.

Arah desain: minimalis modern dengan aksen warna terinspirasi kain
batik/jarik Jawa Tengah (bukan template biru-ungu default), tipografi
serif untuk judul (mengesankan keraton/tradisi) dipadukan sans-serif
yang bersih untuk isi.
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────────
# TOKEN DESAIN
# ─────────────────────────────────────────────────────────────────
COLORS = {
    "ink": "#2A1F1A",          # teks utama, coklat tua kehitaman (warna batik tulis)
    "paper": "#FAF6EF",        # latar utama, krem gading
    "paper_alt": "#F1EADA",    # latar sekunder/kartu
    "sogan": "#8B5A2B",        # coklat soga, aksen utama (warna khas batik sogan)
    "sogan_dark": "#6B431E",
    "indigo": "#2E4756",       # biru tua kain lurik, aksen sekunder
    "terracotta": "#A8456B",   # aksen hangat untuk highlight/error ringan
    "sage": "#5C6B47",         # hijau lumut, aksen sukses
    "border": "#DCD2BC",
    "muted": "#7A6F5E",
}

FONT_DISPLAY = "'Lora', Georgia, serif"
FONT_BODY = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif"


def inject_global_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: {FONT_BODY};
        }}

        /* ── Latar & kontainer utama ───────────────────────────── */
        .stApp {{
            background-color: {COLORS['paper']};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {COLORS['paper_alt']};
            border-right: 1px solid {COLORS['border']};
        }}

        /* ── Tipografi ──────────────────────────────────────────── */
        h1, h2, h3 {{
            font-family: {FONT_DISPLAY};
            color: {COLORS['ink']};
            font-weight: 600;
            letter-spacing: -0.01em;
        }}

        h1 {{
            font-size: 2.2rem !important;
            border-bottom: 3px solid {COLORS['sogan']};
            padding-bottom: 0.5rem;
            display: inline-block;
        }}

        p, span, div, label {{
            color: {COLORS['ink']};
        }}

        .muted-text {{
            color: {COLORS['muted']};
            font-size: 0.92rem;
        }}

        /* ── Eyebrow label (kecil di atas judul) ───────────────── */
        .eyebrow {{
            font-family: {FONT_BODY};
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: {COLORS['sogan']};
            margin-bottom: 0.3rem;
        }}

        /* ── Tombol ─────────────────────────────────────────────── */
        .stButton > button, .stDownloadButton > button {{
            background-color: {COLORS['sogan']};
            color: {COLORS['paper']};
            border: none;
            border-radius: 6px;
            padding: 0.55rem 1.4rem;
            font-weight: 600;
            font-family: {FONT_BODY};
            transition: background-color 0.15s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover {{
            background-color: {COLORS['sogan_dark']};
            color: {COLORS['paper']};
        }}

        /* ── Kartu generik ──────────────────────────────────────── */
        .card {{
            background-color: white;
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1rem;
        }}

        /* ── Kartu hasil klasifikasi (signature element) ───────── */
        .result-card {{
            background: linear-gradient(135deg, {COLORS['paper_alt']} 0%, white 100%);
            border: 1px solid {COLORS['border']};
            border-left: 6px solid var(--accent-color, {COLORS['sogan']});
            border-radius: 10px;
            padding: 1.8rem 2rem;
            margin: 1rem 0 1.5rem 0;
        }}

        .result-card .pred-title {{
            font-family: {FONT_DISPLAY};
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0.2rem 0 0.3rem 0;
        }}

        .confidence-bar-track {{
            background-color: {COLORS['border']};
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

        /* ── Badge kecil ────────────────────────────────────────── */
        .badge {{
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.2rem 0.65rem;
            border-radius: 999px;
            background-color: {COLORS['paper_alt']};
            color: {COLORS['sogan_dark']};
            border: 1px solid {COLORS['border']};
            margin-right: 0.4rem;
        }}

        /* ── Kartu katalog ──────────────────────────────────────── */
        .catalog-card {{
            background-color: white;
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            overflow: hidden;
            margin-bottom: 1.2rem;
            transition: box-shadow 0.2s ease;
        }}
        .catalog-card:hover {{
            box-shadow: 0 4px 18px rgba(42, 31, 26, 0.08);
        }}
        .catalog-card-header {{
            padding: 1rem 1.3rem 0.8rem 1.3rem;
            border-bottom: 1px solid {COLORS['border']};
        }}
        .catalog-card-body {{
            padding: 1rem 1.3rem 1.3rem 1.3rem;
        }}

        /* ── Divider tipis ──────────────────────────────────────── */
        .thin-divider {{
            border: none;
            border-top: 1px solid {COLORS['border']};
            margin: 1.2rem 0;
        }}

        /* ── Sembunyikan elemen default Streamlit yang kurang perlu */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* ── Upload box kustom ──────────────────────────────────── */
        [data-testid="stFileUploader"] {{
            background-color: white;
            border: 2px dashed {COLORS['border']};
            border-radius: 10px;
            padding: 0.6rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def eyebrow(text: str):
    st.markdown(f'<div class="eyebrow">{text}</div>', unsafe_allow_html=True)
