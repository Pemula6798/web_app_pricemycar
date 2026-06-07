# PriceMyCar — Used Car Valuation & Physical Scoring Platform

PriceMyCar is an end-to-end Machine Learning web application designed to provide transparent, data-driven, and calibrated used car price estimations in Indonesia. The system integrates a trained and tuned classical machine learning regression pipeline with a 10-factor physical vehicle condition scoring checklist to estimate a car's real-world market value.

This project was built to satisfy the requirements of the **COMP6577001 - Machine Learning Final Project** at School of Computer Science, BINUS University.

## Deployed Application
- **Hugging Face Space Live Demo**: [PriceMyCar on Hugging Face](https://huggingface.co/spaces/PyroBlizzed/PriceMyCar)
- **GitHub Repository**: [PriceMyCar Repository](https://github.com/Pemula6798/web_app_pricemycar)

---

## 1. Problem Statement & Motivation
* **Problem**: Setting fair prices for used cars is highly subjective, non-transparent, and inconsistent for both individual buyers and sellers. Important components (e.g., mileage, age, physical wear and tear) are difficult to aggregate and calculate manually.
* **Motivation**: To build a transparent, data-driven used car price estimation system. By combining a predictive machine learning model with a structured physical condition deduction checklist, we provide an objective price baseline that reflects both the vehicle's historical depreciation profile and its actual physical state.

---

## 2. Dataset & Data Preprocessing
* **Source**: [Kaggle Used Car Dataset (from CarDekho)](https://www.kaggle.com/datasets/taeefnajib/used-car-price-prediction-dataset)
* **Initial Records**: 4,340 rows, 8 columns.
* **Cleaned Records**: **4,255 rows** (exactly 85 rows removed as outliers using Percentile 1–99 thresholding on `selling_price` and `km_driven`).
* **Columns**:
  - `name`: Brand and model of the car (Categorical)
  - `year`: Manufacturing year (Numerical)
  - `selling_price`: Transaction price (Target Variable - Numerical)
  - `km_driven`: Total distance driven (Numerical)
  - `fuel`: Fuel type (Diesel, Petrol, CNG, LPG, Electric) (Categorical)
  - `seller_type`: Sales channel (Individual, Dealer, Trustmark Dealer) (Categorical)
  - `transmission`: Gearbox type (Manual, Automatic) (Categorical)
  - `owner`: Previous ownership count (First, Second, Third, Fourth & Above) (Categorical)

---

## 3. Exploratory Data Analysis (EDA) Key Insights
1. **Target Skewness**: The target variable `selling_price` is highly right-skewed (Skewness = 4.89, Kurtosis = 37.09) due to a small number of high-value luxury cars. A logarithmic transformation ($\log(1+x)$) was applied to stabilize variance and prevent the model from biasing towards mass-market budget cars.
2. **Age & Mileage Depreciation**: Car age and mileage (`km_driven`) show a clear negative correlation ($-0.50$ and $-0.19$ respectively) with the selling price.
3. **Categorical Impact**: Diesel cars and Automatic transmissions consistently command a premium resale value in the dataset. First-owner cars and dealer-listed cars also maintain higher valuations compared to multi-owner and private listings.

---

## 4. Machine Learning Problem Formulation
* **Task Type**: Supervised Regression
* **Target Variable**: $y = \log(1 + \text{selling\_price})$
* **Feature Engineering (15 Features)**:
  - Numerical: `km_driven`, `car_age`, `km_per_year`, `age_x_km` (interaction term), `brand_freq` (target frequency mapping).
  - Categorical Encodings: `owner` (Ordinal Encoding); `fuel`, `seller_type`, and `transmission` (One-Hot Encoding).
* **Cost Function**: Mean Squared Error (MSE) in log-space, which focuses on relative percentage errors:
  $$\text{MSE}_{\text{log}} = \frac{1}{n} \sum_{i=1}^n (\log(1 + y_i) - \log(1 + \hat{y}_i))^2$$
* **Inference Post-Processing**: The model output is converted back to currency using $\text{expm1}(x) = e^x - 1$, guaranteeing non-negative price outputs.

---

## 5. Model Selection, Training, & Tuning Results
The dataset was split using a **60% Train / 20% Validation / 20% Test** strategy. Six models were trained, tuned, and evaluated. Tuning utilized analytical cross-validation (`RidgeCV`, `LassoCV`) and progressive halving search (`HalvingRandomSearchCV` with 80 candidates and 5-fold CV) to optimize hyperparameters and mitigate overfitting.

### Evaluation Results Table:
| Model | Train $R^2$ | Validation $R^2$ | **Test $R^2$** | Test MAE (INR) | Test MAPE | Overfitting Gap (Train-Test) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Linear Regression (Baseline) | 0.5960 | 0.5891 | **0.5898** | 163,892 | 37.8% | 0.006 |
| Ridge Regression (Tuned) | 0.5957 | 0.5895 | **0.5892** | 163,656 | 37.7% | 0.006 |
| Lasso Regression (Tuned) | 0.5942 | 0.5890 | **0.5880** | 163,401 | 37.6% | 0.006 |
| Random Forest (Tuned) | 0.9161 | 0.7201 | **0.7797** | 109,834 | 28.0% | 0.136 |
| Gradient Boosting (Tuned) | 0.8678 | 0.7128 | **0.7649** | 117,031 | 29.9% | 0.103 |
| **HistGradientBoosting (Winner)** | **0.8613** | **0.7223** | **0.7822** | **112,033** | **27.6%** | **0.079** |

### Winner Selection Rationale:
**HistGradientBoostingRegressor** was chosen as the deployed model. It achieves the highest **Test $R^2$ (78.22%)**, the lowest **Test MAE (112,033 INR)**, the lowest **MAPE (27.6%)**, and maintains an excellent generalization profile with an **overfitting gap of only 7.9%**. Linear models underperformed due to the non-linear relationship of used car depreciation, while Random Forest showed signs of overfitting (13.6% gap).

---

## 6. System Architecture & Deployment
The application is deployed using a Flask framework inside a Docker container, achieving a **prediction latency of < 15 ms** (well below the 100 ms limit).

```text
               +-------------------------------------------+
               |             Client Browser                |
               +-------------------------------------------+
                                     |
                                     v HTTP POST (JSON)
               +-------------------------------------------+
               |             Flask App Engine              |
               +-------------------------------------------+
                                     |
             +-----------------------+-----------------------+
             |                                               |
             v                                               v
+------------------------+                      +------------------------+
|   Base Price Engine    |                      |   Physical Deductor    |
+------------------------+                      +------------------------+
| 1. Encoders & Scalers  |                      | Calculates deduction % |
| 2. HistGBR Model (pkl) |                      | based on 10 physical   |
| 3. Base Value (INR)    |                      | condition factors      |
+------------------------+                      +------------------------+
             |                                               |
             +-----------------------+-----------------------+
                                     |
                                     v
                        +--------------------------+
                        |  Calibration & Converter |
                        +--------------------------+
                        | 1. Exchange Rate (INR)   |
                        | 2. Market Multiplier     |
                        | 3. Final IDR Calculation |
                        +--------------------------+
                                     |
                                     v JSON Response
                        +--------------------------+
                        |       Result UI          |
                        +--------------------------+
```

---

## 7. Real-World Indonesian Market Calibration
Because the core model was trained on Indian market data (INR), the Flask application applies a real-time calibration module to map predictions accurately to the Indonesian market (OLX/Mobil123, June 2026):
1. **Exchange Rate**: `1 INR = Rp 187.6`
2. **Inflation & Age Offset**: +12% adjustment
3. **Calibrated Brand-Segment Multipliers**:
   - *Luxury Segment* (BMW, Mercedes-Benz, Audi, Jaguar, Land Rover): **1.15x**
   - *Premium SUV/MPV Segment* (Toyota Fortuner, Honda CR-V, Toyota Innova): **1.15x**
   - *Standard Segment* (Toyota City, Honda Jazz, HR-V, Suzuki Ertiga): **1.55x**
   - *Budget Japanese Segment* (Suzuki Karimun, Daihatsu Ayla): **1.70x**
   - *Korean & Others* (Hyundai, Kia, Ford, Nissan): **1.25x**

### Physical Condition Scoring Checklist:
The base price is adjusted based on a 10-factor checklist submitted by the user:
1. **Body Damage Severity**: Up to $-28\%$ deduction
2. **Number of Dents**: $-2\%$ per dent (Max $-15\%$)
3. **Paint Condition**: Up to $-13\%$ deduction
4. **Interior Condition**: Up to $-15\%$ deduction
5. **Accident History**: Up to $-40\%$ deduction
6. **Flood Damage**: Up to $-50\%$ deduction
7. **Engine & Mechanical**: Up to $-30\%$ deduction
8. **Tire Condition**: Up to $-5\%$ deduction
9. **Service History**: $+3\%$ bonus to $-6\%$ deduction
10. **Modifications**: Up to $-8\%$ deduction

$$\text{Final Price} = \text{Base Price} \times (1 - \text{Total Deduction Percentage})$$

---

## 8. Real User Testing Design & Results
The application was evaluated by **5 independent users** who are not members of the development team (including an automotive sales representative, a used car entrepreneur, and students).

### Quantitative Ratings (Scale 1–5):
- **Learnability** (Is the UI easy to understand?): **4.6 / 5.0**
- **System Functionality** (Did the prediction work correctly?): **4.8 / 5.0**
- **Prediction Reasonableness** (Are the price estimates logical?): **4.4 / 5.0**
- **Overall User Satisfaction**: **4.6 / 5.0**

### Qualitative Feedback Highlights:
* **What users liked**: Clean, fast, and simple user interface; support for a wide range of Indonesian car brands; the condition-scoring checklist adds realistic value reflection.
* **Areas for improvement**: Further accuracy calibration for specific low-volume local models; adding a comparison search history; displaying price ranges instead of a single point estimate.

---

## 9. Project Directory Structure
```text
web_app_pricemycar/
├── README.md                          # Master project documentation
├── evaluasi/                          # Model training & validation
│   ├── CAR_DETAILS_FROM_CAR_DEKHO.csv # Raw Dataset
│   └── evaluasi.ipynb                 # Jupyter notebook containing training code
└── web_app/                           # Deployed Flask Application
    ├── app.py                         # Flask server code with calibration engine
    ├── Dockerfile                     # Container configuration
    ├── requirements.txt               # App dependencies
    ├── best_model.pkl                 # Tuned HistGradientBoosting model
    ├── brand_freq_map.pkl             # Encoded brand frequencies
    ├── feature_columns.pkl            # Trained model columns
    ├── ordinal_encoder.pkl            # Trained ordinal encoder
    ├── static/                        # Frontend assets (CSS/JS)
    └── templates/                     # Jinja2 HTML pages
```

---

## 10. Local Setup and Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/Pemula6798/web_app_pricemycar.git
   cd web_app_pricemycar/web_app
   ```
2. Create and activate a python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the local Flask server:
   ```bash
   python app.py
   ```
5. Open your browser and access `http://127.0.0.1:5000`.
