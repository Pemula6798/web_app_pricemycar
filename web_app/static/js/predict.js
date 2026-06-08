
// predict.js — live penalty preview + progress


const PENALTIES = {
  body_damage_severity: { 0: 0, 1: 4, 2: 12, 3: 28 },
  paint_condition:      { excellent: 0, good: 2, fair: 6, poor: 13 },
  interior_condition:   { excellent: 0, good: 2, fair: 7, poor: 15 },
  accident_history:     { none: 0, minor: 8, moderate: 20, major: 40 },
  flood_damage:         { none: 0, minor: 20, severe: 50 },
  engine_condition:     { excellent: 0, good: 3, fair: 10, poor: 30 },
  tire_condition:       { good: 0, worn: 3, bald: 5 },
  service_history:      { complete: -3, partial: 0, none: 6 },
  modification_status:  { stock: 0, cosmetic_minor: 2, cosmetic_major: 5, performance: 4, non_reversible: 8 },
};

function calcPenalty() {
  let total = 0;

  // Body damage severity
  const sev = parseInt(document.querySelector('[name=body_damage_severity]')?.value || 0);
  total += PENALTIES.body_damage_severity[sev] || 0;

  // Dent count extra
  const dents = parseInt(document.querySelector('[name=dent_count]')?.value || 0);
  total += Math.min(dents * 2, 15);

  // Other dropdowns
  const fields = ['paint_condition','interior_condition','accident_history',
                  'flood_damage','engine_condition','tire_condition',
                  'service_history','modification_status'];
  fields.forEach(f => {
    const el = document.querySelector(`[name=${f}]`);
    if (el) total += PENALTIES[f][el.value] || 0;
  });

  return Math.max(-5, Math.min(90, total));
}

function updatePenaltyPreview() {
  const pct = calcPenalty();
  document.getElementById('penaltyPct').textContent = (pct >= 0 ? '−' : '+') + Math.abs(pct) + '%';
  document.getElementById('penaltyFill').style.width = Math.abs(pct) + '%';
  const fill = document.getElementById('penaltyFill');
  fill.style.background = pct > 20 ? '#DC2626' : pct > 10 ? '#D97706' : '#16A34A';
}

// ── Progress tracker ──
function updateProgress() {
  const brand  = document.querySelector('[name=brand]')?.value.trim();
  const model  = document.querySelector('[name=model]')?.value.trim();
  const year   = document.querySelector('[name=year]')?.value;
  const km     = document.querySelector('[name=mileage]')?.value;
  const fuel   = document.querySelector('[name=fuel_type]')?.value;

  const checks = {
    'cl-make': !!(brand && model),
    'cl-age':  !!(year && km),
    'cl-spec': !!(fuel),
    'cl-cond': calcPenalty() !== 5,  // user touched condition section
  };

  let done = 0;
  Object.entries(checks).forEach(([id, ok]) => {
    const el = document.getElementById(id);
    if (el) { el.classList.toggle('done', ok); if (ok) done++; }
  });

  const pct = 14 + Math.round((done / 4) * 86);
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressPct').textContent  = pct + '%';
}

// ── Event Listeners ──
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('predictForm')?.addEventListener('input', () => {
    updatePenaltyPreview();
    updateProgress();
  });
  updatePenaltyPreview();
  updateProgress();
});
