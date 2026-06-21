"""
config.py
Konfigurasi terpusat untuk aplikasi Klasifikasi Kostum Tari Tradisional
Jawa Tengah. Semua path, konstanta, dan data konten katalog disimpan di
sini agar mudah diubah tanpa menyentuh logika di file lain.
"""

import os

# ─────────────────────────────────────────────────────────────────
# PATH MODEL & ASET
# ─────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model_final.h5")
MODEL_PATH_KERAS = os.path.join(MODEL_DIR, "model_final.keras")
CLASS_MAPPING_PATH = os.path.join(MODEL_DIR, "class_mapping.json")
MODEL_CONFIG_PATH = os.path.join(MODEL_DIR, "model_config.json")

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
CATALOG_IMG_DIR = os.path.join(ASSETS_DIR, "catalog")

# ─────────────────────────────────────────────────────────────────
# PARAMETER MODEL (fallback jika model_config.json tidak terbaca)
# ─────────────────────────────────────────────────────────────────
IMG_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 40.0  # % minimum sebelum dianggap "kurang yakin"

# Fallback manual jika model_config.json tidak/belum menyimpan field
# dataset total (dipakai di halaman Tentang -> kartu "Total Dataset").
# Update angka ini secara manual jika dataset training berubah, atau
# lebih baik: tambahkan field "dataset_total" ke model_config.json
# langsung dari notebook training agar selalu akurat otomatis.
FALLBACK_DATASET_TOTAL = 1335

# ─────────────────────────────────────────────────────────────────
# DETEKSI GAMBAR "TIDAK SESUAI" (di luar 5 kelas kostum tari)
# ─────────────────────────────────────────────────────────────────
# Model hanya dilatih untuk 5 kelas ini, sehingga TIDAK punya cara native
# untuk bilang "ini bukan kostum tari apapun" -- ia akan selalu memaksa
# memilih salah satu dari 5 kelas, dan softmax kadang tetap memberi
# confidence cukup tinggi ke satu kelas meski input sama sekali tidak
# relevan (mis. foto makanan/minuman). Threshold di bawah ini SENGAJA
# dibuat ketat (bukan "sedang" lagi) berdasarkan pengujian langsung:
# threshold longgar sebelumnya (45%/12%) masih meloloskan foto
# makanan/minuman sebagai salah satu kostum tari.
#
#  1. OOD_CONFIDENCE_THRESHOLD : confidence kelas teratas harus tinggi
#     (>=70%) untuk dianggap valid -- di bawah ini ditandai tidak sesuai.
#  2. OOD_MARGIN_THRESHOLD     : selisih confidence kelas #1 vs #2 juga
#     harus cukup besar -- model yang benar-benar yakin pada satu kelas
#     dari 5 yang dilatih biasanya unggul jauh dari kelas kedua.
#
# Gambar ditandai "kemungkinan tidak sesuai" jika MEMENUHI SALAH SATU
# kondisi di bawah (OR) -- confidence rendah ATAU margin tipis.
OOD_CONFIDENCE_THRESHOLD = 80.0  # % -- di bawah ini dianggap tidak sesuai
OOD_MARGIN_THRESHOLD = 20.0      # % -- selisih top-1 vs top-2 harus signifikan

# ─────────────────────────────────────────────────────────────────
# DETEKSI WAJAH DOMINAN (anti-selfie)
# ─────────────────────────────────────────────────────────────────
# Model klasifikasi tetap bisa sangat "yakin" (>90%) terhadap foto
# wajah/selfie yang sebenarnya sama sekali bukan kostum tari, karena
# model hanya dilatih membedakan 5 kelas tari satu sama lain -- bukan
# membedakan "kostum tari" vs "bukan kostum tari" secara umum. Sinyal
# confidence/margin saja tidak cukup menangkap kasus ini (ditemukan
# lewat pengujian langsung: foto selfie terdeteksi 98.6% sebagai
# salah satu kostum tari). Deteksi wajah dipakai sebagai sinyal
# TAMBAHAN yang independen dari confidence model.
FACE_AREA_THRESHOLD = 0.12  # proporsi luas wajah/luas gambar dianggap "dominan"

# ─────────────────────────────────────────────────────────────────
# DETEKSI BENDA POLOS (anti botol/piring/lampu/dll)
# ─────────────────────────────────────────────────────────────────
# Sinyal tambahan di luar deteksi wajah: benda sehari-hari yang permukaannya
# polos/halus (botol kaca, piring keramik, lampu, dsb) ditandai lewat 3
# pengukuran visual SEDERHANA (BUKAN model machine learning terpisah,
# hanya heuristik fitur citra dasar -- tetap konsisten dengan cakupan
# skripsi yang berfokus pada CNN MobileNetV2, bukan deteksi objek):
#   - edge_density     : kepadatan tepi (Canny). Kain bermotif punya
#     banyak tepi; permukaan polos jauh lebih sedikit.
#   - color_diversity   : jumlah warna dominan unik di histogram Hue.
#     Kostum tari biasanya multi-warna; benda polos sering 1-2 warna.
#   - saturation_mean   : rata-rata saturasi warna. Kain tradisional
#     umumnya saturasi tinggi (warna mencolok).
# Ketiga kondisi harus terpenuhi BERSAMAAN (AND, bukan OR) sebelum
# ditandai "likely_plain_object" -- supaya tidak terlalu agresif
# menolak foto kostum tari yang sah tapi kebetulan fotonya minim
# tekstur (misal kostum polos tanpa motif, foto agak overexposed, dst).
PLAIN_OBJECT_EDGE_THRESHOLD = 0.05        # di bawah ini dianggap "kurang bertekstur"
PLAIN_OBJECT_COLOR_THRESHOLD = 4          # di bawah ini dianggap "warna terlalu monoton"
PLAIN_OBJECT_SATURATION_THRESHOLD = 60.0  # di bawah ini dianggap "warna kurang mencolok" (skala 0-255)

# ─────────────────────────────────────────────────────────────────
# DATA KATALOG TARI
# Konten dirangkum dari BAB II.2.2.1 proposal skripsi (Fasya Maulinada,
# "Pengembangan Model CNN Menggunakan Transfer Learning untuk Klasifikasi
# Kostum Tari Tradisional Jawa Tengah", Universitas Muria Kudus, 2025).
# ─────────────────────────────────────────────────────────────────

DANCE_CATALOG = {
    "Tari_Bedhaya": {
        "nama_tampilan": "Tari Bedhaya",
        "asal": "Keraton Surakarta & Yogyakarta",
        "karakter": "Sakral & Religius",
        "warna_aksen": "#7B2D26",
        "ringkasan": (
            "Tarian sakral dan tertua yang mencerminkan kerumitan budaya "
            "keraton Surakarta dan Yogyakarta."
        ),
        "deskripsi": (
            "Tari Bedhaya merupakan sebuah tarian sakral dan tertua yang "
            "mencerminkan kerumitan budaya keraton Surakarta dan "
            "Yogyakarta. Dalam tarian ini terkandung nilai-nilai edukasi "
            "religius, sakral, dan etika kesantunan wanita keraton. "
            "Tarian ini biasanya ditarikan secara berkelompok oleh "
            "sembilan penari putri dalam suasana penuh khidmat, sebagai "
            "bagian dari ritual dan upacara penting di lingkungan "
            "keraton."
        ),
        "ciri_kostum": [
            "Kemben dan jarik batik bermotif klasik keraton",
            "Sanggul gelung tekuk dengan hiasan bunga melati",
            "Selendang panjang yang diselempangkan",
            "Warna dominan gelap dan keemasan, melambangkan kewibawaan",
        ],
        "fakta_singkat": "Dianggap sebagai salah satu tarian klasik tertua di Jawa, sarat makna spiritual.",
    },
    "Tari_Dolalak": {
        "nama_tampilan": "Tari Dolalak",
        "asal": "Purworejo, Jawa Tengah",
        "karakter": "Akulturasi Budaya & Dinamis",
        "warna_aksen": "#1F4E5F",
        "ringkasan": (
            "Warisan budaya hasil akulturasi budaya Barat dan Jawa pada "
            "zaman penjajahan Belanda."
        ),
        "deskripsi": (
            "Tari Dolalak merupakan warisan budaya dari zaman penjajahan "
            "Belanda yang merupakan hasil akulturasi budaya Barat dan "
            "Jawa. Tarian ini meniru gerak-gerik serdadu Belanda dengan "
            "diiringi musik tradisional, dan memiliki keunikan pada gerak "
            "dansa serta formasi rampak barisan. Di Kabupaten Purworejo, "
            "tarian ini telah tumbuh pesat dengan kelompok kesenian yang "
            "tersebar hampir di setiap kecamatan."
        ),
        "ciri_kostum": [
            "Seragam menyerupai pakaian militer kolonial",
            "Topi pet khas serdadu dengan hiasan rumbai",
            "Selempang dan kacamata hitam sebagai aksesori khas",
            "Warna mencolok seperti hitam, merah, dan emas",
        ],
        "fakta_singkat": "Namanya berasal dari notasi musik 'do-la-la' yang berulang dalam iringan tarinya.",
    },
    "Tari_Gambyong": {
        "nama_tampilan": "Tari Gambyong",
        "asal": "Surakarta, Jawa Tengah",
        "karakter": "Anggun & Penyambutan",
        "warna_aksen": "#A8456B",
        "ringkasan": (
            "Awalnya tari tunggal putri rakyat, kini menjadi tarian "
            "pembuka dan penyambutan tamu yang populer."
        ),
        "deskripsi": (
            "Tari Gambyong awalnya merupakan tari tunggal putri, tetapi "
            "kini sering ditarikan secara berkelompok untuk pembukaan "
            "acara, penyambutan tamu, atau pertunjukan komersial. Busana "
            "Tari Gambyong yang asli berasal dari tarian rakyat (tledhek) "
            "dan sering disesuaikan dengan permintaan konsumen, sehingga "
            "tampilannya cukup beragam namun tetap mempertahankan ciri "
            "khas keluwesannya."
        ),
        "ciri_kostum": [
            "Kemben dengan warna mencolok (hijau, merah, atau kuning keemasan)",
            "Jarik batik dengan wiron rapi",
            "Sampur (selendang) panjang sebagai properti tari utama",
            "Sanggul dengan hiasan bunga dan cunduk mentul",
        ],
        "fakta_singkat": "Sering menjadi tarian pembuka resmi acara-acara kenegaraan di Jawa Tengah.",
    },
    "Tari_Golek": {
        "nama_tampilan": "Tari Golek",
        "asal": "Yogyakarta, Jawa Tengah",
        "karakter": "Riang & Pencarian Jati Diri",
        "warna_aksen": "#C9762C",
        "ringkasan": (
            "Tarian klasik populer yang merepresentasikan remaja putri "
            "dalam masa pencarian jati diri melalui upaya berhias."
        ),
        "deskripsi": (
            "Tari Golek merupakan tarian klasik yang sangat populer, "
            "menggambarkan sosok remaja putri yang sedang dalam masa "
            "pencarian jati diri melalui upaya berhias dan mempercantik "
            "diri. Gerakannya cenderung lincah dan ekspresif, "
            "menggambarkan keceriaan serta kelembutan khas remaja putri "
            "Jawa."
        ),
        "ciri_kostum": [
            "Kemben dengan warna-warna cerah dan motif bunga",
            "Mahkota atau jamang dengan hiasan bulu/sirip warna-warni",
            "Jarik batik dipadukan dengan kain motif kontemporer",
            "Aksesori gelang dan kalung yang mencolok",
        ],
        "fakta_singkat": "Menggambarkan tema universal remaja yang sedang belajar mengenal dan merawat dirinya.",
    },
    "Tari_Srimpi": {
        "nama_tampilan": "Tari Srimpi",
        "asal": "Keraton Yogyakarta & Surakarta",
        "karakter": "Lembut & Penyambutan Resmi",
        "warna_aksen": "#3D5A40",
        "ringkasan": (
            "Tarian putri berkarakter lungguh (halus) yang ditarikan "
            "secara berkelompok, sering untuk menyambut tamu kehormatan."
        ),
        "deskripsi": (
            "Tari Srimpi merupakan tarian putri yang berkarakter lungguh "
            "(halus) dan ditarikan secara berkelompok, umumnya oleh "
            "empat penari yang melambangkan empat unsur alam. Tarian ini "
            "sering digunakan untuk menyambut tamu kehormatan di "
            "lingkungan keraton, dengan gerakan yang tenang, lembut, dan "
            "penuh kewibawaan."
        ),
        "ciri_kostum": [
            "Kemben dan jarik batik motif keraton yang serasi antar penari",
            "Sanggul gelung dengan hiasan cunduk mentul keemasan",
            "Sampur (selendang) yang digunakan dalam gerakan simetris",
            "Warna kain yang kalem dan harmonis, mencerminkan kehalusan",
        ],
        "fakta_singkat": "Biasanya ditarikan oleh empat penari yang melambangkan empat unsur: api, angin, air, bumi.",
    },
}

# Urutan tampilan default (samakan dengan urutan kelas model)
CLASS_ORDER = [
    "Tari_Bedhaya",
    "Tari_Dolalak",
    "Tari_Gambyong",
    "Tari_Golek",
    "Tari_Srimpi",
]


def get_catalog_image_path(class_key: str):
    """
    Mencari file foto untuk kelas tertentu di folder assets/catalog/.
    Mendukung beberapa ekstensi umum. Mengembalikan path string jika
    ditemukan, atau None jika belum ada foto untuk kelas itu (UI akan
    menampilkan placeholder elegan sebagai fallback).

    Penamaan file yang dicari: <class_key>.jpg / .jpeg / .png / .webp
    Contoh: assets/catalog/Tari_Bedhaya.jpg
    """
    if not os.path.isdir(CATALOG_IMG_DIR):
        return None
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        candidate = os.path.join(CATALOG_IMG_DIR, f"{class_key}{ext}")
        if os.path.exists(candidate):
            return candidate
    return None
