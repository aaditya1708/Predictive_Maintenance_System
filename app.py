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
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root & background ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #F7F5F0 !important;
    color: #374151 !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: #F7F5F0 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* Hide default streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

/* ── Custom header strip ── */
.hmi-header {
    background: linear-gradient(135deg, #FFFFFF 0%, #FBF9F4 100%);
    border: 1px solid #E0DDD2;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(31, 41, 55, 0.05);
}

.hmi-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #0369A1, #0EA5E9, #0369A1);
}

.hmi-header .icon {
    font-size: 2.8rem;
    line-height: 1;
}

.hmi-header h1 {
    font-family: 'Inter', sans-serif;
    font-size: 1.65rem;
    font-weight: 700;
    color: #1F2937;
    margin: 0;
    letter-spacing: -0.02em;
}

.hmi-header p {
    font-size: 0.82rem;
    color: #6B7280;
    margin: 4px 0 0 0;
    font-family: 'Roboto Mono', monospace;
    letter-spacing: 0.03em;
}

.hmi-status {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'Roboto Mono', monospace;
    font-size: 0.72rem;
    color: #047857;
    background: rgba(4, 120, 87, 0.1);
    border: 1px solid rgba(4, 120, 87, 0.25);
    border-radius: 20px;
    padding: 6px 14px;
}

.hmi-status::before {
    content: '';
    width: 7px; height: 7px;
    background: #047857;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Section label (eyebrow) ── */
.section-label {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    color: #0369A1;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #E0DDD2, transparent);
}

/* ── Panel card ── */
.panel-card {
    background: #FFFFFF;
    border: 1px solid #E0DDD2;
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 16px;
    box-shadow: 0 1px 6px rgba(31, 41, 55, 0.04);
}

/* ── Streamlit number inputs & selects ── */
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    font-family: 'Roboto Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    color: #6B7280 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background-color: #F7F5F0 !important;
    border: 1px solid #E0DDD2 !important;
    border-radius: 8px !important;
    color: #1F2937 !important;
    font-family: 'Roboto Mono', monospace !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
}

[data-testid="stNumberInput"] input:focus,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #0369A1 !important;
    box-shadow: 0 0 0 2px rgba(3, 105, 161, 0.15) !important;
}

/* ── Predict button ── */
.stButton > button {
    background: linear-gradient(135deg, #0369A1, #0EA5E9) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    padding: 14px 36px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0284C7, #38BDF8) !important;
    box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Gauge container ── */
.gauge-wrap {
    background: #FFFFFF;
    border: 1px solid #E0DDD2;
    border-radius: 12px;
    padding: 28px 24px 20px;
    text-align: center;
    margin-top: 4px;
    box-shadow: 0 1px 8px rgba(31, 41, 55, 0.05);
}

/* ── Result cards ── */
.result-safe {
    background: rgba(4, 120, 87, 0.08);
    border: 1px solid rgba(4, 120, 87, 0.35);
    border-radius: 10px;
    padding: 18px 22px;
    margin-top: 16px;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #047857;
    display: flex;
    align-items: center;
    gap: 10px;
}

.result-danger {
    background: rgba(185, 28, 28, 0.08);
    border: 1px solid rgba(185, 28, 28, 0.35);
    border-radius: 10px;
    padding: 18px 22px;
    margin-top: 16px;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #B91C1C;
    display: flex;
    align-items: center;
    gap: 10px;
}

.result-label {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.68rem;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 4px;
}

/* ── Stat mini card ── */
.stat-row {
    display: flex;
    gap: 12px;
    margin-top: 16px;
}

.stat-box {
    flex: 1;
    background: #F7F5F0;
    border: 1px solid #E0DDD2;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: center;
}

.stat-box .val {
    font-family: 'Roboto Mono', monospace;
    font-size: 1.45rem;
    font-weight: 600;
    color: #1F2937;
    line-height: 1;
}

.stat-box .lbl {
    font-family: 'Roboto Mono', monospace;
    font-size: 0.65rem;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 5px;
}

/* ── Divider override ── */
hr {
    border-color: #E0DDD2 !important;
    margin: 24px 0 !important;
}

/* ── Responsive column gap ── */
[data-testid="column"] { padding: 0 8px !important; }
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


col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.markdown('<p class="section-label">Sensor Readings</p>', unsafe_allow_html=True)
    with st.container():
        volt = st.number_input("Voltage (V)", min_value=0.0, value=170.0, step=0.1, format="%.1f")
        rotate = st.number_input("Rotation Speed (RPM)", min_value=0.0, value=450.0, step=1.0, format="%.1f")
        pressure = st.number_input("Pressure (PSI)", min_value=0.0, value=100.0, step=0.5, format="%.1f")
        vibration = st.number_input("Vibration (mm/s)", min_value=0.0, value=40.0, step=0.1, format="%.2f")

with col_right:
    st.markdown('<p class="section-label">Machine Profile</p>', unsafe_allow_html=True)
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
        <div style="font-family:'Roboto Mono',monospace; font-size:0.72rem;
                    color:#6B7280; line-height:2; background:#F7F5F0;
                    border:1px solid #E0DDD2; border-radius:8px; padding:12px 16px;">
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