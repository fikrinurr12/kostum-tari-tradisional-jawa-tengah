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
│   └── styling.py          # CSS kustom terpusat
└── assets/
    └── catalog/            # Gambar katalog (Tari_Bedhaya.jpg, dll.)
```

## Menjalankan Aplikasi

1. Letakkan model (`model_final.h5`) di folder `models/`
2. Install dependensi: `pip install -r requirements.txt`
3. Jalankan: `streamlit run app.py`

## Deteksi Gambar Di Luar Cakupan

Menggunakan metode Maximum Softmax Probability (MSP):
- Jika `confidence < 60%` ATAU `margin_top1_top2 < 15%` → gambar tidak dikenali
- Threshold dapat disesuaikan di `config.py` (OOD_CONFIDENCE_THRESHOLD, OOD_MARGIN_THRESHOLD)
