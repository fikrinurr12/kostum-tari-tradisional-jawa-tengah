"""
app.py  —  TariJateng
Halaman Beranda: upload gambar & klasifikasi kostum tari secara real-time.

Deteksi gambar di luar cakupan (bukan kostum tari) memakai 3 lapis:
  0. Deteksi selfie (Haar Cascade, sebelum inferensi model — lihat
     utils/selfie_detector.py dan is_selfie di hasil prediksi).
  1. Model 6-kelas dengan kelas eksplisit "Non_Tari" (utama — lihat
     is_non_tari di hasil prediksi).
  2. Threshold Maximum Softmax Probability/MSP sebagai jaring pengaman
     untuk gambar di luar cakupan data latih Non_Tari (likely_out_of_scope).
"""

import time

import streamlit as st
from PIL import Image

import config
from utils import model_loader, selfie_detector, styling

st.set_page_config(
    page_title="TariJateng — Klasifikasi Kostum Tari Jawa Tengah",
    page_icon="🩰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

styling.inject_global_css()

# ── NAVBAR ────────────────────────────────────────────────────────
_switched = styling.render_navbar(active_page="Home")
if _switched:
    st.stop()

# ── HERO ──────────────────────────────────────────────────────────
st.markdown(
    '<h1 style="margin-bottom:1rem;">Kenali Warisan Budaya<br>Lewat Satu Foto.</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="lead-text" style="margin:0 auto; text-align:center;">'
    "Sistem cerdas berbasis Machine Learning untuk mengidentifikasi "
    "kostum tari tradisional Jawa Tengah secara instan.</p>",
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)

_, col_hero, _ = st.columns([0.6, 1.6, 0.6])
with col_hero:
    badges = "".join(
        f'<span class="badge">{config.DANCE_CATALOG[k]["nama_tampilan"]}</span>'
        for k in config.CLASS_ORDER
    )
    st.markdown(f'<div class="center-text">{badges}</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)

# ── MUAT MODEL ────────────────────────────────────────────────────
mapping = model_loader.load_class_mapping()
if mapping is None:
    st.error(
        "⚠️ File `class_mapping.json` tidak ditemukan di folder `models/`. "
        "Pastikan file tersebut ada sebelum melakukan klasifikasi."
    )
    st.stop()

with st.spinner("Memuat model klasifikasi..."):
    model, model_error = model_loader.load_model()

if model_error:
    st.error(f"⚠️ {model_error}")
    st.info("Kamu tetap bisa menjelajahi halaman **Katalog** di menu atas.")
    st.stop()

# ── UPLOAD & KLASIFIKASI ──────────────────────────────────────────
_, col_upload_center, _ = st.columns([0.3, 1.4, 0.3])

with col_upload_center:
    tab_upload, tab_camera = st.tabs(["📁 Upload Berkas", "📷 Ambil Foto"])

    with tab_upload:
        uploaded_from_file = st.file_uploader(
            "Pilih gambar",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="file_uploader_widget",
        )

    with tab_camera:
        st.markdown(
            '<p class="muted-text" style="text-align:center; margin-bottom:0.6rem;">'
            "Izinkan akses kamera saat diminta oleh browser, lalu tekan tombol "
            "ambil foto di bawah.</p>",
            unsafe_allow_html=True,
        )
        uploaded_from_camera = st.camera_input(
            "Ambil foto kostum tari",
            label_visibility="collapsed",
            key="camera_input_widget",
        )

    # ── Tentukan sumber gambar aktif ─────────────────────────────
    # Dua widget ini aktif berbarengan (state masing-masing tetap
    # tersimpan walau tab-nya tidak sedang dibuka), jadi kita perlu
    # menentukan mana yang PALING BARU diisi pengguna, bukan sekadar
    # "yang mana saja yang tidak kosong". Deteksinya dengan membandingkan
    # ke _last_file_key yang sudah diproses pada rerun sebelumnya —
    # sumber yang key-nya berubah dari situ berarti baru saja diisi/diganti.
    def _file_key(f):
        return f"{f.name}_{f.size}" if f is not None else None

    key_file = _file_key(uploaded_from_file)
    key_cam = _file_key(uploaded_from_camera)
    last_processed = st.session_state.get("_last_file_key")

    if key_cam and key_cam != last_processed:
        uploaded_file = uploaded_from_camera
    elif key_file and key_file != last_processed:
        uploaded_file = uploaded_from_file
    elif uploaded_from_camera is not None:
        uploaded_file = uploaded_from_camera
    elif uploaded_from_file is not None:
        uploaded_file = uploaded_from_file
    else:
        uploaded_file = None

    if uploaded_file is not None:
        file_key = f"{uploaded_file.name}_{uploaded_file.size}"

        try:
            image = Image.open(uploaded_file)
        except Exception:
            st.error("⚠️ Gambar tidak bisa dibuka. Coba file lain.")
            image = None

        if image is not None:
            st.image(image, caption=f"📁 {uploaded_file.name}", use_column_width=True)

            # ── Auto-klasifikasi jika file baru ──────────────────
            if st.session_state.get("_last_file_key") != file_key:
                st.session_state["_last_file_key"] = file_key

                with st.spinner("🔍 Memeriksa gambar..."):
                    selfie_info = selfie_detector.is_selfie(image)

                if selfie_info["is_selfie"]:
                    result = {"is_selfie": True, **selfie_info}
                else:
                    with st.spinner("🎭 Menganalisis pola visual kostum tari..."):
                        result = model_loader.predict(model, mapping, image)
                    result["is_selfie"] = False

                st.session_state["last_result"] = result
                st.session_state["last_image_caption"] = uploaded_file.name
                st.rerun()

    else:
        # File dihapus / belum dipilih — bersihkan hasil lama
        st.session_state.pop("last_result", None)
        st.session_state.pop("_last_file_key", None)

# ── TAMPILKAN HASIL ───────────────────────────────────────────────
if "last_result" not in st.session_state:
    styling.render_footer()
    st.stop()

result = st.session_state["last_result"]

st.markdown('<hr class="thin-divider">', unsafe_allow_html=True)
styling.eyebrow("Hasil Klasifikasi")

# ── LAPIS 0: Gambar terdeteksi sebagai selfie/foto wajah close-up ──
# Dicek SEBELUM inferensi model (lihat blok upload di atas), jadi kalau
# masuk sini, "result" HANYA berisi is_selfie/num_faces/largest_ratio —
# belum ada pred_class_key/confidence/margin sama sekali.
if result.get("is_selfie"):
    st.markdown(
        f"""
        <div class="result-card" style="--accent-color:{nt['warna_aksen']};">
            <div class="eyebrow" style="color:{nt['warna_aksen']};">🖼️ Hasil Deteksi</div>
            <div class="pred-title" style="color:{nt['warna_aksen']}; font-size:1.35rem;">
                Gambar ini bukan kostum tari tradisional Jawa Tengah
            </div>
            <p style="margin-bottom:0.6rem;">
                Model mengenali gambar ini sebagai <strong>bukan salah satu</strong> dari
                5 kostum tari yang dikenalinya (Bedhaya, Dolalak, Gambyong, Golek, Srimpi),
                dengan tingkat keyakinan <strong>{confidence:.1f}%</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "💡 Kalau ini seharusnya foto kostum tari, coba unggah foto yang menampilkan "
        "kostum secara penuh dan jelas, dengan pencahayaan yang cukup."
    )
    if st.button("🔄 Coba Gambar Lain", use_container_width=True, key="btn_retry_nontari"):
        del st.session_state["last_result"]
        st.rerun()
    styling.render_footer()
    st.stop()

pred_key   = result["pred_class_key"]
pred_info  = config.DANCE_CATALOG.get(pred_key, {})
accent     = pred_info.get("warna_aksen", "#8B5A2B")
confidence = result["confidence"]
margin     = result["margin"]

# ── LAPIS 1: Model secara eksplisit memprediksi kelas Non_Tari ─────
# Ditangani TERPISAH dari blok threshold di bawah (LAPIS 2) karena ini
# prediksi asli dari model (bisa sangat yakin), bukan sekadar kondisi
# "ragu-ragu" — jadi pesannya dibuat lebih tegas & informatif, bukan
# nada "kurang yakin".
if result.get("is_non_tari"):
    nt = config.NON_TARI_INFO
    st.markdown(
        f"""
        <div class="result-card" style="--accent-color:{nt['warna_aksen']};">
            <div class="eyebrow" style="color:{nt['warna_aksen']};">🖼️ Hasil Deteksi</div>
            <div class="pred-title" style="color:{nt['warna_aksen']}; font-size:1.35rem;">
                Gambar ini bukan kostum tari tradisional Jawa Tengah
            </div>
            <p style="margin-bottom:0.6rem;">
                Model mengenali gambar ini sebagai <strong>bukan salah satu</strong> dari
                5 kostum tari yang dikenalinya (Bedhaya, Dolalak, Gambyong, Golek, Srimpi),
                dengan tingkat keyakinan <strong>{confidence:.1f}%</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "💡 Kalau ini seharusnya foto kostum tari, coba unggah foto yang menampilkan "
        "kostum secara penuh dan jelas, dengan pencahayaan yang cukup."
    )
    if st.button("🔄 Coba Gambar Lain", use_container_width=True, key="btn_retry_nontari"):
        del st.session_state["last_result"]
        st.rerun()
    styling.render_footer()
    st.stop()

# ── LAPIS 2: Threshold MSP (jaring pengaman untuk kasus di luar cakupan
# data latih Non_Tari — lihat config.py) ────────────────────────────
if result.get("likely_out_of_scope"):
    reason = result.get("reason", "")

    if reason == "low_confidence":
        title_ood = "Sistem kurang yakin — gambar mungkin bukan salah satu dari 5 kostum tari"
        body_ood  = (
            f"Tingkat keyakinan model hanya <strong>{confidence:.1f}%</strong>, "
            f"di bawah ambang batas minimum ({config.OOD_CONFIDENCE_THRESHOLD:.0f}%). "
            "Model tidak menemukan pola visual yang cukup kuat untuk mencocokkan "
            "gambar ini dengan salah satu kostum tari yang dikenalinya."
        )
    elif reason == "low_margin":
        title_ood = "Sistem tidak dapat membedakan — gambar memiliki kemiripan dengan beberapa kostum sekaligus"
        body_ood  = (
            f"Selisih keyakinan antara dua pilihan teratas hanya <strong>{margin:.1f}%</strong>, "
            f"di bawah ambang batas ({config.OOD_MARGIN_THRESHOLD:.0f}%). "
            "Model tidak dapat memilih satu kelas dengan keyakinan yang memadai."
        )
    else:
        title_ood = "Gambar tidak dikenali sebagai salah satu dari 5 kostum tari"
        body_ood  = (
            f"Tingkat keyakinan model (<strong>{confidence:.1f}%</strong>) dan "
            f"selisih antar kelas (<strong>{margin:.1f}%</strong>) keduanya berada "
            "di bawah ambang batas yang ditetapkan. Gambar mungkin bukan kostum "
            "tari Jawa Tengah yang dilatihkan pada sistem ini."
        )

    st.markdown(
        f"""
        <div class="result-card" style="--accent-color:#A8456B;">
            <div class="eyebrow" style="color:#A8456B;">⚠️ Gambar Tidak Dikenali</div>
            <div class="pred-title" style="color:#A8456B; font-size:1.35rem;">{title_ood}</div>
            <p style="margin-bottom:0.6rem;">{body_ood}</p>
            <p class="muted-text" style="margin-bottom:0;">
                Tebakan terdekat: <strong>{pred_info.get('nama_tampilan', result['pred_label'])}</strong>
                ({confidence:.1f}%) — diabaikan karena berada di bawah ambang batas keyakinan.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "💡 Pastikan foto menampilkan kostum tari secara penuh dan jelas. "
        "Sistem ini hanya mengenali: Tari Bedhaya, Tari Dolalak, Tari Gambyong, "
        "Tari Golek, dan Tari Srimpi."
    )
    if st.button("🔄 Coba Gambar Lain", use_container_width=True):
        del st.session_state["last_result"]
        st.rerun()
    styling.render_footer()
    st.stop()

# ── Hasil klasifikasi normal ──────────────────────────────────────
if confidence < config.CONFIDENCE_THRESHOLD:
    st.warning(
        f"Model kurang yakin dengan prediksi ini (keyakinan {confidence:.1f}%). "
        "Pertimbangkan untuk mengunggah foto yang lebih jelas."
    )

st.markdown(
    f"""
    <div class="result-card" style="--accent-color:{accent};">
        <div class="eyebrow" style="color:{accent};">Jenis Kostum Terdeteksi</div>
        <div class="pred-title" style="color:{accent};">
            {pred_info.get('nama_tampilan', result['pred_label'])}
        </div>
        <p class="muted-text" style="margin-bottom:0.8rem;">
            Asal: {pred_info.get('asal', '-')} &nbsp;·&nbsp;
            Karakter: {pred_info.get('karakter', '-')}
        </p>
        <div style="display:flex; justify-content:space-between;
                    font-size:0.85rem; margin-bottom:0.2rem;">
            <span>Tingkat Keyakinan</span>
            <span style="font-weight:700;">{confidence:.1f}%</span>
        </div>
        <div class="confidence-bar-track">
            <div class="confidence-bar-fill"
                 style="width:{confidence:.1f}%; background-color:{accent};"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Lihat rincian probabilitas semua kelas"):
    for cls_key, prob in result["all_probabilities"].items():
        if cls_key == config.NEGATIVE_CLASS_KEY:
            cls_info = config.NON_TARI_INFO
        else:
            cls_info = config.DANCE_CATALOG.get(cls_key, {})
        label      = cls_info.get("nama_tampilan", cls_key)
        cls_accent = cls_info.get("warna_aksen", "#8B5A2B")
        st.markdown(
            f"""
            <div style="display:flex; justify-content:space-between;
                        font-size:0.9rem; margin-bottom:0.15rem;">
                <span>{label}</span>
                <span style="font-weight:600;">{prob:.1f}%</span>
            </div>
            <div class="confidence-bar-track" style="height:6px; margin-bottom:0.6rem;">
                <div class="confidence-bar-fill"
                     style="width:{prob:.1f}%; background-color:{cls_accent};"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

col_a, col_b = st.columns(2)
with col_a:
    if st.button("📖 Lihat Detail Lengkap di Katalog", use_container_width=True):
        st.session_state["catalog_focus"] = pred_key
        st.switch_page("pages/1_Katalog.py")
with col_b:
    if st.button("🔄 Klasifikasikan Gambar Lain", use_container_width=True):
        del st.session_state["last_result"]
        st.rerun()

styling.render_footer()
