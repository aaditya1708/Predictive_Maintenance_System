import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #f3f6fb; --card: #fff; --ink: #14213a; --muted: #65758b;
  --line: #e2e9f2; --blue: #2563eb; --cyan: #0891b2;
  --green: #059669; --amber: #d97706; --red: #dc2626;
}
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background: var(--bg) !important; color: var(--ink) !important;
  font-family: 'Manrope', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main { background: var(--bg) !important; }
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
.block-container { max-width: 1440px !important; padding: 1.6rem 2.8rem 3rem !important; }
[data-testid="column"] { padding: 0 .55rem !important; }
[data-testid="stVerticalBlock"] { gap: .75rem; }

/* Application top bar */
.hmi-header {
  position: relative; overflow: hidden; display: flex; align-items: center; gap: 1.1rem;
  padding: 1.55rem 1.8rem; margin-bottom: 1.35rem; border-radius: 20px;
  border: 1px solid #233d60;
  background: linear-gradient(112deg, #0b1426 0%, #142a49 58%, #075985 100%);
  box-shadow: 0 16px 38px rgba(15, 32, 58, .16);
}
.hmi-header::after {
  content: ''; position: absolute; width: 300px; height: 300px; right: -70px; top: -180px;
  border: 1px solid rgba(255,255,255,.14); border-radius: 50%;
  box-shadow: 0 0 0 30px rgba(255,255,255,.035), 0 0 0 60px rgba(255,255,255,.025);
}
.hmi-header .icon {
  z-index: 1; width: 62px; height: 62px; flex: 0 0 62px; display: grid; place-items: center;
  border-radius: 17px; background: rgba(255,255,255,.09);
  border: 1px solid rgba(255,255,255,.17); font-size: 1.9rem;
}
.hmi-header h1 {
  color: #fff; font-size: clamp(1.3rem, 2.1vw, 1.85rem); line-height: 1.25;
  font-weight: 800; letter-spacing: -.045em; margin: 0;
}
.hmi-header p { color: #b8cbe2; margin: .5rem 0 0; font: 500 .67rem 'DM Mono', monospace; letter-spacing: .1em; }
.hmi-status {
  z-index: 1; margin-left: auto; display: flex; align-items: center; gap: .55rem;
  white-space: nowrap; padding: .6rem .85rem; border-radius: 999px;
  border: 1px solid rgba(110,231,183,.27); background: rgba(16,185,129,.12);
  color: #a7f3d0; font: 500 .66rem 'DM Mono', monospace; letter-spacing: .07em;
}
.hmi-status::before { content: ''; width: 7px; height: 7px; border-radius: 50%; background: #34d399; box-shadow: 0 0 0 4px rgba(52,211,153,.13); }

/* Dashboard context / cards */
.dashboard-intro { display:flex; justify-content:space-between; align-items:flex-end; gap:1rem; margin: .15rem .2rem 1.2rem; }
.dashboard-intro h2 { margin:0; color:#172844; font-size:1.18rem; font-weight:800; letter-spacing:-.035em; }
.dashboard-intro p { margin:.35rem 0 0; color:#718096; font-size:.82rem; }
.live-chip { padding:.45rem .7rem; border:1px solid #d7e5f4; background:#fff; color:#4d6685; border-radius:9px; font:500 .64rem 'DM Mono',monospace; white-space:nowrap; }
.kpi-strip { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:.8rem; margin:0 0 1.5rem; }
.kpi-card { background:#fff; border:1px solid var(--line); border-radius:15px; padding:1rem 1.1rem; box-shadow:0 4px 15px rgba(15,23,42,.025); }
.kpi-top { display:flex; align-items:center; justify-content:space-between; gap:.5rem; color:#6b7a90; font:500 .65rem 'DM Mono',monospace; letter-spacing:.055em; text-transform:uppercase; }
.kpi-icon { display:grid; place-items:center; width:30px; height:30px; border-radius:9px; background:#eff6ff; color:#2563eb; font-size:1rem; }
.kpi-value { margin:.7rem 0 .25rem; color:#15233b; font:600 1.35rem 'DM Mono',monospace; }
.kpi-foot { color:#8190a5; font-size:.68rem; line-height:1.45; }
.section-label { display:flex; align-items:center; gap:.65rem; margin:.2rem 0 .85rem; color:#53647b; font:500 .68rem 'DM Mono',monospace; letter-spacing:.1em; text-transform:uppercase; }
.section-label::before { content:''; width:4px; height:17px; border-radius:5px; background:linear-gradient(180deg,var(--cyan),var(--blue)); }
.section-label::after { content:''; height:1px; flex:1; background:linear-gradient(90deg,#d8e2ef,transparent); }
.panel-caption { color:#8190a5; font-size:.75rem; margin:-.3rem 0 .85rem; line-height:1.5; }

/* Inputs */
[data-testid="stNumberInput"] label, [data-testid="stSelectbox"] label {
  color:#52627a !important; font:700 .7rem 'Manrope',sans-serif !important; letter-spacing:.02em !important; margin-bottom:.35rem !important;
}
[data-testid="stNumberInput"] input, [data-testid="stSelectbox"] [data-baseweb="select"] > div {
  min-height:47px; background:#fff !important; border:1px solid #dce5f0 !important;
  border-radius:11px !important; color:var(--ink) !important;
  font:600 .9rem 'DM Mono',monospace !important; box-shadow:0 1px 2px rgba(15,23,42,.025);
  transition:border-color .18s ease,box-shadow .18s ease;
}
[data-testid="stNumberInput"] input:focus, [data-testid="stSelectbox"] [data-baseweb="select"]:focus-within > div {
  border-color:#60a5fa !important; box-shadow:0 0 0 3px rgba(37,99,235,.12) !important;
}
[data-testid="stNumberInput"] button { border:0 !important; color:#64748b !important; background:transparent !important; }
[data-testid="stNumberInput"] button:hover { color:var(--blue) !important; }

/* CTA */
.stButton > button {
  width:100%; min-height:54px; border:0 !important; border-radius:12px !important;
  background:linear-gradient(100deg,#1d4ed8,#2563eb 60%,#0891b2) !important;
  color:#fff !important; font:800 .82rem 'Manrope',sans-serif !important;
  letter-spacing:.055em; text-transform:uppercase; box-shadow:0 8px 18px rgba(37,99,235,.2);
  transition:transform .18s ease,box-shadow .18s ease,filter .18s ease;
}
.stButton > button:hover { transform:translateY(-1px); filter:brightness(1.06); box-shadow:0 12px 24px rgba(37,99,235,.25); }
.stButton > button:active { transform:translateY(0); }

/* Output surfaces */
.gauge-wrap { background:#fff; border:1px solid var(--line); border-radius:18px; padding:1.4rem 1.2rem .95rem; margin-top:.25rem; text-align:center; box-shadow:0 5px 18px rgba(15,23,42,.035); }
.result-safe,.result-danger { display:flex; align-items:center; gap:.9rem; padding:1.05rem 1.15rem; margin-top:.5rem; border-radius:14px; font:700 .9rem 'Manrope',sans-serif; line-height:1.5; }
.result-safe { color:#047857; background:#ecfdf5; border:1px solid #a7f3d0; }
.result-danger { color:#b91c1c; background:#fef2f2; border:1px solid #fecaca; }
.result-label { margin-bottom:.25rem; color:#64748b; font:500 .64rem 'DM Mono',monospace; letter-spacing:.12em; text-transform:uppercase; }
.stat-row { display:flex; gap:.7rem; margin-top:.9rem; }
.stat-box { flex:1; min-width:0; padding:1rem .5rem; border:1px solid var(--line); border-radius:13px; background:#fff; box-shadow:0 3px 10px rgba(15,23,42,.025); text-align:center; }
.stat-box .val { color:var(--ink); font:600 clamp(1rem,1.6vw,1.4rem) 'DM Mono',monospace; line-height:1.25; overflow-wrap:anywhere; }
.stat-box .lbl { margin-top:.45rem; color:#64748b; font:500 .58rem 'DM Mono',monospace; letter-spacing:.05em; text-transform:uppercase; }
.telemetry-readout { background:#f8fafc; border:1px solid #e2e9f2; border-radius:12px; padding:1rem 1.1rem; color:#65758b; font:500 .7rem/2 'DM Mono',monospace; }
.telemetry-readout span { color:#1e293b; font-weight:600; }
.footer-note { display:flex; justify-content:space-between; gap:1rem; margin-top:2rem; padding-top:1rem; border-top:1px solid #e0e8f2; color:#8492a6; font:400 .65rem 'DM Mono',monospace; }
hr { border:0 !important; border-top:1px solid #dce5f0 !important; margin:1.5rem 0 !important; }
[data-testid="stAlert"] { border-radius:12px !important; }
@media(max-width:900px) {
  .block-container { padding:1.2rem 1rem 2rem !important; }
  .hmi-header { padding:1.2rem; gap:.8rem; }
  .hmi-header .icon { width:50px; height:50px; flex-basis:50px; font-size:1.5rem; }
  .hmi-header p { font-size:.56rem; }
  .hmi-status { padding:.5rem .6rem; font-size:.57rem; }
  .kpi-strip { grid-template-columns:repeat(2,minmax(0,1fr)); }
}
@media(max-width:600px) {
  .hmi-header { flex-wrap:wrap; }
  .hmi-status { margin-left:0; }
  .dashboard-intro { align-items:flex-start; flex-direction:column; }
  .stat-row { gap:.4rem; }
  .stat-box { padding:.8rem .3rem; }
  .stat-box .lbl { font-size:.5rem; }
  .footer-note { flex-direction:column; gap:.35rem; }
}
</style>
""", unsafe_allow_html=True)



@st.cache_resource
def load_artifacts():
    model = joblib.load("model.pkl")
    pipeline = joblib.load("pipeline.pkl")
    return model, pipeline

model, pipeline = load_artifacts()


st.markdown("""
<div class="hmi-header">
    <div class="icon">⚙️</div>
    <div>
        <h1>Predictive Maintenance System</h1>
        <p>SENSOR TELEMETRY · FAILURE FORECAST · 24-HOUR HORIZON</p>
    </div>
    <div class="hmi-status">SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-intro">
  <div>
    <h2>Operations overview</h2>
    <p>Review machine telemetry and estimate near-term failure risk before maintenance is required.</p>
  </div>
  <div class="live-chip">●&nbsp; PREDICTION CONSOLE</div>
</div>
<div class="kpi-strip">
  <div class="kpi-card">
    <div class="kpi-top">Analysis window <span class="kpi-icon">◷</span></div>
    <div class="kpi-value">24 hours</div>
    <div class="kpi-foot">Near-term failure forecast</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-top">Sensor channels <span class="kpi-icon">⌁</span></div>
    <div class="kpi-value">04</div>
    <div class="kpi-foot">Voltage, rotation, pressure, vibration</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-top">Asset profile <span class="kpi-icon">⚙</span></div>
    <div class="kpi-value">08 inputs</div>
    <div class="kpi-foot">Telemetry and machine history</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-top">Decision support <span class="kpi-icon">◈</span></div>
    <div class="kpi-value">AI model</div>
    <div class="kpi-foot">Risk estimate from your trained pipeline</div>
  </div>
</div>
""", unsafe_allow_html=True)



col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown('<p class="section-label">Sensor Readings</p><p class="panel-caption">Enter the latest measured operating values from the target machine.</p>', unsafe_allow_html=True)
    with st.container():
        volt = st.number_input("Voltage (V)", min_value=0.0, value=170.0, step=0.1, format="%.1f")
        rotate = st.number_input("Rotation Speed (RPM)", min_value=0.0, value=450.0, step=1.0, format="%.1f")
        pressure = st.number_input("Pressure (PSI)", min_value=0.0, value=100.0, step=0.5, format="%.1f")
        vibration = st.number_input("Vibration (mm/s)", min_value=0.0, value=40.0, step=0.1, format="%.2f")

with col_right:
    st.markdown('<p class="section-label">Machine Profile</p><p class="panel-caption">Add asset age and recent fault / maintenance history.</p>', unsafe_allow_html=True)
    with st.container():
        model_type = st.selectbox("Machine Model", ["model1", "model2", "model3", "model4"])
        age = st.number_input("Machine Age (years)", min_value=0, value=10, step=1)
        error_count_24h = st.number_input("Errors in Last 24 Hours", min_value=0, value=0, step=1)
        maintenance_count_30d = st.number_input("Maintenance Events (30 Days)", min_value=0, value=0, step=1)


st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
predict_clicked = st.button("▶  Run Failure Analysis", use_container_width=True)


if predict_clicked:

    input_df = pd.DataFrame({
        "volt": [volt],
        "rotate": [rotate],
        "pressure": [pressure],
        "vibration": [vibration],
        "age": [age],
        "model": [model_type],
        "error_count_24h": [error_count_24h],
        "maintenance_count_30d": [maintenance_count_30d],
    })

    input_prepared = pipeline.transform(input_df)
    prediction = model.predict(input_prepared)[0]
    probability = model.predict_proba(input_prepared)[0][1]
    pct = probability * 100

    # Colour stops: green → amber → red
    if pct < 40:
        gauge_color = "#047857"
        arc_class = "safe"
    elif pct < 70:
        gauge_color = "#C2410C"
        arc_class = "warn"
    else:
        gauge_color = "#B91C1C"
        arc_class = "danger"


    CIRC = 251.3
    filled = CIRC * (pct / 100)
    empty  = CIRC - filled

    st.markdown("<hr>", unsafe_allow_html=True)

    res_col, gauge_col = st.columns([1.15, 1], gap="large")

    with gauge_col:
        st.markdown(f"""
        <div class="gauge-wrap">
            <svg viewBox="0 0 200 110" width="100%" style="overflow:visible">
              <!-- Track arc -->
              <path d="M 20 100 A 80 80 0 0 1 180 100"
                    fill="none" stroke="#E0DDD2" stroke-width="14"
                    stroke-linecap="round"/>
              <!-- Value arc -->
              <path d="M 20 100 A 80 80 0 0 1 180 100"
                    fill="none" stroke="{gauge_color}" stroke-width="14"
                    stroke-linecap="round"
                    stroke-dasharray="{filled:.1f} {empty:.1f}"
                    style="transition: stroke-dasharray 0.6s ease;"/>
              <!-- Centre value -->
              <text x="100" y="92" text-anchor="middle"
                    font-family="Roboto Mono, monospace"
                    font-size="26" font-weight="600"
                    fill="{gauge_color}">{pct:.1f}%</text>
              <text x="100" y="108" text-anchor="middle"
                    font-family="Roboto Mono, monospace"
                    font-size="8.5" fill="#6B7280" letter-spacing="1">FAILURE PROBABILITY</text>
              <!-- Tick labels -->
              <text x="14" y="113" font-family="Roboto Mono, monospace" font-size="7.5" fill="#9CA3AF">0</text>
              <text x="95" y="20" font-family="Roboto Mono, monospace" font-size="7.5" fill="#9CA3AF">50</text>
              <text x="178" y="113" font-family="Roboto Mono, monospace" font-size="7.5" fill="#9CA3AF">100</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)

    with res_col:
        st.markdown('<p class="section-label" style="margin-top:4px">Analysis Result</p>', unsafe_allow_html=True)

        if prediction == 1:
            st.markdown(f"""
            <div class="result-danger">
                <span style="font-size:1.4rem">⚠️</span>
                <div>
                    <div class="result-label">Status</div>
                    High Risk — Failure Likely Within 24 Hours
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-safe">
                <span style="font-size:1.4rem">✅</span>
                <div>
                    <div class="result-label">Status</div>
                    Low Risk — Machine Operating Normally
                </div>
            </div>""", unsafe_allow_html=True)

        
        safe_pct = 100 - pct
        risk_level = "CRITICAL" if pct >= 70 else ("MODERATE" if pct >= 40 else "NOMINAL")
        risk_color = "#B91C1C" if pct >= 70 else ("#C2410C" if pct >= 40 else "#047857")

        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-box">
                <div class="val" style="color:{gauge_color}">{pct:.1f}%</div>
                <div class="lbl">Failure Risk</div>
            </div>
            <div class="stat-box">
                <div class="val" style="color:#047857">{safe_pct:.1f}%</div>
                <div class="lbl">Reliability</div>
            </div>
            <div class="stat-box">
                <div class="val" style="color:{risk_color}; font-size:0.95rem; padding-top:4px">{risk_level}</div>
                <div class="lbl">Risk Level</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Input echo — compact telemetry readout
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown('<p class="section-label">Input Telemetry</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="telemetry-readout">
            VOLT&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#374151">{volt:.1f} V</span><br>
            ROTATE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#374151">{rotate:.1f} RPM</span><br>
            PRESSURE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#374151">{pressure:.1f} PSI</span><br>
            VIBRATION&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#374151">{vibration:.2f} mm/s</span><br>
            MODEL&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#374151">{model_type.upper()}</span><br>
            AGE&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#374151">{age} yr</span><br>
            ERRORS/24H&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#374151">{error_count_24h}</span><br>
            MAINT/30D&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#374151">{maintenance_count_30d}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-note">
  <span>PREDICTIVE MAINTENANCE · CONDITION MONITORING</span>
  <span>Decision support only · Validate alerts against real operating conditions</span>
</div>
""", unsafe_allow_html=True)
