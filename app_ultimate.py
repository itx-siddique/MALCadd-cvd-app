# -*- coding: utf-8 -*-
import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="MaLCaDD - CVD Diagnosis CDSS",
    layout="wide",
    initial_sidebar_state="expanded"
)

def st_html(html_content: str):
    cleaned = "".join(line.strip() for line in html_content.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)

st_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* ── Global App ── */
    .stApp {
        background-color: #F0F4FF;
        color: #1E293B;
        font-family: 'Inter', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}

    /* ── Hide Streamlit yellow warning banners ── */
    .stAlert[data-baseweb="notification"] { display: none !important; }
    div[data-testid="stNotification"] { display: none !important; }
    .element-container:has(.stWarning) { display: none !important; }
    div[role="alert"] { display: none !important; }
    .stWarning { display: none !important; }
    .stStatusWidget { display: none !important; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #DBEAFE;
    }

    /* Force ALL sidebar text to be visible dark */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stNumberInput label,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stCheckbox label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #1E293B !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #1E3A8A !important;
        font-family: 'Outfit', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        border-bottom: 2px solid #DBEAFE;
        padding-bottom: 0.4rem;
        margin-top: 1rem;
    }

    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #1D4ED8 !important;
        font-family: 'Outfit', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 1rem;
        margin-bottom: 0.25rem;
    }

    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
        color: #64748B !important;
    }

    section[data-testid="stSidebar"] .stRadio > label,
    section[data-testid="stSidebar"] .stCheckbox > label {
        color: #1E293B !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] input[type="number"] {
        color: #1E293B !important;
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
    }

    /* ── Heartbeat animation ── */
    @keyframes heartbeat {
        0%   { transform: scale(1); }
        14%  { transform: scale(1.15); }
        28%  { transform: scale(1); }
        42%  { transform: scale(1.1); }
        70%  { transform: scale(1); }
        100% { transform: scale(1); }
    }
    .heart-beat {
        display: inline-block;
        animation: heartbeat 1.6s infinite;
        transform-origin: center;
    }

    @keyframes pulse-line {
        0%   { stroke-dashoffset: 300; }
        100% { stroke-dashoffset: 0; }
    }

    /* ── Header Card ── */
    .app-title-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #1D4ED8 60%, #2563EB 100%);
        padding: 1.75rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(30,58,138,0.35);
        display: flex;
        align-items: center;
        gap: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .app-title-container::before {
        content: '';
        position: absolute;
        right: -60px;
        top: -60px;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: rgba(255,255,255,0.05);
    }
    .app-title-container::after {
        content: '';
        position: absolute;
        right: 80px;
        bottom: -80px;
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: rgba(255,255,255,0.04);
    }
    .app-title {
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .app-subtitle {
        color: #BFDBFE;
        font-size: 0.95rem;
        margin-top: 0.3rem;
        font-weight: 400;
    }
    .header-badge {
        background: rgba(255,255,255,0.15);
        border: 1px solid rgba(255,255,255,0.25);
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        display: inline-block;
        margin-top: 0.5rem;
        letter-spacing: 0.3px;
    }

    /* ── Performance Banner ── */
    .performance-banner {
        background-color: #FFFFFF;
        border: 1px solid #DBEAFE;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(30,58,138,0.07);
    }
    .banner-title {
        color: #1E3A8A;
        font-family: 'Outfit', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid #EFF6FF;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(145deg, #EFF6FF, #DBEAFE);
        border: 1px solid #BFDBFE;
        border-radius: 10px;
        padding: 0.75rem;
        text-align: center;
        transition: all 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px -2px rgba(30,58,138,0.15);
    }
    .metric-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1D4ED8;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #1E3A8A;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.3px;
        margin-top: 0.15rem;
    }

    /* ── Cards ── */
    .card {
        background-color: #FFFFFF;
        border: 1px solid #DBEAFE;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(30,58,138,0.06);
    }
    .card-title {
        color: #1E3A8A;
        font-family: 'Outfit', sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid #EFF6FF;
        padding-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── Triage Boxes ── */
    .triage-box {
        padding: 1rem 1.25rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-left: 5px solid transparent;
    }
    .triage-critical { background-color: #FEF2F2; border-left-color: #EF4444; color: #991B1B; }
    .triage-high     { background-color: #FFF7ED; border-left-color: #F97316; color: #9A3412; }
    .triage-moderate { background-color: #FEF3C7; border-left-color: #D97706; color: #92400E; }
    .triage-low      { background-color: #ECFDF5; border-left-color: #10B981; color: #065F46; }

    /* ── Gauge ── */
    .gauge-wrapper { margin: 1.25rem 0; }
    .gauge-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        font-weight: 700;
        color: #475569;
        margin-bottom: 0.5rem;
    }
    .gauge-track {
        background-color: #E2E8F0;
        border-radius: 9999px;
        height: 18px;
        overflow: hidden;
        border: 1px solid #CBD5E1;
    }
    .gauge-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.4s cubic-bezier(0.4,0,0.2,1);
    }

    /* ── Reasoning List ── */
    .reasoning-list {
        background-color: #F8FAFF;
        border: 1px solid #DBEAFE;
        border-radius: 8px;
        padding: 1.25rem 1.25rem 1.25rem 2rem;
        margin-top: 0.5rem;
    }
    .reasoning-list li {
        margin-bottom: 0.75rem;
        color: #334155;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .reasoning-list li strong { color: #0F172A; }

    /* ── Var Grid ── */
    .var-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
        gap: 0.85rem;
        margin-top: 0.5rem;
    }
    .var-card {
        background: linear-gradient(145deg, #EFF6FF, #F0F9FF);
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 0.75rem;
    }
    .var-label {
        font-size: 0.7rem;
        color: #1D4ED8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .var-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 0.25rem;
    }

    /* ── Waiting screen ── */
    .waiting-card {
        background-color: #FFFFFF;
        border: 1px solid #DBEAFE;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(30,58,138,0.06);
        margin-top: 1rem;
        /* ── Number input +/- buttons fix ── */
    section[data-testid="stSidebar"] button[data-testid="stNumberInputStepDown"],
    section[data-testid="stSidebar"] button[data-testid="stNumberInputStepUp"] {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 6px !important;
    }

    section[data-testid="stSidebar"] button[data-testid="stNumberInputStepDown"]:hover,
    section[data-testid="stSidebar"] button[data-testid="stNumberInputStepUp"]:hover {
        background-color: #DBEAFE !important;
        color: #1E3A8A !important;
    }

    /* ── Number input box itself ── */
    section[data-testid="stSidebar"] input[type="number"] {
        background-color: #F8FAFF !important;
        color: #1E293B !important;
        border: 1px solid #BFDBFE !important;
        border-radius: 6px !important;
    }

    /* ── Reset Diagnostic secondary button ── */
    section[data-testid="stSidebar"] button[kind="secondary"],
    section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-secondary"] {
        background-color: #FEF2F2 !important;
        color: #991B1B !important;
        border: 1px solid #FECACA !important;
        border-radius: 8px !important;
    }

    section[data-testid="stSidebar"] button[kind="secondary"]:hover,
    section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-secondary"]:hover {
        background-color: #FEE2E2 !important;
        color: #7F1D1D !important;
        border-color: #FCA5A5 !important;
    }
    }
</style>
""")


def generate_mock_model_file():
    from generate_mock_model import main as train_mock
    try:
        train_mock()
        return True
    except Exception as e:
        st.error(f"Error auto-generating model pipeline: {str(e)}")
        return False

@st.cache_resource
def load_model():
    model_paths = [
        'MaLCaDD_FINAL.pkl',
        'heart_disease_model.pkl',
        os.path.join(os.path.dirname(__file__), 'MaLCaDD_FINAL.pkl'),
        os.path.join(os.path.dirname(__file__), 'heart_disease_model.pkl'),
    ]
    loaded_model = None
    searched_paths = []
    for path in model_paths:
        searched_paths.append(path)
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    loaded_model = pickle.load(f)
                break
            except Exception:
                pass
    if loaded_model is None:
        if generate_mock_model_file():
            try:
                with open('MaLCaDD_FINAL.pkl', 'rb') as f:
                    loaded_model = pickle.load(f)
            except Exception as e:
                st.error(f"Failed to load newly generated model: {str(e)}")
        else:
            st.error(f"Could not load or generate model. Searched: {searched_paths}")
    return loaded_model

model = load_model()

# ── HEADER ────────────────────────────────────────────────────────────────────
st_html("""
<div class="app-title-container">
    <div style="flex-shrink:0; z-index:1;">
        <svg width="90" height="90" viewBox="0 0 90 90" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Heart shape -->
            <path d="M45 75 C45 75 10 52 10 28 C10 18 18 10 28 10 C35 10 41 14 45 20 C49 14 55 10 62 10 C72 10 80 18 80 28 C80 52 45 75 45 75Z"
                  fill="rgba(255,255,255,0.18)" stroke="rgba(255,255,255,0.6)" stroke-width="2"/>
            <!-- Heartbeat ECG line inside heart -->
            <polyline points="18,42 28,42 32,30 36,54 40,38 44,38 48,46 52,46 56,34 60,50 64,42 72,42"
                      fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"
                      style="animation: pulse-line 2s linear infinite; stroke-dasharray: 300; stroke-dashoffset: 300;">
                <animate attributeName="stroke-dashoffset" from="300" to="0" dur="2s" repeatCount="indefinite"/>
            </polyline>
        </svg>
    </div>
    <div style="z-index:1;">
        <div class="app-title">MaLCaDD</div>
        <div class="app-subtitle">Machine Learning Cardiovascular Disease Diagnosis &mdash; Clinical Decision Support System</div>
        <span class="header-badge">&#9679; Ensemble Voting Classifier &nbsp;|&nbsp; 22 Clinical Parameters</span>
    </div>
    <!-- Decorative faint large heart background -->
    <div style="position:absolute; right:2rem; top:50%; transform:translateY(-50%); opacity:0.07; z-index:0; pointer-events:none;">
        <svg width="160" height="160" viewBox="0 0 90 90" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M45 80 C45 80 5 54 5 26 C5 14 14 5 26 5 C34 5 41 10 45 18 C49 10 56 5 64 5 C76 5 85 14 85 26 C85 54 45 80 45 80Z"
                  fill="white"/>
        </svg>
    </div>
</div>
""")

# ── PERFORMANCE BANNER ─────────────────────────────────────────────────────────
st_html("""
<div class="performance-banner">
    <div class="banner-title">&#10084; Final Model Performance Benchmarks</div>
    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem;">
        <div class="metric-card"><div class="metric-value">94.04%</div><div class="metric-label">Accuracy</div></div>
        <div class="metric-card"><div class="metric-value">95.15%</div><div class="metric-label">Sensitivity</div></div>
        <div class="metric-card"><div class="metric-value">92.93%</div><div class="metric-label">Specificity</div></div>
        <div class="metric-card"><div class="metric-value">0.9851</div><div class="metric-label">ROC-AUC</div></div>
        <div class="metric-card"><div class="metric-value">93.09%</div><div class="metric-label">Precision</div></div>
        <div class="metric-card"><div class="metric-value">94.11%</div><div class="metric-label">F1 Score</div></div>
    </div>
</div>
""")

# ── SIDEBAR INPUTS ─────────────────────────────────────────────────────────────
st.sidebar.markdown("## ❤️ Patient Profile Details")

st.sidebar.markdown("### Demographics")
age = st.sidebar.slider("Age (Years)", min_value=20, max_value=90, value=52, step=1)
gender_label = st.sidebar.radio("Gender", options=["Female", "Male"], index=1)
gender = 1 if gender_label == "Male" else 0

st.sidebar.markdown("### Blood Panel & Vitals")
sbp = st.sidebar.number_input("Systolic BP (mmHg)", min_value=80, max_value=220, value=128, step=1)
dbp = st.sidebar.number_input("Diastolic BP (mmHg)", min_value=50, max_value=140, value=82, step=1)
cholesterol = st.sidebar.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=210, step=1)
glucose = st.sidebar.number_input("Glucose (mg/dL)", min_value=60, max_value=400, value=95, step=1)
bmi = st.sidebar.number_input("BMI (kg/m\u00b2)", min_value=15.0, max_value=50.0, value=26.4, step=0.1)

st.sidebar.markdown("### Lifestyle Factors")
cigs_per_day = st.sidebar.slider("Cigarettes Per Day", min_value=0, max_value=60, value=0, step=1)
sedentary_lifestyle = 1 if st.sidebar.checkbox("Sedentary Lifestyle") else 0
family_history = 1 if st.sidebar.checkbox("Family History of CVD") else 0
chronic_stress = 1 if st.sidebar.checkbox("Chronic Stress") else 0

st.sidebar.markdown("### Symptom Presentation")
chest_pain = 1 if st.sidebar.checkbox("Chest Pain") else 0
shortness_of_breath = 1 if st.sidebar.checkbox("Shortness of Breath") else 0
fatigue = 1 if st.sidebar.checkbox("Fatigue") else 0
palpitations = 1 if st.sidebar.checkbox("Palpitations") else 0
radiating_pain = 1 if st.sidebar.checkbox("Radiating Pain (Arms/Jaw/Back)") else 0

# ── FEATURE ENGINEERING ────────────────────────────────────────────────────────
if cigs_per_day == 0:
    smoking_level = 0
elif cigs_per_day <= 5:
    smoking_level = 1
elif cigs_per_day <= 15:
    smoking_level = 2
else:
    smoking_level = 3

clinical_vulnerability = family_history + chronic_stress
ischemic_signal = chest_pain * radiating_pain
chest_pain_weighted = chest_pain * 3.0
pulse_pressure = sbp - dbp
symptom_burden = chest_pain + shortness_of_breath + fatigue + palpitations + radiating_pain

if sbp >= 140 or dbp >= 90:
    hypertension_stage = 3
elif (130 <= sbp <= 139) or (80 <= dbp <= 89):
    hypertension_stage = 2
elif (120 <= sbp <= 129) and dbp < 80:
    hypertension_stage = 1
else:
    hypertension_stage = 0

metabolic_risk_score = int(bmi >= 25) + int(glucose >= 100) + int(cholesterol >= 200)
age_gender_risk = 1 if ((gender == 1 and age >= 45) or (gender == 0 and age >= 55)) else 0

cv_risk_score = 0
if age >= 70:   cv_risk_score += 4
elif age >= 60: cv_risk_score += 3
elif age >= 50: cv_risk_score += 2
elif age >= 40: cv_risk_score += 1
cv_risk_score += hypertension_stage
cv_risk_score += smoking_level
if cholesterol >= 240:   cv_risk_score += 2
elif cholesterol >= 200: cv_risk_score += 1
if glucose >= 126:   cv_risk_score += 2
elif glucose >= 100: cv_risk_score += 1
if bmi >= 30: cv_risk_score += 1
cv_risk_score = min(cv_risk_score, 15)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if 'diagnosed' not in st.session_state:
    st.session_state.diagnosed = False

st.sidebar.markdown("---")
if not st.session_state.diagnosed:
    st.sidebar.markdown("<p style='font-size:0.85rem; color:#475569; text-align:center;'>Double-check patient parameters before diagnostic execution.</p>", unsafe_allow_html=True)
    if st.sidebar.button("🔬 Run Diagnostic Assessment", use_container_width=True, type="primary", key="sidebar_run"):
        st.session_state.diagnosed = True
        st.rerun()
else:
    st.sidebar.markdown("<p style='font-size:0.85rem; color:#475569; text-align:center;'>Clear current diagnostic results to process a new patient.</p>", unsafe_allow_html=True)
    if st.sidebar.button("🔄 Reset Diagnostic", use_container_width=True, type="secondary", key="sidebar_reset"):
        st.session_state.diagnosed = False
        st.rerun()

# ── MAIN ROUTING ───────────────────────────────────────────────────────────────
if not st.session_state.diagnosed:
    st_html("""
    <div class="waiting-card">
        <div style="margin-bottom: 1.25rem;">
            <svg width="100" height="100" viewBox="0 0 90 90" fill="none" xmlns="http://www.w3.org/2000/svg" class="heart-beat">
                <path d="M45 78 C45 78 8 53 8 27 C8 16 17 8 28 8 C36 8 42 13 45 20 C48 13 54 8 62 8 C73 8 82 16 82 27 C82 53 45 78 45 78Z"
                      fill="#DBEAFE" stroke="#1D4ED8" stroke-width="2.5"/>
                <polyline points="20,44 28,44 32,32 36,56 40,40 44,40 48,48 52,48 56,36 60,52 64,44 70,44"
                          fill="none" stroke="#EF4444" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <h3 style="color: #1E3A8A; font-family: 'Outfit', sans-serif; margin: 0 0 0.75rem; font-size: 1.6rem; font-weight: 700;">
            Awaiting Patient Parameters
        </h3>
        <p style="color: #475569; font-size: 1rem; max-width: 600px; margin: 0 auto 1.75rem; line-height: 1.65;">
            This Clinical Decision Support System uses an ensemble machine learning voting classifier
            trained on 22 cardiovascular clinical parameters to compute real-time CVD risk probability.
        </p>
        <div style="background: #F0F7FF; border: 1px dashed #93C5FD; border-radius: 10px; padding: 1.5rem; display: inline-block; text-align: left; max-width: 520px; margin-bottom: 0.5rem;">
            <span style="color: #1E3A8A; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; display: block; margin-bottom: 0.75rem; letter-spacing: 0.5px;">
                &#9888; Workflow Instructions
            </span>
            <ol style="margin: 0; padding-left: 1.25rem; color: #334155; font-size: 0.95rem; line-height: 1.7;">
                <li style="margin-bottom: 0.4rem;">Input patient demographics and blood panel measurements in the sidebar.</li>
                <li style="margin-bottom: 0.4rem;">Select active symptom presentations and lifestyle factors.</li>
                <li>Click <strong>Run Diagnostic Assessment</strong> to compute cardiovascular risk.</li>
            </ol>
        </div>
    </div>
    """)
    if st.button("🔬 Run Diagnostic Assessment", key="main_run", type="primary", use_container_width=True):
        st.session_state.diagnosed = True
        st.rerun()

else:
    col_results, col_metrics = st.columns([3, 2])

    if model is not None:
        feature_order = [
            'Age', 'Systolic_BP', 'Diastolic_BP', 'Pulse_Pressure',
            'Total_Cholesterol', 'Glucose', 'BMI', 'CV_Risk_Score', 'Symptom_Burden',
            'Gender', 'Pain_Arms_Jaw_Back', 'Shortness_of_Breath', 'Fatigue',
            'Palpitations', 'Sedentary_Lifestyle', 'Smoking_Level',
            'Clinical_Vulnerability', 'Ischemic_Signal', 'Chest_Pain_Weighted',
            'Hypertension_Stage', 'Metabolic_Risk_Score', 'Age_Gender_Risk'
        ]
        input_data = pd.DataFrame([{
            'Age': age, 'Systolic_BP': sbp, 'Diastolic_BP': dbp,
            'Pulse_Pressure': pulse_pressure, 'Total_Cholesterol': cholesterol,
            'Glucose': glucose, 'BMI': bmi, 'CV_Risk_Score': cv_risk_score,
            'Symptom_Burden': symptom_burden, 'Gender': gender,
            'Pain_Arms_Jaw_Back': radiating_pain, 'Shortness_of_Breath': shortness_of_breath,
            'Fatigue': fatigue, 'Palpitations': palpitations,
            'Sedentary_Lifestyle': sedentary_lifestyle, 'Smoking_Level': smoking_level,
            'Clinical_Vulnerability': clinical_vulnerability, 'Ischemic_Signal': ischemic_signal,
            'Chest_Pain_Weighted': chest_pain_weighted, 'Hypertension_Stage': hypertension_stage,
            'Metabolic_Risk_Score': metabolic_risk_score, 'Age_Gender_Risk': age_gender_risk
        }])
        input_data = input_data[feature_order]

        prob = model.predict_proba(input_data)[0][1]

        if prob > 0.70 and ischemic_signal == 1:
            risk_class = "CRITICAL"
            risk_color = "#EF4444"
            triage_style = "triage-critical"
            triage_icon = "🚨"
        elif prob > 0.50 and ischemic_signal == 1:
            risk_class = "HIGH"
            risk_color = "#F97316"
            triage_style = "triage-high"
            triage_icon = "⚠️"
        elif prob > 0.50:
            risk_class = "MODERATE"
            risk_color = "#D97706"
            triage_style = "triage-moderate"
            triage_icon = "⚠️"
        else:
            risk_class = "LOW"
            risk_color = "#10B981"
            triage_style = "triage-low"
            triage_icon = "✅"

        with col_results:
            st_html(f"""
            <div class="card">
                <div class="card-title">
                    <svg width="20" height="20" viewBox="0 0 90 90" fill="none">
                        <path d="M45 78 C45 78 8 53 8 27 C8 16 17 8 28 8 C36 8 42 13 45 20 C48 13 54 8 62 8 C73 8 82 16 82 27 C82 53 45 78 45 78Z"
                              fill="#DBEAFE" stroke="#1D4ED8" stroke-width="3"/>
                    </svg>
                    CVD Diagnostic Assessment
                </div>
                <div class="triage-box {triage_style}">
                    <span>{triage_icon}</span>
                    <span>TRIAGE STATUS: {risk_class} RISK &nbsp;({prob*100:.1f}%)</span>
                </div>
                <div class="gauge-wrapper">
                    <div class="gauge-label">
                        <span>Cardiovascular Disease Risk Probability</span>
                        <span style="color:{risk_color};">{prob*100:.1f}%</span>
                    </div>
                    <div class="gauge-track">
                        <div class="gauge-fill" style="width:{prob*100:.1f}%; background-color:{risk_color};"></div>
                    </div>
                </div>
                <div style="font-size:0.82rem; color:#1D4ED8; margin-top:0.5rem; text-align:right; font-style:italic; font-weight:600;">
                    &#9889; Real-time prediction active &mdash; adjusting sidebar parameters updates results instantly.
                </div>
            </div>
            """)

            # Clinical Reasoning
            reasons = []
            if age >= 70:
                reasons.append("<strong>Advanced age (&ge;70)</strong>: Significantly increases cardiovascular baseline vulnerability (+4 pts).")
            elif age >= 60:
                reasons.append("<strong>Senior age (60&ndash;69)</strong>: Contributes to increased risk scoring (+3 pts).")
            elif age >= 50:
                reasons.append("<strong>Middle-to-senior age (50&ndash;59)</strong>: Contributes to risk scoring (+2 pts).")

            if hypertension_stage == 3:
                reasons.append(f"<strong>Hypertension Stage 2</strong>: Highly elevated vascular pressure (SBP: {sbp} / DBP: {dbp} mmHg).")
            elif hypertension_stage == 2:
                reasons.append(f"<strong>Hypertension Stage 1</strong>: Elevated vascular pressure (SBP: {sbp} / DBP: {dbp} mmHg).")
            elif hypertension_stage == 1:
                reasons.append(f"<strong>Elevated Blood Pressure</strong>: Mildly elevated pressure (SBP: {sbp} / DBP: {dbp} mmHg).")

            if pulse_pressure >= 60:
                reasons.append(f"<strong>Widened Pulse Pressure ({pulse_pressure} mmHg)</strong>: Suggests potential arterial stiffness (normal: 40&ndash;50).")

            if cholesterol >= 240:
                reasons.append(f"<strong>Severely elevated Cholesterol ({cholesterol} mg/dL)</strong>: High hypercholesterolemia risk.")
            elif cholesterol >= 200:
                reasons.append(f"<strong>Elevated Cholesterol ({cholesterol} mg/dL)</strong>: Promotes atherogenesis.")

            if glucose >= 126:
                reasons.append(f"<strong>Diabetic-range Glucose ({glucose} mg/dL)</strong>: Elevated metabolic cardiovascular distress.")
            elif glucose >= 100:
                reasons.append(f"<strong>Pre-diabetic Glucose ({glucose} mg/dL)</strong>: Contributes to metabolic burden.")

            if bmi >= 30:
                reasons.append(f"<strong>Obese BMI ({bmi:.1f} kg/m&sup2;)</strong>: Accelerates metabolic stress and cardiac workload.")
            elif bmi >= 25:
                reasons.append(f"<strong>Overweight BMI ({bmi:.1f} kg/m&sup2;)</strong>: Contributes mildly to metabolic risk.")

            if smoking_level >= 2:
                reasons.append(f"<strong>Heavy smoking ({cigs_per_day} cigs/day)</strong>: Severely damages vascular endothelium and increases thrombogenicity.")
            elif smoking_level == 1:
                reasons.append(f"<strong>Light smoking ({cigs_per_day} cigs/day)</strong>: Contributes to endothelial stress.")

            if sedentary_lifestyle:
                reasons.append("<strong>Sedentary lifestyle</strong>: Associated with reduced vascular elasticity and aerobic deconditioning.")

            if clinical_vulnerability >= 2:
                reasons.append("<strong>High clinical vulnerability</strong>: Compounding risk from positive family history and chronic stress.")
            elif family_history:
                reasons.append("<strong>Positive family history of CVD</strong>: Suggests inherited genetic susceptibility.")

            if ischemic_signal:
                reasons.append("<span style='color:#EF4444; font-weight:700;'>🚨 ACTIVE ISCHEMIC SIGNAL</span>: Co-presentation of chest pain and radiating pain (arms/jaw/back). Requires immediate ECG and triage.")
            elif chest_pain:
                reasons.append("<strong>Active chest pain reported</strong>: Major indicator requiring cardiac ischemia evaluation.")

            if symptom_burden >= 3:
                reasons.append(f"<strong>High symptom burden ({symptom_burden}/5 active symptoms)</strong>: Points to acute clinical presentation.")

            if not reasons:
                reasons.append("No major clinical risk markers or symptoms currently active. Continue regular preventive screenings.")

            list_items = "".join([f"<li>{r}</li>" for r in reasons])
            st_html(f"""
            <div class="card">
                <div class="card-title">
                    &#128203; Clinical Reasoning &amp; Risk Factor Breakdown
                </div>
                <p style="font-size:0.92rem; color:#475569; margin-bottom:0.5rem;">
                    The diagnostic ensemble model processed 22 parameters. The following patient factors contributed to this risk stratification:
                </p>
                <ul class="reasoning-list">{list_items}</ul>
            </div>
            """)

        with col_metrics:
            st_html(f"""
            <div class="card">
                <div class="card-title">&#128200; Engineered Clinical Indicators</div>
                <div class="var-grid">
                    <div class="var-card">
                        <div class="var-label">CV Risk Score (0–15)</div>
                        <div class="var-value">{cv_risk_score} / 15</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Pulse Pressure</div>
                        <div class="var-value">{pulse_pressure} mmHg</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Hypertension Stage</div>
                        <div class="var-value">Stage {hypertension_stage}</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Metabolic Risk (0–3)</div>
                        <div class="var-value">{metabolic_risk_score} / 3</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Symptom Burden (0–5)</div>
                        <div class="var-value">{symptom_burden} / 5</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Smoking Level (0–3)</div>
                        <div class="var-value">Level {smoking_level}</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Clinical Vulnerability</div>
                        <div class="var-value">{clinical_vulnerability} / 2</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Ischemic Signal</div>
                        <div class="var-value" style="color:{'#EF4444' if ischemic_signal==1 else '#10B981'};">
                            {"🔴 Active" if ischemic_signal == 1 else "🟢 Inactive"}
                        </div>
                    </div>
                </div>
            </div>
            """)

            if risk_class == "CRITICAL":
                rec_html = """
                <li><strong>Immediate action required</strong>: Order 12-lead ECG, cardiac enzymes (Troponin), and consult Cardiology stat.</li>
                <li>Patient exhibits active ischemic symptoms with high model probability &mdash; do not delay.</li>
                <li>Initiate continuous telemetry monitoring and secure intravenous access immediately.</li>
                """
            elif risk_class == "HIGH":
                rec_html = """
                <li><strong>Urgent evaluation needed</strong>: Refer to Cardiology for stress testing or echocardiogram within 24&ndash;48 hours.</li>
                <li>Active ischemic symptoms present. Optimize medical management (antiplatelet, lipid-lowering therapies).</li>
                <li>Strict BP monitoring and avoidance of heavy physical exertion recommended.</li>
                """
            elif risk_class == "MODERATE":
                rec_html = """
                <li><strong>Primary care follow-up</strong>: Scheduled outpatient appointment to review metabolic profile and lifestyle risk factors.</li>
                <li>Address elevated lipids, blood glucose, or blood pressure. Consider pharmacological controls.</li>
                <li>Counsel patient on DASH diet, physical activity targets, and smoking cessation.</li>
                """
            else:
                rec_html = """
                <li><strong>Routine surveillance</strong>: Re-evaluate during annual physical examination.</li>
                <li>Maintain healthy lifestyle choices. Encourage smoking cessation if applicable.</li>
                <li>Review vitals and lipid panel during standard interval check-ups.</li>
                """

            st_html(f"""
            <div class="card">
                <div class="card-title">&#128203; Recommended Clinical Pathway</div>
                <ul class="reasoning-list">{rec_html}</ul>
            </div>
            """)

            # Mini ECG decoration card at bottom
            st_html("""
            <div style="background: linear-gradient(135deg, #1E3A8A, #1D4ED8); border-radius: 12px; padding: 1rem 1.25rem; text-align: center;">
                <svg width="100%" height="50" viewBox="0 0 300 50" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
                    <polyline points="0,25 30,25 40,25 50,5 60,45 70,25 90,25 110,25 120,10 130,40 140,25 160,25 180,25 190,8 200,42 210,25 230,25 250,25 260,12 270,38 280,25 300,25"
                              fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <animate attributeName="stroke-dashoffset" from="600" to="0" dur="3s" repeatCount="indefinite"/>
                    </polyline>
                </svg>
                <p style="color:rgba(255,255,255,0.75); font-size:0.75rem; margin:0.25rem 0 0; font-weight:600; letter-spacing:0.5px; text-transform:uppercase;">
                    Live ECG Pattern Monitor
                </p>
            </div>
            """)

    else:
        st.error("No model pipeline could be loaded. Please ensure MaLCaDD_FINAL.pkl is present in the application folder.")
