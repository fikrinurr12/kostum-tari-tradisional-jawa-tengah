# TariJateng — Sistem Klasifikasi Kostum Tari Tradisional Jawa Tengah

Sistem klasifikasi berbasis CNN MobileNetV2 + Transfer Learning untuk mengidentifikasi
lima jenis kostum tari tradisional Jawa Tengah: Tari Bedhaya, Tari Dolalak,
Tari Gambyong, Tari Golek, dan Tari Srimpi.

## Struktur Proyek

```
├── app.py                  # Halaman Beranda (upload + klasifikasi)
├── config.py               # Konfigurasi terpusat
├── requirements.txt        # Dependensi Python
├── runtime.txt             # Versi Python untuk deployment
├── models/
│   ├── model_final.h5      # Model terlatih (letakkan di sini)
│   ├── class_mapping.json  # Pemetaan kelas
│   └── model_config.json   # Konfigurasi model
├── pages/
│   ├── 1_Katalog.py        # Halaman Katalog
│   ├── 2_Tentang.py        # Halaman Tentang
│   └── 3_Detail_Tari.py    # Halaman Detail Tari
├── utils/
│   ├── model_loader.py     # Loading model dan prediksi (dengan deteksi OOD via MSP)
│   ├── selfie_detector.py  # Deteksi selfie via Haar Cascade (OpenCV)
│   └── styling.py          # CSS kustom terpusat
└── assets/
    └── catalog/            # Gambar katalog (Tari_Bedhaya.jpg, dll.)
```

## Menjalankan Aplikasi

1. Letakkan model (`model_final.h5`) di folder `models/`
2. Install dependensi: `pip install -r requirements.txt`
3. Jalankan: `streamlit run app.py`

## Deteksi Gambar Di Luar Cakupan

- **Selfie (lapis 0)** — Haar Cascade (OpenCV) mendeteksi wajah; jika wajah
  terbesar >= 15% dari luas gambar, ditolak sebagai selfie sebelum model
  klasifikasi dijalankan. Threshold: `SELFIE_FACE_AREA_THRESHOLD` di `config.py`.
- **Non-tari (lapis 1)** — Model 6-kelas dengan kelas eksplisit `Non_Tari`.
- **MSP (lapis 2)** — Jika `confidence < 60%` ATAU `margin_top1_top2 < 15%`
  → gambar tidak dikenali. Threshold: `OOD_CONFIDENCE_THRESHOLD`,
  `OOD_MARGIN_THRESHOLD` di `config.py`.
