"""
config.py  —  TariJateng
Konfigurasi terpusat: path, konstanta model, dan data katalog tari.
Semua nilai dapat diubah di sini tanpa menyentuh logika halaman lain.
"""

import os

# ── PATH ─────────────────────────────────────────────────────────
BASE_DIR          = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR         = os.path.join(BASE_DIR, "models")
MODEL_PATH        = os.path.join(MODEL_DIR, "model_final.h5")
MODEL_PATH_KERAS  = os.path.join(MODEL_DIR, "model_final.keras")
CLASS_MAPPING_PATH = os.path.join(MODEL_DIR, "class_mapping.json")
MODEL_CONFIG_PATH  = os.path.join(MODEL_DIR, "model_config.json")
ASSETS_DIR        = os.path.join(BASE_DIR, "assets")
CATALOG_IMG_DIR   = os.path.join(ASSETS_DIR, "catalog")

# ── PARAMETER MODEL ───────────────────────────────────────────────
IMG_SIZE               = (224, 224)
FALLBACK_DATASET_TOTAL = 1335

# Peringatan ringan "kurang yakin" (warning, bukan penolakan)
CONFIDENCE_THRESHOLD   = 40.0   # %

# ── DETEKSI GAMBAR DI LUAR CAKUPAN (Out-of-Distribution / OOD) ──
#
# Model CNN 5-kelas dengan fungsi aktivasi softmax SELALU memilih
# salah satu dari 5 kelas meski menerima gambar yang sama sekali
# bukan kostum tari. Untuk mendeteksi kondisi ini tanpa model atau
# library tambahan, digunakan dua sinyal langsung dari output softmax:
#
# 1. Confidence (Maximum Softmax Probability):
#    Ketika model mengenali objek yang dilatihnya, probabilitas kelas
#    teratas cenderung tinggi. Untuk gambar asing, model "ragu" dan
#    menyebarkan probabilitas ke semua kelas sehingga nilai maksimum
#    menjadi rendah. Pendekatan ini sesuai prinsip Maximum Softmax
#    Probability (MSP) untuk deteksi OOD (Hendrycks & Gimpel, 2017).
#
# 2. Margin (selisih prob_top1 - prob_top2):
#    Model yang benar-benar yakin akan menghasilkan gap besar antara
#    kelas terbaik dan kedua terbaik. Gap tipis mengindikasikan model
#    dipaksa memilih tanpa keyakinan nyata.
#
# Gambar ditandai di luar cakupan jika SALAH SATU kondisi terpenuhi:
#   confidence < OOD_CONFIDENCE_THRESHOLD  ATAU
#   margin     < OOD_MARGIN_THRESHOLD
#
# Threshold ditentukan empiris dari distribusi confidence score
# pada data uji (nilai percentile ke-5 data kostum asli yang benar).
# ─────────────────────────────────────────────────────────────────
OOD_CONFIDENCE_THRESHOLD = 60.0   # % — di bawah ini dianggap tidak sesuai
OOD_MARGIN_THRESHOLD     = 15.0   # % — selisih top-1 vs top-2 minimum

# ── DATA KATALOG TARI ─────────────────────────────────────────────
DANCE_CATALOG = {
    "Tari_Bedhaya": {
        "nama_tampilan": "Tari Bedhaya",
        "asal"         : "Keraton Surakarta & Yogyakarta",
        "karakter"     : "Sakral & Religius",
        "warna_aksen"  : "#7B2D26",
        "ringkasan"    : (
            "Tarian sakral dan tertua yang mencerminkan kerumitan budaya "
            "keraton Surakarta dan Yogyakarta."
        ),
        "deskripsi"    : (
            "Tari Bedhaya merupakan sebuah tarian sakral dan tertua yang "
            "mencerminkan kerumitan budaya keraton Surakarta dan Yogyakarta. "
            "Dalam tarian ini terkandung nilai-nilai edukasi religius, sakral, "
            "dan etika kesantunan wanita keraton. Tarian ini biasanya ditarikan "
            "secara berkelompok oleh sembilan penari putri dalam suasana penuh "
            "khidmat, sebagai bagian dari ritual dan upacara penting di lingkungan "
            "keraton."
        ),
        "ciri_kostum"  : [
            "Kemben dan jarik batik bermotif klasik keraton",
            "Sanggul gelung tekuk dengan hiasan bunga melati",
            "Selendang panjang yang diselempangkan",
            "Warna dominan gelap dan keemasan, melambangkan kewibawaan",
        ],
        "fakta_singkat": "Dianggap sebagai salah satu tarian klasik tertua di Jawa, sarat makna spiritual.",
    },
    "Tari_Dolalak": {
        "nama_tampilan": "Tari Dolalak",
        "asal"         : "Purworejo, Jawa Tengah",
        "karakter"     : "Akulturasi Budaya & Dinamis",
        "warna_aksen"  : "#1F4E5F",
        "ringkasan"    : (
            "Warisan budaya hasil akulturasi budaya Barat dan Jawa pada "
            "zaman penjajahan Belanda."
        ),
        "deskripsi"    : (
            "Tari Dolalak merupakan warisan budaya dari zaman penjajahan "
            "Belanda yang merupakan hasil akulturasi budaya Barat dan Jawa. "
            "Tarian ini meniru gerak-gerik serdadu Belanda dengan diiringi "
            "musik tradisional, dan memiliki keunikan pada gerak dansa serta "
            "formasi rampak barisan. Di Kabupaten Purworejo, tarian ini telah "
            "tumbuh pesat dengan kelompok kesenian yang tersebar hampir di "
            "setiap kecamatan."
        ),
        "ciri_kostum"  : [
            "Seragam menyerupai pakaian militer kolonial Belanda",
            "Topi pet khas serdadu dengan hiasan rumbai warna-warni",
            "Motif batik hitam-putih pada bawahan",
            "Warna dominan hitam, putih, dan merah yang kontras",
        ],
        "fakta_singkat": "Nama 'Dolalak' berasal dari not musik do-la-la yang sering dimainkan serdadu Belanda.",
    },
    "Tari_Gambyong": {
        "nama_tampilan": "Tari Gambyong",
        "asal"         : "Surakarta, Jawa Tengah",
        "karakter"     : "Anggun & Elegan",
        "warna_aksen"  : "#5C3D1E",
        "ringkasan"    : (
            "Tarian putri yang berasal dari tarian rakyat (tledhek), kini "
            "sering ditarikan untuk pembukaan acara dan penyambutan tamu."
        ),
        "deskripsi"    : (
            "Tari Gambyong awalnya merupakan tari tunggal putri yang berasal "
            "dari tarian rakyat (tledhek). Kini sering ditarikan secara "
            "berkelompok untuk pembukaan acara, penyambutan tamu, atau "
            "pertunjukan komersial. Busana Tari Gambyong sering disesuaikan "
            "dengan permintaan konsumen, menjadikannya salah satu tarian paling adaptif."
        ),
        "ciri_kostum"  : [
            "Kemben berwarna cerah (kuning, hijau, atau merah muda)",
            "Jarik batik dengan motif khas Surakarta",
            "Selendang panjang warna senada",
            "Aksesoris kepala bunga melati dan hiasan rambut tradisional",
        ],
        "fakta_singkat": "Tari Gambyong menjadi inspirasi lahirnya berbagai tarian Jawa lainnya.",
    },
    "Tari_Golek": {
        "nama_tampilan": "Tari Golek",
        "asal"         : "Yogyakarta, Jawa Tengah",
        "karakter"     : "Feminim & Periang",
        "warna_aksen"  : "#2E5D34",
        "ringkasan"    : (
            "Tarian klasik yang merepresentasikan remaja putri yang sedang "
            "dalam masa pencarian jati diri melalui upaya berhias."
        ),
        "deskripsi"    : (
            "Tari Golek merupakan tarian klasik yang sangat populer yang "
            "merepresentasikan remaja putri yang sedang dalam masa pencarian "
            "jati diri melalui upaya berhias. Gerakannya menggambarkan keceriaan "
            "dan kelembutan seorang gadis muda, dengan kostum yang penuh warna "
            "dan aksesori kepala yang mencolok."
        ),
        "ciri_kostum"  : [
            "Kemben dan jarik batik dengan warna cerah dan beragam",
            "Mahkota/jamang berornamen emas yang mencolok",
            "Selendang warna-warni yang digunakan saat menari",
            "Aksesoris dada dan gelang yang mewah",
        ],
        "fakta_singkat": "Tari Golek Menak terinspirasi dari tokoh dalam Serat Menak karya Sultan Hamengkubuwono I.",
    },
    "Tari_Srimpi": {
        "nama_tampilan": "Tari Srimpi",
        "asal"         : "Keraton Surakarta & Yogyakarta",
        "karakter"     : "Halus & Anggun",
        "warna_aksen"  : "#4A2C6E",
        "ringkasan"    : (
            "Tarian putri keraton berkarakter lungguh (halus) yang ditarikan "
            "secara kelompok, sering digunakan untuk menyambut tamu kehormatan."
        ),
        "deskripsi"    : (
            "Tari Srimpi merupakan tarian putri yang berkarakter lungguh (halus) "
            "dan ditarikan secara kelompok. Sering digunakan untuk menyambut tamu "
            "kehormatan dalam upacara adat dan perayaan budaya. Tarian ini memiliki "
            "nilai sakral dan keanggunan yang tinggi, mencerminkan budaya keraton "
            "yang kaya tradisi."
        ),
        "ciri_kostum"  : [
            "Kemben dan jarik batik khas keraton",
            "Sanggul gelung dengan hiasan bunga melati dan payet",
            "Selendang panjang bermotif emas",
            "Warna dominan hijau, merah, dan emas yang melambangkan kemuliaan",
        ],
        "fakta_singkat": "Srimpi berasal dari kata 'impi' yang berarti impian — menggambarkan keanggunan tak duniawi.",
    },
}

CLASS_ORDER = [
    "Tari_Bedhaya",
    "Tari_Dolalak",
    "Tari_Gambyong",
    "Tari_Golek",
    "Tari_Srimpi",
]


def get_catalog_image_path(class_key: str):
    """Mengembalikan path gambar katalog jika file ada, None jika tidak."""
    for ext in (".jpg", ".jpeg", ".png"):
        path = os.path.join(CATALOG_IMG_DIR, class_key + ext)
        if os.path.exists(path):
            return path
    return None
