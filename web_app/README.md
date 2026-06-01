---
title: PriceMyCar
emoji: 🚗
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🚗 PriceMyCar — Complete Setup & Usage Guide

Welcome to **PriceMyCar**, a premium web application featuring an intelligent used car valuation system. It combines an **Empirical Price Estimation Model** with a **10-Factor Physical Condition Evaluation System**.

The app features a modern, fully responsive user interface designed to look premium and run smoothly on both **Desktop** and **Mobile** devices.

---

## ⚡ Key Features
1. **Empirical Pricing Algorithm**: Automatically estimates the base car value based on historical sales transaction data.
2. **Physical Condition Calibration**: Dynamically adjusts the base price using a 10-factor scoring system (body damage, paint, interior, accidents, flood history, etc.).
3. **Premium & Responsive UI**: Uses a clean layout grid and smooth transitions optimized for all screen sizes.
4. **Indonesian Rupiah (IDR) Conversion**: Integrates seamless currency rendering and local pricing adjustments.

---

## 💻 Local Setup Guide

Follow these steps to run PriceMyCar on your local machine:

### 1. Open Terminal and Enter Web App Directory
Navigate to the `web_app` directory:
```bash
cd web_app
```

### 2. Create and Activate Virtual Environment (Recommended)
Set up a clean environment for python packages:

*   **Windows (Command Prompt / PowerShell):**
    ```powershell
    python -m venv venv
    venv\Scripts\activate
    ```

*   **Mac / Linux (Terminal):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Install Dependencies
Run the command below to install required python packages:
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Start the local web server:
```bash
python app.py
```

### 5. Open in Your Browser
Access the running application:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📊 10-Factor Vehicle Condition Scoring System

The final car value is calculated by applying deductions based on the physical condition of the car:

```text
Final Price = Base ML Price × (1 - Total Deduction Percentage)
```

The system evaluates **10 Physical Factors** to determine the total deduction:

| No | Condition Factor | User Selection Choices | Impact on Price |
|----|------------------|------------------------|-----------------|
| 1  | **Body Damage Severity** | None / Minor Scratches / Moderate Dents / Severe Damage | 0% to -28% |
| 2  | **Number of Dents** | Input range: 0 to 20 dents | -2% per dent (Max -15%) |
| 3  | **Paint Condition** | Excellent / Good / Fair (Faded) / Poor (Peeling) | 0% to -13% |
| 4  | **Interior Condition** | Excellent / Good / Fair (Stained) / Poor (Torn) | 0% to -15% |
| 5  | **Accident History** | None / Minor / Moderate / Major (Total Loss) | 0% to -40% |
| 6  | **Flood Damage** | None / Minor (Carpet only) / Severe (Engine bay) | 0% to -50% |
| 7  | **Engine & Mechanical** | Excellent / Good / Fair (Minor Issues) / Poor (Needs Overhaul) | 0% to -30% |
| 8  | **Tire Condition** | Good (>50% tread) / Worn (20-50%) / Bald | 0% to -5% |
| 9  | **Service History** | Complete Records / Partial / None | **+3% Bonus** to -6% |
| 10 | **Modifications** | Stock / Minor Cosmetic / Major Cosmetic / Performance / Non-Reversible | 0% to -8% |

---

## 🇮🇩 Indonesian Market Adjustments & 2026 Inflation

Since the base Machine Learning model was trained on historical Indian market data (CarDekho dataset in INR), we apply custom scaling to ensure predictions match the **Indonesian used car market in 2026**:

### 1. Price Conversion Formula
```text
Base Rupiah Price = (Model Prediction in INR) × 2026 Exchange Rate × Market Multiplier
Final Price = Base Rupiah Price × (1 - Total Physical Deduction)
```

### 2. Adjustment Parameters (June 2026)
*   **Base Exchange Rate (INR to IDR)**: `1 INR = Rp 187.6` (reflecting current currency rates).
*   **Rupiah Depreciation & Used Car Inflation**: A **+12% (1.12x)** adjustment is integrated into the multipliers to account for inflation in 2026.
*   **Combined Market Multipliers**:
    Applied to offset local luxury tax (PPnBM), BBN-KB, import duties, and brand demand in Indonesia:
    
    | Brand Category | Multiplier | Description & Examples |
    |----------------|------------|------------------------|
    | **Luxury Brands** | **1.95x** | Mercedes-Benz, BMW, Audi, Jaguar, Land Rover. Accounts for high luxury tax & CBU import duties. |
    | **Popular Indonesian Brands** | **1.60x** | Toyota, Honda, Daihatsu, Suzuki, Mitsubishi. Strong resale value & brand demand. |
    | **Other Brands** | **1.45x** | Chevrolet, Ford, Hyundai, Nissan, Renault, Datsun, etc. |

### 3. Valuation Verification Sources
Market multipliers are cross-referenced and calibrated against three major automotive portals:
1.  **OLX Indonesia** (olx.co.id) - Private seller listings.
2.  **Mobil123.com** - Showrooms and professional dealers.
3.  **GridOto Pricelist** - Frequently updated automotive pricing index.

---

## ⚠️ Model Support Validation (Unregistered Models)

The system automatically checks if the brand and model inputted are supported:
*   **Supported Models**: Popular models mapped to the training database (e.g. Avanza, Brio, Xpander, Fortuner, Jazz). Predictions have high confidence.
*   **Unregistered Models**: If you input a model not in our database (e.g. "Wuling Almaz", "Toyota Raize"), the system performs a general segment approximation based on year, transmission, fuel type, and mileage.
    *   **Disclaimer Banner**: A prominent yellow **Warning** banner will be displayed at the top of the results page to inform the user that the accuracy of the prediction is limited.
