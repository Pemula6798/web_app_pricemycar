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

## ☁️ Versi 2: Cara Menjalankan di Cloud secara GRATIS (TANPA KARTU KREDIT)

Karena Render sekarang memerlukan verifikasi kartu kredit di beberapa wilayah, berikut adalah **dua alternatif hosting cloud gratis terbaik yang 100% tidak memerlukan kartu kredit**:

---

### Opsi A: Hugging Face Spaces (Sangat Direkomendasikan & Modern)

[Hugging Face](https://huggingface.co/) adalah platform AI terbesar di dunia. Mereka menyediakan layanan **Spaces** gratis untuk menjalankan aplikasi Python/Docker selamanya tanpa meminta kartu kredit sama sekali!

Saya sudah membuatkan file **`Dockerfile`** khusus di folder `web_app` agar aplikasi Anda siap dijalankan di Hugging Face.

#### Langkah-langkah Deploy di Hugging Face Spaces:
1. Daftar akun gratis di **[Hugging Face](https://huggingface.co/join)** (Tidak perlu verifikasi kartu kredit).
2. Di halaman utama, klik profil Anda di kanan atas -> **New Space**.
3. Isi konfigurasi berikut:
   * **Space name**: `pricemycar` *(bebas)*
   * **License**: `mit` *(bebas)*
   * **Select the Space SDK**: Pilih **Docker** *(PENTING! Jangan pilih Streamlit atau Gradio)*
   * **Docker template**: Pilih **Blank**
   * **Space hardware**: Pilih **Cpu basic · Free** (ini gratis selamanya!)
   * **Visibility**: **Public** (agar dosen/teman bisa buka)
4. Klik **Create Space**.
5. Di halaman selanjutnya, pilih tab **Files** -> klik **+ Add file** -> **Upload files**.
6. Seret/upload seluruh file dan folder dari dalam folder `web_app` Anda (termasuk folder `templates`, `static`, file `.pkl`, `requirements.txt`, dan `Dockerfile`).
7. Klik **Commit changes to main** di bagian bawah.

Hugging Face akan otomatis merakit Docker container Anda selama 1-2 menit. Begitu statusnya berubah menjadi **Running** hijau, website Anda resmi online dan bisa diakses lewat menu **App** di atas! 🎉

---

### Opsi B: PythonAnywhere (Klasik, Mudah & Tanpa Git)

[PythonAnywhere](https://www.pythonanywhere.com/) sangat terkenal untuk menghosting web Flask/Django pemula secara gratis dan mudah tanpa kartu kredit.

#### Langkah-langkah Deploy di PythonAnywhere:
1. Daftar akun gratis di **[PythonAnywhere](https://www.pythonanywhere.com/registration/register/beginner/)** (Pilih tipe akun **Create a Beginner account**).
2. Masuk ke tab **Files** di dashboard Anda, lalu buat folder baru bernama `pricemycar`.
3. Unggah seluruh isi file dari folder `web_app` Anda ke sana (bisa menggunakan fitur upload file di web UI mereka).
4. Buka tab **Consoles** -> jalankan **Bash Console**, lalu buat virtual environment dan pasang dependensi:
   ```bash
   mkvirtualenv pricemycar_env --python=/usr/bin/python3.10
   pip install -r requirements.txt
   ```
5. Masuk ke tab **Web** -> Klik **Add a new web app**:
   * Pilih manual configuration.
   * Pilih versi Python (misal `Python 3.10`).
6. Di halaman pengaturan web app PythonAnywhere, sesuaikan:
   * **Code -> Source code**: `/home/username_anda/pricemycar`
   * **Virtualenv -> Path**: `/home/username_anda/.virtualenvs/pricemycar_env`
7. Edit file **WSGI configuration file** (ada link-nya di tab Web tersebut) dan ubah isinya agar mengarah ke Flask app Anda:
   ```python
   import sys
   path = '/home/username_anda/pricemycar'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
8. Klik **Reload Web App** di bagian atas halaman Web. Website Anda sekarang aktif di alamat `http://username_anda.pythonanywhere.com`! 🎉

