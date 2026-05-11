"""
PriceMyCar - Flask Backend
=============================================================
Routes:
  GET  /                    -> Landing page
  GET  /predict             -> Predict form
  POST /predict             -> Run prediction -> redirect to result
  GET  /result/<id>         -> Prediction result page
  GET  /data-insights       -> Market insights dashboard
  GET  /model-info          -> Under the hood page
  GET  /about               -> About page
  POST /api/predict         -> JSON API endpoint (for AJAX)

  Condition Adjustment System -> calculate_condition_penalty()
  Factors: body damage, dents, paint, interior, accident,
           flood, engine, tires, service history, mods
"""

import os, uuid, json
import numpy as np
import pandas as pd
import joblib
from flask import (Flask, render_template, request,
                   redirect, url_for, session, jsonify)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pricemycar-dev-secret')

# =============================================================
# Model Loading (lazy - loaded once on first predict request)
# =============================================================
_model         = None
_encoder       = None
_brand_freq    = None
_feature_cols  = None

def load_artifacts():
    global _model, _encoder, _brand_freq, _feature_cols
    if _model is None:
        _model        = joblib.load('best_model.pkl')
        _encoder      = joblib.load('ordinal_encoder.pkl')
        _brand_freq   = joblib.load('brand_freq_map.pkl')
        _feature_cols = joblib.load('feature_columns.pkl')


# =============================================================
# Condition Penalty System
# 
# =============================================================
CONDITION_PENALTIES = {
    # Body / Physical Damage
    # Severity level: 0=none, 1=minor scratches, 2=moderate dents, 3=severe
    'body_damage_severity': {
        0: 0.00,   # No damage
        1: 0.04,   # Minor scratches / scuffs
        2: 0.12,   # Moderate dents (visible, not structural)
        3: 0.28,   # Severe damage / structural deformation
    },
    # Number of dents beyond the severity level (each extra dent ~2%, cap 15%)
    'dent_count_penalty_per_unit': 0.02,
    'dent_count_max_penalty': 0.15,

    # Paint Condition
    'paint_condition': {
        'excellent': 0.00,
        'good':      0.02,
        'fair':      0.06,   # Fading, minor oxidation
        'poor':      0.13,   # Peeling, heavy oxidation
    },

    # Interior Condition
    'interior_condition': {
        'excellent': 0.00,
        'good':      0.02,
        'fair':      0.07,   # Stains, worn fabric/leather
        'poor':      0.15,   # Torn seats, damaged dashboard
    },

    # Accident History
    'accident_history': {
        'none':       0.00,
        'minor':      0.08,   # Minor accident, properly repaired
        'moderate':   0.20,   # Moderate - airbag deployed / frame checked
        'major':      0.40,   # Major accident / total-loss history
    },

    # Flood / Water Damage
    # Even "repaired" flood damage carries long-term electrical risk
    'flood_damage': {
        'none':     0.00,
        'minor':    0.20,    # Carpet/interior only, dried out
        'severe':   0.50,    # Engine bay / electrical affected
    },

    # Engine & Mechanical
    'engine_condition': {
        'excellent': 0.00,
        'good':      0.03,
        'fair':      0.10,   # Minor issues - needs attention
        'poor':      0.30,   # Major repair needed
    },

    # Tire Condition
    'tire_condition': {
        'good':     0.00,    # >50% tread remaining
        'worn':     0.03,    # 20–50% tread
        'bald':     0.05,    # Needs immediate replacement
    },

    # Service / Maintenance History
    'service_history': {
        'complete':  -0.03,  # Complete records = value BONUS
        'partial':   0.00,
        'none':      0.06,   # No records = buyers discount it
    },

    # Modifications
    # Non-stock mods reduce market pool (not every buyer wants them)
    'modification_status': {
        'stock':           0.00,
        'cosmetic_minor':  0.02,  # Tint, stickers - minor
        'cosmetic_major':  0.05,  # Body kit, paint wrap
        'performance':     0.04,  # Voids warranty concern
        'non_reversible':  0.08,  # Cut chassis, etc.
    },
}


def calculate_condition_penalty(form_data: dict) -> dict:
    """
    Calculate total condition adjustment penalty.

    Returns:
        {
          'penalty_multiplier': float,   # 0–1, multiply onto ML price
          'final_multiplier':   float,   # 1 - penalty_multiplier
          'breakdown': {factor: {'label', 'penalty_pct', 'penalty_amount'}},
          'total_penalty_pct':  float,
        }
    """
    breakdown = {}
    total_penalty = 0.0

    # Helper: clamp
    def clamp(v, lo, hi): return max(lo, min(hi, v))

    # 1. Body damage severity
    sev = int(form_data.get('body_damage_severity', 0))
    p = CONDITION_PENALTIES['body_damage_severity'].get(sev, 0)
    breakdown['body_damage'] = {
        'label': ['No Damage', 'Minor Scratches', 'Moderate Dents', 'Severe Damage'][sev],
        'penalty_pct': p * 100
    }
    total_penalty += p

    # 2. Dent count extra
    dent_count = clamp(int(form_data.get('dent_count', 0)), 0, 20)
    dent_extra = clamp(
        dent_count * CONDITION_PENALTIES['dent_count_penalty_per_unit'],
        0,
        CONDITION_PENALTIES['dent_count_max_penalty']
    )
    if dent_count > 0:
        breakdown['dent_count'] = {
            'label': f'{dent_count} dent(s)',
            'penalty_pct': round(dent_extra * 100, 1)
        }
    total_penalty += dent_extra

    # 3. Paint condition
    paint = form_data.get('paint_condition', 'good')
    p = CONDITION_PENALTIES['paint_condition'].get(paint, 0)
    breakdown['paint'] = {'label': paint.title(), 'penalty_pct': p * 100}
    total_penalty += p

    # 4. Interior condition
    interior = form_data.get('interior_condition', 'good')
    p = CONDITION_PENALTIES['interior_condition'].get(interior, 0)
    breakdown['interior'] = {'label': interior.title(), 'penalty_pct': p * 100}
    total_penalty += p

    # 5. Accident history
    accident = form_data.get('accident_history', 'none')
    p = CONDITION_PENALTIES['accident_history'].get(accident, 0)
    breakdown['accident'] = {'label': accident.replace('_', ' ').title(), 'penalty_pct': p * 100}
    total_penalty += p

    # 6. Flood damage
    flood = form_data.get('flood_damage', 'none')
    p = CONDITION_PENALTIES['flood_damage'].get(flood, 0)
    breakdown['flood'] = {'label': flood.title(), 'penalty_pct': p * 100}
    total_penalty += p

    # 7. Engine condition
    engine = form_data.get('engine_condition', 'good')
    p = CONDITION_PENALTIES['engine_condition'].get(engine, 0)
    breakdown['engine'] = {'label': engine.title(), 'penalty_pct': p * 100}
    total_penalty += p

    # 8. Tire condition
    tires = form_data.get('tire_condition', 'good')
    p = CONDITION_PENALTIES['tire_condition'].get(tires, 0)
    breakdown['tires'] = {'label': tires.title(), 'penalty_pct': p * 100}
    total_penalty += p

    # 9. Service history (can be negative = bonus)
    service = form_data.get('service_history', 'partial')
    p = CONDITION_PENALTIES['service_history'].get(service, 0)
    breakdown['service'] = {
        'label': service.replace('_', ' ').title(),
        'penalty_pct': p * 100
    }
    total_penalty += p

    # 10. Modifications
    mods = form_data.get('modification_status', 'stock')
    p = CONDITION_PENALTIES['modification_status'].get(mods, 0)
    breakdown['modifications'] = {
        'label': mods.replace('_', ' ').title(),
        'penalty_pct': p * 100
    }
    total_penalty += p

    # Cap total penalty at 90% (car still has scrap value)
    total_penalty = clamp(total_penalty, -0.05, 0.90)  # allow up to 5% bonus

    return {
        'penalty_multiplier': total_penalty,
        'final_multiplier':   1.0 - total_penalty,
        'breakdown':          breakdown,
        'total_penalty_pct':  round(total_penalty * 100, 1),
    }


# =============================================================
# ML Prediction
# =============================================================
def predict_price(form_data: dict) -> dict:
    """
    Run ML prediction then apply condition penalty.
    Returns full prediction dict.
    """
    load_artifacts()

    orig_brand = form_data.get('brand', '').strip()
    orig_model = form_data.get('model', '').strip()
    year       = int(form_data.get('year', 2020))
    km         = float(form_data.get('mileage', 50000))
    fuel       = form_data.get('fuel_type', 'Petrol')
    trans      = form_data.get('transmission', 'Manual')
    seller     = form_data.get('seller_type', 'Individual')
    owner      = form_data.get('owner', 'First Owner')

    # Indonesian Car Mapping System
    brand   = orig_brand
    model_n = orig_model
    input_key = f"{brand.lower()} {model_n.lower()}".strip()
    
    INDONESIAN_CAR_MAP = {
        'toyota avanza': ('Maruti', 'Ertiga'),
        'toyota xenia': ('Maruti', 'Ertiga'),
        'toyota calya': ('Maruti', 'Wagon'),
        'toyota agya': ('Maruti', 'Alto'),
        'toyota rush': ('Ford', 'EcoSport'),
        'toyota yaris': ('Hyundai', 'i20'),
        'toyota vios': ('Hyundai', 'Verna'),
        'toyota fortuner': ('Toyota', 'Fortuner'),
        'toyota innova': ('Toyota', 'Innova'),
        'toyota corolla': ('Toyota', 'Corolla'),
        'daihatsu xenia': ('Maruti', 'Ertiga'),
        'daihatsu ayla': ('Maruti', 'Alto'),
        'daihatsu sigra': ('Maruti', 'Wagon'),
        'daihatsu terios': ('Ford', 'EcoSport'),
        'daihatsu sirion': ('Hyundai', 'i10'),
        'honda brio': ('Hyundai', 'i10'),
        'honda jazz': ('Hyundai', 'i20'),
        'honda hr-v': ('Hyundai', 'Creta'),
        'honda cr-v': ('Mahindra', 'XUV500'),
        'honda civic': ('Hyundai', 'Verna'),
        'honda city': ('Honda', 'City'),
        'honda mobilio': ('Maruti', 'Ertiga'),
        'mitsubishi xpander': ('Maruti', 'Ertiga'),
        'mitsubishi pajero': ('Toyota', 'Fortuner'),
        'mitsubishi mirage': ('Hyundai', 'i10'),
        'suzuki ertiga': ('Maruti', 'Ertiga'),
        'suzuki swift': ('Maruti', 'Swift'),
        'suzuki baleno': ('Maruti', 'Baleno'),
        'suzuki ignis': ('Maruti', 'Ignis'),
        'nissan grand livina': ('Maruti', 'Ertiga'),
        'nissan march': ('Hyundai', 'i10'),
    }

    mapped = False
    for ind_key, ind_val in INDONESIAN_CAR_MAP.items():
        if ind_key in input_key or input_key in ind_key:
            brand, model_n = ind_val
            mapped = True
            break

    if not mapped:
        if brand.lower() == 'suzuki':
            brand = 'Maruti'

    brand_model_str = f"{brand} {model_n}"
    orig_brand_model_str = f"{orig_brand} {orig_model}"
    
    car_age   = 2025 - year
    km_per_yr = km / (car_age + 1)
    age_x_km  = car_age * km

    # Build raw row
    row = pd.DataFrame([{
        'km_driven':   km,
        'car_age':     car_age,
        'km_per_year': km_per_yr,
        'age_x_km':    age_x_km,
        'owner':       owner,
        'brand_model': brand_model_str,
        'fuel':        fuel,
        'seller_type': seller,
        'transmission': trans,
    }])

    # OrdinalEncoder for owner
    row['owner_enc'] = _encoder.transform(row[['owner']])
    row.drop('owner', axis=1, inplace=True)

    # Frequency encoding for brand_model
    row['brand_freq'] = row['brand_model'].map(_brand_freq).fillna(0)
    row.drop('brand_model', axis=1, inplace=True)

    # OHE for categoricals
    row = pd.get_dummies(row, columns=['fuel', 'seller_type', 'transmission'],
                         drop_first=False, dtype=int)

    # Align columns with training
    row = row.reindex(columns=_feature_cols, fill_value=0)

    # Predict in log-space, inverse to INR, then convert to IDR
    log_pred  = _model.predict(row)[0]
    base_price_inr = float(np.expm1(log_pred))
    
    EXCHANGE_RATE_INR_TO_IDR = 190.0
    raw_price_idr = base_price_inr * EXCHANGE_RATE_INR_TO_IDR

    # Dynamic Indonesia Market Calibration
    if raw_price_idr < 150000000:
        INDONESIA_MARKET_MULTIPLIER = 1.40
    elif raw_price_idr < 250000000:
        INDONESIA_MARKET_MULTIPLIER = 1.15
    else:
        INDONESIA_MARKET_MULTIPLIER = 0.88

    base_price = raw_price_idr * INDONESIA_MARKET_MULTIPLIER

    # Confidence interval estimate (~±15% from model RMSE)
    ci_low  = base_price * 0.87
    ci_high = base_price * 1.13

    # Apply condition penalty
    condition = calculate_condition_penalty(form_data)
    adj_price = base_price * condition['final_multiplier']
    adj_low   = ci_low  * condition['final_multiplier']
    adj_high  = ci_high * condition['final_multiplier']

    return {
        'base_price':      round(base_price),
        'adjusted_price':  round(adj_price),
        'ci_low':          round(adj_low),
        'ci_high':         round(adj_high),
        'condition':       condition,
        'ai_model':        'HistGradientBoosting Regressor',
        'accuracy_r2':     '93.4%',
        'inputs': {
            'brand_model': orig_brand_model_str,
            'year':        year,
            'km':          int(km),
            'fuel':        fuel,
            'transmission': trans,
            'owner':       owner,
            'seller_type': seller,
        }
    }


# =============================================================
# In-memory result store (use Redis/DB in production)
# =============================================================
_results_store: dict = {}


# =============================================================
# Routes
# =============================================================
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET'])
def predict_page():
    return render_template('predict.html')


@app.route('/predict', methods=['POST'])
def predict_submit():
    try:
        result = predict_price(request.form.to_dict())
        rid = str(uuid.uuid4())[:8]
        _results_store[rid] = result
        return redirect(url_for('result_page', rid=rid))
    except Exception as e:
        return render_template('predict.html', error=str(e))


@app.route('/result/<rid>')
def result_page(rid):
    result = _results_store.get(rid)
    if not result:
        return redirect(url_for('predict_page'))
    return render_template('result.html', result=result)


@app.route('/data-insights')
def data_insights():
    return render_template('data_insights.html')


@app.route('/model-info')
def model_info():
    return render_template('model_info.html')


@app.route('/about')
def about():
    return render_template('about.html')


# JSON API (for AJAX or external consumers)
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json(force=True)
    if not data:
        return jsonify({'error': 'No JSON body'}), 400
    try:
        result = predict_price(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/condition-factors', methods=['GET'])
def api_condition_factors():
    """Return the full condition penalty table. Useful for frontend dropdowns."""
    return jsonify(CONDITION_PENALTIES)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
