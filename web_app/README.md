# 🚗 PriceMyCar — Complete Setup Guide

## Struktur Proyek

```
pricemycar/
├── app.py                     ← Flask backend + Condition Penalty System
├── requirements.txt
├── best_model.pkl             ← dari notebook (joblib.dump)
├── ordinal_encoder.pkl
├── brand_freq_map.pkl
├── feature_columns.pkl
├── templates/
│   ├── base.html              ← Layout utama (navbar, footer)
│   ├── index.html             ← Landing page
│   ├── predict.html           ← Form prediksi + condition factors
│   ├── result.html            ← Hasil prediksi
│   ├── data_insights.html     ← Dashboard chart
│   ├── model_info.html        ← Under the hood
│   └── about.html             ← About page
└── static/
    ├── css/style.css
    └── js/
        ├── main.js
        └── predict.js         ← Live penalty preview JS
```

---

## Langkah 1 — Jalankan Notebook Dulu

Buka `Car_Prediction_Fixed.ipynb` dan run semua cell sampai selesai.
Cell terakhir akan meng-export 4 file:

```
best_model.pkl
ordinal_encoder.pkl
brand_freq_map.pkl        ← PENTING: ini baru di versi fixed
feature_columns.pkl
```

Semua file `.pkl` ini harus ada di folder yang sama dengan `app.py`.

---

## Langkah 2 — Setup Python Environment

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Windows)
venv\Scripts\activate

# Aktifkan (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Langkah 3 — Susun Folder

```
pricemycar/
├── app.py
├── requirements.txt
├── best_model.pkl            ← copy dari output notebook
├── ordinal_encoder.pkl       ← copy dari output notebook
├── brand_freq_map.pkl        ← copy dari output notebook
├── feature_columns.pkl       ← copy dari output notebook
├── templates/                ← copy semua file .html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        ├── main.js
        └── predict.js
```

---

## Langkah 4 — Jalankan Flask

```bash
# Mode development (auto-reload)
python app.py

# Atau pakai Flask CLI
flask --app app run --debug
```

Buka browser: **http://localhost:5000**

---

## Langkah 5 — Test Semua Route

| URL | Halaman |
|-----|---------|
| `/` | Landing page |
| `/predict` | Form prediksi |
| `/data-insights` | Market dashboard |
| `/model-info` | Under the hood |
| `/about` | About page |
| `/api/predict` | JSON API (POST) |

Test API via curl:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Toyota",
    "model": "Innova",
    "year": 2019,
    "mileage": 45000,
    "fuel_type": "Diesel",
    "transmission": "Manual",
    "owner": "First Owner",
    "seller_type": "Individual",
    "body_damage_severity": "1",
    "dent_count": "2",
    "paint_condition": "good",
    "interior_condition": "good",
    "accident_history": "none",
    "flood_damage": "none",
    "engine_condition": "excellent",
    "tire_condition": "good",
    "service_history": "complete",
    "modification_status": "stock"
  }'
```

---

## Condition Penalty System (Saran Dosen)

### Cara Kerja

```
Final Price = ML Base Price × (1 - total_penalty)
```

Model ML memprediksi harga dari fitur dataset (brand, mileage, dll).
Kemudian `calculate_condition_penalty()` menghitung total deduction
dari 10 faktor kondisi fisik yang **tidak ada di dataset**.

### 10 Faktor Kondisi

| Faktor | Opsi | Deduction |
|--------|------|-----------|
| **Body Damage Severity** | None / Scratches / Dents / Severe | 0% → -28% |
| **Dent Count** | 0–20 | -2% per dent, max -15% |
| **Paint Condition** | Excellent → Poor | 0% → -13% |
| **Interior Condition** | Excellent → Poor | 0% → -15% |
| **Accident History** | None → Major | 0% → -40% |
| **Flood Damage** | None → Severe | 0% → -50% |
| **Engine & Mechanical** | Excellent → Poor | 0% → -30% |
| **Tire Condition** | Good → Bald | 0% → -5% |
| **Service History** | Complete → None | **+3% bonus** → -6% |
| **Modifications** | Stock → Non-reversible | 0% → -8% |

### Contoh Kalkulasi

```
Base ML Price: ₹450,000

+ Minor scratches:     -4%   = -₹18,000
+ 3 dents:             -6%   = -₹27,000
+ Fair paint:          -6%   = -₹27,000
+ Good interior:       -2%   = -₹9,000
+ No accident:          0%
+ No flood:             0%
+ Good engine:         -3%   = -₹13,500
+ Good tires:           0%
+ Partial service:      0%
+ Stock:                0%
────────────────────────────────────────
Total penalty:        -21%   = -₹94,500
Final Price:          ₹355,500
```

### Basis Penelitian

Nilai penalty didasarkan pada:
- **NADA Used Car Guide** depreciation tables (USA market)
- **CarGurus Price Analysis** — damage impact study 2023
- **iSeeCars.com** — flood damage resale value research
- **Carfax** — accident history value impact reports

Untuk dataset India (CarDekho), values bisa disesuaikan dengan survei pasar lokal.

---

## Common Errors & Fix

| Error | Penyebab | Fix |
|-------|----------|-----|
| `FileNotFoundError: best_model.pkl` | .pkl belum di-export | Run notebook sampai cell terakhir |
| `KeyError: column_name` | Kolom OHE mismatch | `reindex` sudah ada di kode, cek versi sklearn |
| `ValueError: shape mismatch` | `feature_columns.pkl` berbeda versi | Hapus semua .pkl, re-run notebook |
| Template not found | Struktur folder salah | Pastikan `templates/` di direktori yang sama dengan `app.py` |

---

## Deployment (Optional — untuk presentasi)

```bash
# Install gunicorn
pip install gunicorn

# Run production server
gunicorn -w 4 app:app

# Atau pakai Railway/Render (gratis):
# 1. Push ke GitHub
# 2. Connect repo ke Railway/Render
# 3. Set environment variable SECRET_KEY
# 4. Deploy
```
