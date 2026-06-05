---
title: PriceMyCar
emoji: 🚗
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# PriceMyCar

PriceMyCar is a web app to estimate used car prices in Indonesia. It uses a machine learning model to estimate the base price and adjusts it based on a 10-factor physical condition checklist.

## Features
- **Price Estimation**: Estimates base car value based on historical sales data.
- **Physical Condition Scoring**: Adjusts the base price using 10 physical factors (body damage, paint, interior, accidents, flood history, etc.).
- **Responsive UI**: Simple UI that works on both desktop and mobile.
- **Indonesian Market Adjustments**: Converts the model's base currency (INR) to IDR with local inflation and brand-specific adjustments.

## Local Setup
1. Navigate to this directory:
   ```bash
   cd web_app
   ```
2. Set up a virtual environment:
   - On Windows:
     ```powershell
     python -m venv venv
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Pricing & Condition Scoring
The final price is calculated as:
```text
Final Price = Base Price * (1 - Total Deduction Percentage)
```

The system uses 10 factors to calculate the deduction percentage:
1. Body Damage Severity: 0% to -28%
2. Number of Dents: -2% per dent (Max -15%)
3. Paint Condition: 0% to -13%
4. Interior Condition: 0% to -15%
5. Accident History: 0% to -40%
6. Flood Damage: 0% to -50%
7. Engine & Mechanical: 0% to -30%
8. Tire Condition: 0% to -5%
9. Service History: +3% bonus to -6% deduction
10. Modifications: 0% to -8%

## Indonesian Market Adjustments
Since the base model was trained on Indian market data (in INR), we adjust it for the Indonesian market:
- **Exchange Rate**: `1 INR = Rp 187.6`
- **Inflation/Depreciation**: +12% adjustment
- **Market Multipliers**:
  - Luxury Brands (Mercedes, BMW, etc.): 1.95x
  - Popular Brands (Toyota, Honda, Daihatsu, Suzuki, Mitsubishi): 1.60x
  - Other Brands: 1.45x
Prices are calibrated against listings on OLX Indonesia, Mobil123, and GridOto.

## Model Validation
If a user inputs a brand/model that is not in the database, the system will perform a general segment approximation. A warning banner will be displayed on the result page to indicate that the prediction is an approximation.
