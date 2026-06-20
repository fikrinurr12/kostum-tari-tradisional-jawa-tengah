# 🩰 Klasifikasi Kostum Tari Tradisional Jawa Tengah

Aplikasi web untuk mengklasifikasikan jenis kostum tari tradisional Jawa
Tengah dari foto, menggunakan model CNN (MobileNetV2 + Transfer
Learning). Dibangun dengan Streamlit, sebagai bagian dari skripsi:

> **Pengembangan Model CNN Menggunakan Transfer Learning untuk
> Klasifikasi Kostum Tari Tradisional Jawa Tengah**
> Fasya Maulinada (NIM. 202251155) — Universitas Muria Kudus, 2025

Lima kelas yang dikenali: **Tari Bedhaya, Tari Dolalak, Tari Gambyong,
Tari Golek, dan Tari Srimpi**.

---

## 📁 Struktur Project

```
.
├── app.py                      # Halaman utama: beranda + upload & klasifikasi
├── config.py                   # Konfigurasi path & konten katalog tari
├── pages/
│   ├── 1_Katalog.py            # Halaman katalog seluruh jenis tari
│   └── 2_Tentang.py            # Halaman metodologi & metrik evaluasi model
├── utils/
│   ├── model_loader.py         # Loading model & logika prediksi
│   └── styling.py              # CSS kustom terpusat
├── models/                     # ⚠️ Letakkan file model di sini (lihat bawah)
│   └── PLACE_MODEL_FILES_HERE.txt
├── .streamlit/
│   └── config.toml             # Tema warna native Streamlit
├── requirements.txt            # Dependency Python (versi sudah dipin)
├── runtime.txt                 # Pin Python 3.11 (WAJIB untuk TensorFlow 2.15)
└── README.md
```

---

## 🚀 Langkah Setup Sebelum Deploy

### 1. Siapkan file model dari hasil training

Dari notebook training di Google Colab, download 3 file ini dari Google
Drive (`/content/drive/MyDrive/Skripsi_Fasya/output/`):

| File sumber (di Drive) | Lokasi tujuan (di project ini) |
|---|---|
| `models/model_final.h5` | `models/model_final.h5` |
| `class_mapping.json` | `models/class_mapping.json` |
| `model_config.json` | `models/model_config.json` |

Letakkan ketiganya di folder `models/` pada project ini.

### 2. ⚠️ Cek ukuran file model SEBELUM push ke GitHub

GitHub menolak file di atas 100 MB, dan akan memperingatkan untuk file
di atas 50 MB. Model MobileNetV2 custom biasanya berukuran 15–40 MB
sehingga umumnya aman, tapi **selalu cek dulu**:

```bash
# Di terminal lokal, setelah file model ada di folder models/
ls -lh models/model_final.h5
```

Jika ukurannya **di atas 50 MB**, gunakan [Git LFS](https://git-lfs.com/)
sebelum push:

```bash
git lfs install
git lfs track "models/*.h5"
git add .gitattributes
```

### 3. Jalankan & test secara lokal (opsional tapi disarankan)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Buka `http://localhost:8501` di browser, coba unggah satu gambar test
untuk memastikan model termuat dan prediksi berjalan sebelum deploy.

---

## ☁️ Deploy ke Streamlit Community Cloud via GitHub

1. **Push project ini ke repository GitHub baru** (public atau private):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: aplikasi klasifikasi kostum tari"
   git branch -M main
   git remote add origin https://github.com/USERNAME/NAMA_REPO.git
   git push -u origin main
   ```

2. Buka **[share.streamlit.io](https://share.streamlit.io)**, login
   dengan akun GitHub.

3. Klik **"New app"**, pilih repository, branch `main`, dan file utama
   `app.py`.

4. Klik **Deploy**. Streamlit Cloud akan otomatis membaca:
   - `runtime.txt` → memakai Python 3.11
   - `requirements.txt` → menginstall `tensorflow-cpu`, `streamlit`,
     `numpy`, `pillow` dengan versi yang sudah dipin
   - `.streamlit/config.toml` → menerapkan tema warna kustom

5. Tunggu proses build (biasanya 2–5 menit untuk instalasi
   `tensorflow-cpu`). Jika berhasil, aplikasi langsung bisa diakses
   lewat URL publik yang diberikan.

---

## 🛡️ Mengapa Tidak Ada Konflik Library Saat Deploy

Beberapa keputusan teknis di project ini secara khusus dirancang untuk
menghindari masalah deploy yang umum terjadi:

- **`tensorflow-cpu` bukan `tensorflow` penuh** — Streamlit Cloud hanya
  punya CPU, jadi versi CPU-only ini lebih ringan diinstall dan tidak
  mencoba mencari driver GPU yang tidak ada.
- **`runtime.txt` pin ke Python 3.11** — `tensorflow-cpu==2.15.0` hanya
  punya wheel resmi untuk Python 3.9–3.11. Tanpa pin ini, Streamlit
  Cloud bisa memakai Python 3.12/3.13 dan instalasi TensorFlow akan
  gagal total.
- **Versi `numpy==1.26.4`** — sudah diverifikasi berada dalam rentang
  yang disyaratkan TensorFlow 2.15 (`numpy>=1.23.5,<2.0.0`), sehingga
  pip/uv resolver tidak akan menolak kombinasi versi ini.
- **Model dimuat dengan `compile=False`** (lihat `utils/model_loader.py`)
  — menghindari error langka terkait custom metric objects saat versi
  runtime TensorFlow sedikit berbeda dari versi training di Colab.
- **`st.cache_resource`** pada fungsi loading model — model hanya
  dimuat sekali ke memori per sesi server, bukan setiap kali pengguna
  mengunggah gambar baru.

---

## 🔧 Troubleshooting Umum

| Gejala | Kemungkinan Sebab | Solusi |
|---|---|---|
| `ModuleNotFoundError: No module named 'tensorflow'` | `requirements.txt` tidak terbaca / typo nama file | Pastikan nama file tepat `requirements.txt` di root repo |
| Build gagal di tahap install TensorFlow | `runtime.txt` tidak terbaca, Python versi salah | Pastikan isi `runtime.txt` hanya `3.11` tanpa karakter lain |
| `File model tidak ditemukan di folder models/` | File model belum di-push / nama file salah | Cek nama file persis `model_final.h5` di `models/` |
| Push ke GitHub ditolak / lambat sekali | File model >100MB tanpa Git LFS | Setup Git LFS (lihat langkah 2 di atas) |
| App lambat saat pertama dibuka | Cold start + download dependency besar (`tensorflow-cpu`) | Normal untuk free tier, akan lebih cepat di kunjungan berikutnya |

---

## 📊 Tentang Model

- **Arsitektur**: MobileNetV2 (pretrained ImageNet) + Custom Dense Head
- **Metode**: Transfer Learning 2 fase (Feature Extraction → Fine-Tuning)
- **Input**: Gambar 224×224 piksel, RGB
- **Output**: 5 kelas kostum tari dengan skor probabilitas (Softmax)

Detail lengkap metodologi, hyperparameter, dan hasil evaluasi tersedia
di halaman **"Tentang"** pada aplikasi setelah model berhasil dimuat.
