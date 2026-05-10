# 🚗 PriceMyCar — Panduan Lengkap Instalasi & Penggunaan Lokal

Selamat datang di **PriceMyCar**, sebuah aplikasi web premium berbasis sistem estimasi harga mobil bekas pintar yang memadukan **Algoritma Analisis Harga Historis** dengan **Sistem Penilaian Kondisi Fisik Kendaraan (10-Factor Condition Evaluation System)**.

Aplikasi ini dirancang dengan antarmuka modern yang sepenuhnya responsif, sehingga tampilannya sangat dinamis, premium, dan rapi baik saat dibuka melalui **PC/Laptop** maupun **HP (Mobile)**.

---

## ⚡ Fitur Utama Aplikasi
1. **Algoritma Estimasi Harga Empiris**: Menghitung harga dasar mobil secara objektif berdasarkan pola data transaksi pasar mobil bekas.
2. **Sistem Koreksi Kondisi Fisik**: Melakukan kalibrasi harga yang presisi berdasarkan 10 kriteria kondisi fisik kendaraan secara nyata (seperti kerusakan bodi, riwayat banjir, kondisi mesin, interior, dll.).
3. **Desain Antarmuka Premium & Responsif**: Menggunakan struktur grid modern dan efek transisi halus yang otomatis menyesuaikan ukuran layar perangkat (PC, Tablet, dan Smartphone).
4. **Konversi Mata Uang Rupiah (IDR)**: Sistem konversi otomatis dengan visualisasi simbol mata uang Rp yang presisi dan rapi.

---

## 📂 Struktur Proyek Aplikasi
```text
web_app_pricemycar/
└── web_app/
    ├── app.py                     ← Controller Utama & Logika Penghitungan Estimasi
    ├── requirements.txt           ← Daftar Modul & Package Python yang Dibutuhkan
    ├── best_model.pkl             ← Basis Data Pola Harga Estimasi (Serialized)
    ├── ordinal_encoder.pkl        ← Modul Pemetaan Data Kategori
    ├── brand_freq_map.pkl         ← Modul Frekuensi Brand Mobil
    ├── feature_columns.pkl        ← Modul Struktur Kolom Data
    ├── templates/                 ← Halaman Antarmuka (HTML/Jinja2)
    │   ├── base.html              ← Layout Utama (Navbar & Footer Responsif)
    │   ├── index.html             ← Landing Page (Halaman Utama)
    │   ├── predict.html           ← Formulir Input Spesifikasi & Live Preview Penilaian
    │   ├── result.html            ← Hasil Estimasi Akhir & Rincian Koreksi Nilai
    │   ├── data_insights.html     ← Dashboard Analisis Statistik Pasar
    │   ├── model_info.html        ← Detail Penjelasan Cara Kerja Algoritma
    │   └── about.html             ← Profil Tim Pengembang
    └── static/                    ← File Aset Statis Pendukung
        ├── css/
        │   └── style.css          ← Desain Web & Media Queries (Layout Responsif HP/PC)
        └── js/
            ├── main.js            ← Script Fungsionalitas Navigasi
            └── predict.js         ← Script Live preview pengurangan harga di form
```

---

## 💻 Panduan Menjalankan Aplikasi Secara Lokal (Local Setup)

Ikuti langkah-langkah mudah berikut untuk menginstal dan menjalankan aplikasi PriceMyCar langsung di komputer atau laptop Anda:

### 1. Buka Terminal & Masuk ke Folder Web App
Buka terminal (CMD / PowerShell / Bash) lalu arahkan ke direktori `web_app`:
```bash
cd web_app
```

### 2. Buat & Aktifkan Virtual Environment (Sangat Direkomendasikan)
Gunakan Virtual Environment agar instalasi package rapi dan tidak mengganggu python sistem komputer Anda:

*   **Untuk Pengguna Windows (Command Prompt / PowerShell):**
    ```powershell
    python -m venv venv
    venv\Scripts\activate
    ```

*   **Untuk Pengguna Mac / Linux (Terminal):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Install Seluruh Dependensi Aplikasi
Jalankan perintah berikut untuk menginstal semua modul yang diperlukan aplikasi:
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
Jalankan server lokal aplikasi menggunakan perintah:
```bash
python app.py
```

### 5. Buka Aplikasi di Browser
Setelah server berjalan, buka browser kesayangan Anda dan akses alamat berikut:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📊 Sistem Penilaian & Koreksi Kondisi Kendaraan (10-Factor)

Aplikasi ini mengintegrasikan logika penilaian kondisi fisik yang objektif. Harga akhir mobil diperoleh dari perhitungan berikut:

```text
Harga Akhir = Harga Estimasi Dasar × (1 - Total Persentase Pengurangan)
```

Sistem akan mengevaluasi **10 Faktor Fisik** berikut untuk mengukur persentase pengurangan nilai jual kendaraan secara adil:

| No | Faktor Kondisi | Pilihan Kondisi Pengguna | Dampak Terhadap Harga |
|----|----------------|--------------------------|-----------------------|
| 1  | **Tingkat Kerusakan Bodi** | Aman / Goresan Ringan / Penyok / Parah | 0% s/d -28% |
| 2  | **Jumlah Penyok (Dents)** | Batasan input: 0 s/d 20 penyok | -2% per penyok (Max -15%) |
| 3  | **Kondisi Cat Mobil** | Sangat Baik / Cukup Baik / Pudar / Rusak | 0% s/d -13% |
| 4  | **Kondisi Interior & Dasbor** | Sangat Bersih / Bersih / Kotor / Sobek | 0% s/d -15% |
| 5  | **Riwayat Kecelakaan** | Tidak Pernah / Ringan / Sedang / Parah | 0% s/d -40% |
| 6  | **Riwayat Terendam Banjir** | Tidak Pernah / Setinggi Roda / Setinggi Dasbor | 0% s/d -50% |
| 7  | **Kondisi Mesin & Transmisi** | Prima / Normal / Kasar / Butuh Servis Besar | 0% s/d -30% |
| 8  | **Kondisi Ban Mobil** | Tebal & Baru / Normal / Botak | 0% s/d -5% |
| 9  | **Riwayat Servis Bengkel** | Rutin Resmi / Rutin Biasa / Jarang Servis | **+3% Bonus Nilai** s/d -6% |
| 10 | **Modifikasi Kendaraan** | Standar Pabrik / Ringan / Berat (Permanen) | 0% s/d -8% |
