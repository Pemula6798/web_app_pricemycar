# 🚗 PriceMyCar — Complete Setup & Deployment Guide

Selamat datang di **PriceMyCar**, aplikasi web prediksi harga mobil bekas berbasis Machine Learning (Gradient Boosting Regressor) yang dikombinasikan dengan **10-Factor Condition Penalty System** (Saran Dosen).

Aplikasi ini dirancang sepenuhnya responsif, sehingga tampilannya sangat cantik dan rapi baik saat dibuka melalui **PC/Laptop** maupun **HP (Mobile)**.

---

## ⚡ Fitur Utama
1. **Machine Learning Core**: Memprediksi harga dasar mobil berdasarkan data latih transaksi nyata (CarDekho) menggunakan algoritma ensemble **Gradient Boosting**.
2. **Condition Adjustment System**: Penyesuaian harga realistik berdasarkan 10 faktor kondisi fisik mobil (kerusakan bodi, riwayat banjir, mesin, dll.) sesuai masukan dosen.
3. **100% Responsive Design**: Tampilan antarmuka premium yang dinamis dan proporsional di PC, Tablet, dan Smartphone.
4. **Localization (IDR)**: Konversi nilai otomatis dari Rupee (INR) ke **Rupiah (IDR)** dengan visual simbol mata uang Rp yang akurat.

---

## 📂 Struktur Proyek di GitHub
```text
web_app_pricemycar/
└── web_app/
    ├── app.py                     ← Flask Backend & Engine Perhitungan
    ├── requirements.txt           ← Daftar Package (Termasuk Gunicorn untuk Cloud)
    ├── best_model.pkl             ← Model Machine Learning (Trained)
    ├── ordinal_encoder.pkl        ← Preprocessing Encoder
    ├── brand_freq_map.pkl         ← Map Frekuensi Brand Mobil
    ├── feature_columns.pkl        ← Kolom Fitur Model
    ├── templates/                 ← Halaman Antarmuka (HTML/Jinja2)
    │   ├── base.html              ← Layout Utama (Navbar & Footer)
    │   ├── index.html             ← Landing Page
    │   ├── predict.html           ← Formulir Prediksi & Live Preview Penalty
    │   ├── result.html            ← Hasil Prediksi & Rekomendasi
    │   ├── data_insights.html     ← Dashboard Analisis Pasar
    │   ├── model_info.html        ← Detail Teknis Algoritma AI
    │   └── about.html             ← Profil Tim (Student @ BINUS)
    └── static/                    ← File Aset Statis
        ├── css/
        │   └── style.css          ← Desain Web + Media Queries (Responsive)
        └── js/
            ├── main.js
            └── predict.js         ← Script Live preview penalty di form
```

---

## 💻 Versi 1: Cara Menjalankan secara Lokal (Local Setup)

Untuk menjalankan dan menguji aplikasi ini di komputer/laptop Anda sendiri:

### 1. Buka Terminal & Masuk ke Folder Web App
Buka terminal (CMD / PowerShell / Bash) lalu navigasikan ke folder `web_app`:
```bash
cd web_app
```

### 2. Buat & Aktifkan Virtual Environment (Opsional tapi Direkomendasikan)
**Windows (Command Prompt / PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Mac / Linux (Terminal):**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Semua Dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Server Flask Lokal
```bash
python app.py
```

### 5. Akses Website
Buka browser Anda dan kunjungi:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## ☁️ Versi 2: Cara Menjalankan di Cloud secara GRATIS (Render Cloud)

Aplikasi ini siap dideploy ke **Render** agar bisa diakses oleh siapa saja di internet secara online. 

> [!TIP]
> **Fakta Menarik Paket Gratis Render:**
> Layanan gratis Render **tidak memiliki masa kedaluwarsa** (tidak akan mati setelah beberapa hari). Website Anda akan online selamanya secara gratis!
> *Catatan:* Jika tidak ada pengunjung selama 15 menit, server Render akan tidur (spin down). Jika ada pengunjung baru masuk, server butuh waktu ~40-50 detik untuk bangun otomatis (cold start). Setelah bangun, website berjalan normal kembali.

### Langkah-langkah Deploy ke Render:

1. Buat akun gratis di **[Render](https://render.com/)** menggunakan akun GitHub Anda.
2. Di Dashboard Render, klik **New +** -> **Web Service**.
3. Hubungkan repository GitHub Anda yang berisi project `web_app_pricemycar`.
4. Isi konfigurasi berikut di halaman Render:
   * **Name**: `pricemycar` *(bebas)*
   * **Region**: `Singapore` *(paling dekat dengan Indonesia)*
   * **Root Directory**: `web_app` *(PENTING! Karena file `app.py` kita berada di dalam subfolder `web_app`)*
   * **Language**: `Python`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app`
   * **Plan**: `Free`
5. Klik **Deploy Web Service** di bagian bawah.

Tunggu waktu kompilasi 2-3 menit. Setelah selesai, Render akan memberikan tautan publik gratis seperti `https://pricemycar.onrender.com` yang siap diakses di laptop maupun HP teman-teman dan dosen Anda! 🎉
