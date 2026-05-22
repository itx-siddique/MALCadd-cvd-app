"""
╔════════════════════════════════════════════════════════════════════╗
║     MaLCaDD ULTIMATE — Premium Clinical AI Diagnosis Dashboard    ║
║          Next-Generation Cardiovascular Risk Assessment           ║
║                Air University | Enterprise Grade                  ║
╚════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import os
from datetime import datetime

st.set_page_config(page_title="MaLCaDD Pro", page_icon="🫀", layout="wide", initial_sidebar_state="expanded")

# ════════════════════════════════════════════════════════════════════════════════
# ULTIMATE PREMIUM CSS - CUTTING EDGE DESIGN
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Outfit:wght@300;400;600;700;800&display=swap');

    /* ROOT VARIABLES */
    :root {
        --primary: #FF1654;
        --primary-dark: #C41248;
        --primary-light: #FF4D7A;
        --accent: #00D9FF;
        --accent-dark: #00A8CC;
        --success: #00FF88;
        --warning: #FFB800;
        --danger: #FF0051;
        --dark-bg: #0a0e27;
        --card-bg: rgba(20, 30, 60, 0.4);
        --border-color: rgba(0, 217, 255, 0.15);
        --text-primary: #f0f4f8;
        --text-secondary: #b0bec5;
        --text-tertiary: #8892a6;
    }

    /* GLOBAL STYLES */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body {
        scroll-behavior: smooth;
    }

    /* MAIN BACKGROUND - ANIMATED GRADIENT */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #0f1a35 25%, #141e3c 50%, #0d1829 75%, #0a0e27 100%);
        background-attachment: fixed;
        color: var(--text-primary);
        font-family: 'Outfit', sans-serif;
        overflow-x: hidden;
    }

    /* ANIMATED BACKGROUND EFFECT */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255, 22, 84, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(0, 217, 255, 0.03) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }

    @keyframes float {
        0%, 100% { transform: translate(0, 0); }
        50% { transform: translate(-50px, -50px); }
    }

    /* SIDEBAR - GLASS MORPHISM PREMIUM */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.8) 0%, rgba(15, 26, 56, 0.8) 100%) !important;
        backdrop-filter: blur(30px) !important;
        border-right: 1px solid var(--border-color) !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1), 0 20px 60px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stSidebar"] * { color: var(--text-primary) !important; }

    [data-testid="stSidebar"] label {
        color: var(--accent) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.8px !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    [data-testid="stSidebar"] .stSlider [role="slider"] {
        background: linear-gradient(90deg, var(--accent), var(--primary)) !important;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 14px 28px !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        width: 100% !important;
        box-shadow: 0 12px 40px rgba(255, 22, 84, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        position: relative;
        overflow: hidden !important;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.2);
        transition: left 0.4s ease;
    }

    .stButton > button:hover {
        box-shadow: 0 20px 60px rgba(255, 22, 84, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-3px) !important;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    /* HIDE STREAMLIT UI */
    #MainMenu, footer, .stDeployButton { visibility: hidden !important; }

    /* PREMIUM GLASS CARDS */
    .glass-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 28px;
        backdrop-filter: blur(40px);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.08);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(0, 217, 255, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(0, 217, 255, 0.3);
        background: rgba(20, 30, 60, 0.6);
        box-shadow: 0 20px 70px rgba(0, 217, 255, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.12);
        transform: translateY(-6px);
    }

    .glass-card:hover::before {
        opacity: 1;
    }

    /* METRIC CARDS - PREMIUM */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.05) 0%, rgba(255, 22, 84, 0.02) 100%);
        border: 1.5px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .metric-card:hover {
        border-color: var(--accent);
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(255, 22, 84, 0.05) 100%);
        box-shadow: 0 12px 48px rgba(0, 217, 255, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        transform: translateY(-4px) scale(1.02);
    }

    .metric-label {
        font-size: 0.8rem;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        margin-bottom: 8px;
        opacity: 0.9;
    }

    .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, var(--accent) 0%, var(--primary-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }

    .metric-unit {
        font-size: 0.85rem;
        color: var(--text-tertiary);
        font-weight: 500;
        margin-left: 4px;
    }

    /* HEADER - HERO SECTION */
    .hero-header {
        background: linear-gradient(135deg, rgba(10, 14, 39, 0.6) 0%, rgba(20, 30, 60, 0.4) 100%);
        border: 1px solid var(--border-color);
        border-radius: 28px;
        padding: 50px 40px;
        backdrop-filter: blur(40px);
        box-shadow: 0 25px 80px rgba(0, 217, 255, 0.1), inset 0 1px 1px rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 40px;
        animation: slideDown 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 217, 255, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }

    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-icon {
        font-size: 4rem;
        margin-bottom: 16px;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.05); opacity: 0.8; }
    }

    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
        background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 50%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-secondary);
        margin-top: 12px;
        letter-spacing: 0.5px;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }

    .hero-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 16px;
        margin-top: 28px;
        position: relative;
        z-index: 1;
    }

    .stat-badge {
        background: rgba(0, 217, 255, 0.05);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 12px;
        padding: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* TRIAGE RESULT CARD */
    .triage-result {
        border-radius: 24px;
        padding: 44px 32px;
        text-align: center;
        backdrop-filter: blur(30px);
        border: 2px solid;
        box-shadow: 0 25px 80px;
        animation: resultPulse 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }

    .triage-result::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: rotate 15s linear infinite;
    }

    @keyframes resultPulse {
        0%, 100% { box-shadow: 0 25px 80px currentColor; transform: scale(1); }
        50% { box-shadow: 0 35px 120px currentColor; transform: scale(1.01); }
    }

    .triage-critical { background: rgba(255, 0, 81, 0.15); border-color: rgba(255, 0, 81, 0.6); color: #FF6B7A; }
    .triage-high { background: rgba(255, 165, 0, 0.15); border-color: rgba(255, 165, 0, 0.6); color: #FFB347; }
    .triage-moderate { background: rgba(0, 150, 255, 0.15); border-color: rgba(0, 150, 255, 0.6); color: #00D9FF; }
    .triage-low { background: rgba(0, 255, 136, 0.15); border-color: rgba(0, 255, 136, 0.6); color: #00FF88; }

    .triage-icon {
        font-size: 3.5rem;
        margin-bottom: 16px;
        animation: bounce 0.6s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-12px); }
    }

    .triage-label {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'Space Grotesk', sans-serif;
        margin: 12px 0;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }

    .triage-detail {
        font-size: 0.95rem;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }

    /* REASON TAGS */
    .reason-tag {
        background: rgba(255, 255, 255, 0.02);
        border-left: 4px solid;
        border-radius: 12px;
        padding: 14px 16px;
        margin: 10px 0;
        font-size: 0.95rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        animation: slideIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        opacity: 0;
        border: 1px solid;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .reason-red { border-left-color: var(--danger); border-color: rgba(255, 0, 81, 0.2); background: rgba(255, 0, 81, 0.08); color: #FF9DB5; }
    .reason-green { border-left-color: var(--success); border-color: rgba(0, 255, 136, 0.2); background: rgba(0, 255, 136, 0.08); color: #5FFF9F; }
    .reason-amber { border-left-color: var(--warning); border-color: rgba(255, 184, 0, 0.2); background: rgba(255, 184, 0, 0.08); color: #FFD166; }

    /* EMERGENCY BANNER */
    .emergency-banner {
        background: linear-gradient(135deg, rgba(255, 0, 81, 0.2) 0%, rgba(255, 80, 100, 0.1) 100%);
        border: 2px solid rgba(255, 0, 81, 0.6);
        border-radius: 20px;
        padding: 28px;
        text-align: center;
        margin: 28px 0;
        animation: alertPulse 1.2s ease-in-out infinite;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 40px rgba(255, 0, 81, 0.3);
    }

    @keyframes alertPulse {
        0%, 100% { box-shadow: 0 0 40px rgba(255, 0, 81, 0.3); }
        50% { box-shadow: 0 0 80px rgba(255, 0, 81, 0.6); }
    }

    .emergency-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #FF6B7A;
        font-family: 'Space Grotesk', sans-serif;
        margin: 0;
    }

    .emergency-text {
        color: #FFB3B3;
        margin-top: 10px;
        font-weight: 600;
        font-size: 0.95rem;
    }

    /* SECTION TITLE */
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        font-family: 'Space Grotesk', sans-serif;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 22px;
        padding-bottom: 12px;
        border-bottom: 2px solid var(--border-color);
        position: relative;
    }

    .section-title::before {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), transparent);
        width: 100%;
        animation: expandWidth 0.6s ease;
    }

    @keyframes expandWidth {
        from { width: 0; }
        to { width: 100%; }
    }

    /* DIVIDER */
    hr {
        border: none !important;
        border-top: 1px solid var(--border-color) !important;
        margin: 28px 0 !important;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    }

    /* EXPANDABLE */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 14px !important;
        border: 1px solid var(--border-color) !important;
        padding: 14px 16px !important;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(0, 217, 255, 0.06) !important;
        border-color: rgba(0, 217, 255, 0.3) !important;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 8px !important; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(0, 217, 255, 0.15) !important;
        border-color: var(--accent) !important;
    }

    /* SCROLLBAR STYLING */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 217, 255, 0.05);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 217, 255, 0.3);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 217, 255, 0.5);
    }

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# LOAD MODEL
# ════════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    paths = ['MaLCaDD_FINAL.pkl', 'heart_disease_model.pkl']
    for path in paths:
        if os.path.exists(path):
            return joblib.load(path)
    return None

# ════════════════════════════════════════════════════════════════════════════════
# FEATURE ENGINEERING
# ════════════════════════════════════════════════════════════════════════════════
def engineer_features(raw):
    c = raw['cigs_per_day']
    smoking_level = 0 if c == 0 else (1 if c <= 5 else (2 if c <= 15 else 3))
    clinical_vulnerability = int(raw['family_history']) + int(raw['chronic_stress'])
    ischemic_signal = int(raw['chest_pain']) * int(raw['pain_arms_jaw_back'])
    chest_pain_weighted = int(raw['chest_pain']) * 3.0
    pulse_pressure = raw['systolic_bp'] - raw['diastolic_bp']
    symptom_burden = sum([int(raw['chest_pain']), int(raw['shortness_of_breath']),
                          int(raw['fatigue']), int(raw['palpitations']), int(raw['pain_arms_jaw_back'])])
    
    sbp, dbp = raw['systolic_bp'], raw['diastolic_bp']
    ht_stage = 3 if (sbp >= 140 or dbp >= 90) else (2 if (sbp >= 130 or dbp >= 80) else (1 if sbp >= 120 else 0))
    
    metabolic_risk = int(raw['bmi'] >= 25) + int(raw['glucose'] >= 100) + int(raw['total_cholesterol'] >= 200)
    age_gender_risk = int((raw['gender'] == 1 and raw['age'] >= 45) or (raw['gender'] == 0 and raw['age'] >= 55))
    
    cv_risk = 0
    cv_risk += 4 if raw['age'] >= 70 else (3 if raw['age'] >= 60 else (2 if raw['age'] >= 50 else (1 if raw['age'] >= 40 else 0)))
    cv_risk += ht_stage + smoking_level
    cv_risk += 2 if raw['total_cholesterol'] >= 240 else (1 if raw['total_cholesterol'] >= 200 else 0)
    cv_risk += 2 if raw['glucose'] >= 126 else (1 if raw['glucose'] >= 100 else 0)
    cv_risk += 1 if raw['bmi'] >= 30 else 0
    cv_risk = min(cv_risk, 15)

    df = pd.DataFrame([{
        'Age': raw['age'], 'Systolic_BP': sbp, 'Diastolic_BP': dbp,
        'Pulse_Pressure': pulse_pressure, 'Total_Cholesterol': raw['total_cholesterol'],
        'Glucose': raw['glucose'], 'BMI': raw['bmi'], 'CV_Risk_Score': cv_risk,
        'Symptom_Burden': symptom_burden, 'Gender': raw['gender'],
        'Chest_Pain': int(raw['chest_pain']),
        'Pain_Arms_Jaw_Back': int(raw['pain_arms_jaw_back']),
        'Shortness_of_Breath': int(raw['shortness_of_breath']),
        'Fatigue': int(raw['fatigue']), 'Palpitations': int(raw['palpitations']),
        'Sedentary_Lifestyle': int(raw['sedentary_lifestyle']),
        'Smoking_Level': smoking_level, 'Clinical_Vulnerability': clinical_vulnerability,
        'Ischemic_Signal': ischemic_signal, 'Chest_Pain_Weighted': chest_pain_weighted,
        'Hypertension_Stage': ht_stage, 'Metabolic_Risk_Score': metabolic_risk,
        'Age_Gender_Risk': age_gender_risk,
    }])

    return df, {
        'pulse_pressure': pulse_pressure, 'symptom_burden': symptom_burden,
        'ht_stage': ht_stage, 'metabolic_risk': metabolic_risk, 'age_gender_risk': age_gender_risk,
        'smoking_level': smoking_level, 'clinical_vuln': clinical_vulnerability,
        'ischemic_signal': ischemic_signal, 'cv_risk': cv_risk,
        'smoking_text': ['Non-smoker', 'Light', 'Moderate', 'Heavy'][smoking_level],
        'ht_text': ['Normal', 'Elevated', 'Stage 1', 'Stage 2'][ht_stage]
    }

# ════════════════════════════════════════════════════════════════════════════════
# PLOTLY DARK GAUGE
# ════════════════════════════════════════════════════════════════════════════════
def make_gauge(probability):
    pct = probability * 100
    if pct >= 70: color = "#FF1654"
    elif pct >= 50: color = "#FFB800"
    elif pct >= 30: color = "#00D9FF"
    else: color = "#00FF88"

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pct,
        number={'suffix': '%', 'font': {'size': 48, 'color': color, 'family': 'Space Grotesk'}},
        delta={'reference': 50, 'suffix': ' vs Avg', 'font': {'size': 12, 'color': '#8892a6'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': '#404040'},
            'bar': {'color': color, 'thickness': 0.38},
            'bgcolor': 'rgba(255,255,255,0.02)',
            'borderwidth': 2,
            'bordercolor': 'rgba(255,255,255,0.1)',
            'steps': [
                {'range': [0, 30],   'color': 'rgba(0, 255, 136, 0.08)'},
                {'range': [30, 50],  'color': 'rgba(0, 217, 255, 0.08)'},
                {'range': [50, 70],  'color': 'rgba(255, 184, 0, 0.08)'},
                {'range': [70, 100], 'color': 'rgba(255, 22, 84, 0.08)'},
            ]
        }
    ))
    fig.update_layout(
        height=320, margin=dict(t=30, b=10, l=10, r=10),
        paper_bgcolor='rgba(20, 30, 60, 0.4)', font={'family': 'Space Grotesk', 'color': '#f0f4f8'},
        plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark',
        plot_margin=dict(l=20, r=20, b=20, t=20)
    )
    return fig

# ════════════════════════════════════════════════════════════════════════════════
# FEATURE CONTRIBUTION CHART
# ════════════════════════════════════════════════════════════════════════════════
def make_contribution_chart(model, input_df):
    try:
        preprocessor = model.named_steps['preprocessing']
        lr = model.named_steps['model'].named_estimators_['lr']
        X_proc = preprocessor.transform(input_df)
        coefs = lr.coef_[0]
        contribs = X_proc[0] * coefs

        names = ['Age', 'Systolic_BP', 'Diastolic_BP', 'Pulse_Pressure', 'Total_Cholesterol',
                 'Glucose', 'BMI', 'CV_Risk_Score', 'Symptom_Burden', 'Gender',
                 'Pain_Arms_Jaw_Back', 'Shortness_of_Breath', 'Fatigue', 'Palpitations',
                 'Sedentary_Lifestyle', 'Smoking_Level', 'Clinical_Vulnerability',
                 'Ischemic_Signal', 'Chest_Pain_Weighted', 'Hypertension_Stage',
                 'Metabolic_Risk_Score', 'Age_Gender_Risk']

        display_names = {
            'Systolic_BP': 'Systolic BP', 'Diastolic_BP': 'Diastolic BP',
            'Pulse_Pressure': 'Pulse Pressure', 'Total_Cholesterol': 'Cholesterol',
            'Pain_Arms_Jaw_Back': 'Radiating Pain', 'Shortness_of_Breath': 'SOB',
            'Sedentary_Lifestyle': 'Sedentary', 'Smoking_Level': 'Smoking',
            'Clinical_Vulnerability': 'Vulnerability', 'Ischemic_Signal': 'Ischemic Signal',
            'Chest_Pain_Weighted': 'Chest Pain', 'Hypertension_Stage': 'HT Stage',
            'Metabolic_Risk_Score': 'Metabolic Risk', 'Age_Gender_Risk': 'Age-Gender Risk',
            'CV_Risk_Score': 'CV Risk'
        }

        n = min(len(names), len(contribs))
        vals = contribs[:n]
        disp = [display_names.get(names[i], names[i]) for i in range(n)]

        df = pd.DataFrame({'feature': disp, 'contribution': vals})
        df = df.reindex(df['contribution'].abs().sort_values(ascending=True).index)
        df = df.tail(14)

        colors = ['#FF1654' if v > 0 else '#00FF88' for v in df['contribution']]

        fig = go.Figure(go.Bar(
            x=df['contribution'], y=df['feature'], orientation='h',
            marker={'color': colors, 'line': {'color': 'rgba(255,255,255,0.2)', 'width': 1}},
            text=[f"{v:+.3f}" for v in df['contribution']], textposition='outside',
            textfont={'size': 10, 'family': 'JetBrains Mono', 'color': '#f0f4f8'},
            hovertemplate='<b>%{y}</b><br>Contribution: %{x:.3f}<extra></extra>'
        ))

        fig.update_layout(
            title={'text': '⚡ Feature Impact on Risk Score', 'font': {'size': 13, 'family': 'Space Grotesk', 'color': '#00D9FF'}},
            xaxis_title="Contribution →", yaxis_title="",
            height=420, margin=dict(t=40, b=40, l=10, r=60),
            paper_bgcolor='rgba(20, 30, 60, 0.4)', plot_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Outfit', 'size': 11, 'color': '#f0f4f8'},
            xaxis={'gridcolor': 'rgba(255,255,255,0.08)', 'zeroline': True, 'zerolinecolor': '#404040', 'zerolinewidth': 2},
            yaxis={'showgrid': False},
            shapes=[dict(type='line', x0=0, x1=0, y0=-0.5, y1=len(df)-0.5, line=dict(color='#404040', width=2))]
        )
        return fig
    except:
        return None

# ════════════════════════════════════════════════════════════════════════════════
# CLINICAL REASONING
# ════════════════════════════════════════════════════════════════════════════════
def get_clinical_reasoning(raw, computed, probability):
    reasons = []
    
    if computed['ischemic_signal'] == 1:
        reasons.append(('red', "🔴 ISCHEMIC SIGNAL ACTIVE — Chest pain + radiating arm/jaw/back pain = classic Angina Pectoris. URGENT cardiology."))
    elif raw['chest_pain']:
        reasons.append(('red', "🔴 Active chest pain — Primary acute cardiac indicator. Weighted 9× higher in AI algorithm."))
    
    if raw['shortness_of_breath'] and raw['palpitations']:
        reasons.append(('red', "🔴 Dyspnoea + Palpitations — Simultaneous breathlessness + irregular heartbeat indicates severe cardiac compromise."))
    elif raw['shortness_of_breath']:
        reasons.append(('amber', "⚠️ Shortness of breath — May indicate reduced cardiac output or pulmonary congestion from heart failure."))
    elif raw['palpitations']:
        reasons.append(('amber', "⚠️ Palpitations present — Irregular heartbeat is an independent CVD predictor."))
    
    if raw['fatigue']:
        reasons.append(('amber', "⚠️ Persistent fatigue — Strong association with reduced cardiac output. Model rank: 2nd most important feature."))
    
    if computed['ht_stage'] == 3:
        reasons.append(('red', f"🔴 Stage 2 Hypertension ({raw['systolic_bp']}/{raw['diastolic_bp']} mmHg) — SEVERE. Immediate BP control required."))
    elif computed['ht_stage'] == 2:
        reasons.append(('amber', f"⚠️ Stage 1 Hypertension ({raw['systolic_bp']}/{raw['diastolic_bp']}) — Above clinical threshold. Lifestyle modification critical."))
    elif computed['ht_stage'] == 1:
        reasons.append(('amber', f"⚠️ Elevated BP ({raw['systolic_bp']}/{raw['diastolic_bp']}) — Monitor closely. Reduce salt/stress."))
    
    if computed['metabolic_risk'] >= 2:
        reasons.append(('red' if computed['metabolic_risk'] == 3 else 'amber',
            f"{'🔴' if computed['metabolic_risk']==3 else '⚠️'} Metabolic Syndrome ({computed['metabolic_risk']}/3 criteria) — Major independent CVD risk cluster."))
    elif computed['metabolic_risk'] == 1:
        if raw['total_cholesterol'] >= 200:
            reasons.append(('amber', f"⚠️ Borderline high cholesterol ({raw['total_cholesterol']} mg/dL) — Contributes to atherosclerotic plaque."))
        elif raw['glucose'] >= 100:
            reasons.append(('amber', f"⚠️ Pre-diabetic glucose ({raw['glucose']} mg/dL) — Insulin resistance linked to CVD."))
        elif raw['bmi'] >= 25:
            reasons.append(('amber', f"⚠️ Overweight BMI ({raw['bmi']:.1f}) — Increases metabolic load."))
    
    if computed['age_gender_risk']:
        gender_str = "Men ≥ 45" if raw['gender'] == 1 else "Women ≥ 55"
        reasons.append(('amber', f"⚠️ {gender_str} — Framingham threshold. CVD risk accelerates significantly at this age."))
    
    if raw['sedentary_lifestyle'] and computed['smoking_level'] >= 2:
        reasons.append(('red', "🔴 Sedentary + Moderate/Heavy smoking — Dual chronic risk significantly compounds CVD burden."))
    elif raw['sedentary_lifestyle']:
        reasons.append(('amber', "⚠️ Sedentary lifestyle — #1 modifiable risk factor. Associated with obesity, HTN, insulin resistance."))
    elif computed['smoking_level'] >= 2:
        reasons.append(('amber', f"⚠️ {computed['smoking_text']} smoker — Direct arterial wall damage. Promotes thrombosis."))
    
    if computed['clinical_vuln'] == 2:
        reasons.append(('red', "🔴 High Clinical Vulnerability (Family Hx + Chronic Stress) — Hereditary + psychosocial compounding effect."))
    elif computed['clinical_vuln'] == 1:
        if raw['family_history']:
            reasons.append(('amber', "⚠️ Positive family history — Genetic predisposition increases lifetime CVD risk 40–60%."))
        else:
            reasons.append(('amber', "⚠️ Chronic stress — Elevated cortisol promotes inflammation and atherosclerosis."))
    
    if not raw['chest_pain'] and not raw['shortness_of_breath'] and not raw['fatigue'] and not raw['palpitations']:
        reasons.append(('green', "✅ NO acute symptoms — Strong protective signal. Low immediate cardiac risk."))
    if computed['ht_stage'] == 0:
        reasons.append(('green', f"✅ Optimal BP ({raw['systolic_bp']}/{raw['diastolic_bp']}) — Strong protective cardiovascular factor."))
    if computed['smoking_level'] == 0:
        reasons.append(('green', "✅ Non-smoker — Eliminates the #1 modifiable risk factor."))
    if raw['bmi'] < 25:
        reasons.append(('green', f"✅ Healthy BMI ({raw['bmi']:.1f}) — Normal body weight reduces metabolic stress."))
    
    return reasons

# ════════════════════════════════════════════════════════════════════════════════
# TRIAGE DETERMINATION
# ════════════════════════════════════════════════════════════════════════════════
def get_triage(probability, ischemic_signal):
    pct = probability * 100
    if pct > 70 and ischemic_signal:
        return '🚨 CRITICAL RISK', 'triage-critical'
    elif pct > 50 and ischemic_signal:
        return '⚠️ HIGH RISK', 'triage-high'
    elif pct > 50:
        return '⚠️ MODERATE RISK', 'triage-moderate'
    else:
        return '✅ LOW RISK', 'triage-low'

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 28px;'>
        <div style='font-size: 2.5rem; animation: pulse 2s infinite;'>🫀</div>
        <div style='font-size: 1.3rem; font-weight: 800; color: #00D9FF; margin: 12px 0; font-family: Space Grotesk;'>MaLCaDD</div>
        <div style='font-size: 0.75rem; color: #8892a6; text-transform: uppercase; letter-spacing: 1px;'>AI Diagnostic System</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<div class='section-title' style='margin: 0 -16px 16px -16px;'>👤 Demographics</div>", unsafe_allow_html=True)
    age = st.slider("Age", 20, 90, 55, help="Patient age in years")
    gender = st.selectbox("Gender", ["Female", "Male"])
    gender_val = 1 if gender == "Male" else 0

    st.markdown("<div class='section-title' style='margin: 16px -16px 16px -16px;'>💉 Blood Panel</div>", unsafe_allow_html=True)
    sbp = st.slider("Systolic BP", 80, 220, 130)
    dbp = st.slider("Diastolic BP", 50, 140, 85)
    chol = st.slider("Cholesterol", 100, 400, 210)
    glucose = st.slider("Glucose", 60, 400, 110)
    bmi = st.slider("BMI", 15.0, 50.0, 26.0, step=0.1)

    st.markdown("<div class='section-title' style='margin: 16px -16px 16px -16px;'>🚬 Lifestyle</div>", unsafe_allow_html=True)
    cigs = st.slider("Cigarettes/Day", 0, 60, 0)
    sedentary = st.checkbox("Sedentary Lifestyle")
    fam_hist = st.checkbox("Family History CVD")
    stress = st.checkbox("Chronic Stress")

    st.markdown("---")
    analyze = st.button("🫀 ANALYZE PATIENT", use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════════════════════════
model = load_model()
if not model:
    st.error("⚠️ Model not found")
    st.stop()

# HERO HEADER
st.markdown("""
<div class='hero-header'>
    <div class='hero-icon'>🫀</div>
    <div class='hero-title'>MaLCaDD</div>
    <div class='hero-subtitle'>AI-Powered Cardiovascular Risk Assessment System</div>
    <div class='hero-stats'>
        <div class='stat-badge'>94.04% Accuracy</div>
        <div class='stat-badge'>95.15% Sensitivity</div>
        <div class='stat-badge'>0.9851 ROC-AUC</div>
        <div class='stat-badge'>38.5K Patients</div>
    </div>
</div>
""", unsafe_allow_html=True)

# SYMPTOMS SECTION
st.markdown("<div class='section-title'>🩺 Acute Cardiac Symptoms</div>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: cp = st.checkbox("💔 Chest Pain")
with c2: sob = st.checkbox("😮‍💨 Breathless")
with c3: fat = st.checkbox("😴 Fatigue")
with c4: pal = st.checkbox("💓 Palpitations")
with c5: rad = st.checkbox("🦾 Radiating")

raw = {'age': age, 'gender': gender_val, 'systolic_bp': sbp, 'diastolic_bp': dbp,
       'total_cholesterol': chol, 'glucose': glucose, 'bmi': bmi, 'cigs_per_day': cigs,
       'sedentary_lifestyle': sedentary, 'family_history': fam_hist, 'chronic_stress': stress,
       'chest_pain': cp, 'shortness_of_breath': sob, 'fatigue': fat,
       'palpitations': pal, 'pain_arms_jaw_back': rad}

st.markdown("---")

with st.expander("📊 Computed Values", expanded=False):
    _, comp = engineer_features(raw)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Pulse Pressure", f"{comp['pulse_pressure']} mmHg")
    c2.metric("Symptom Burden", f"{comp['symptom_burden']}/5")
    c3.metric("HT Stage", comp['ht_text'])
    c4.metric("Met. Risk", f"{comp['metabolic_risk']}/3")
    c5.metric("Smoking", comp['smoking_text'])
    c6.metric("Ischemic Signal", "🔴 ACTIVE" if comp['ischemic_signal'] else "✅ Inactive")

if analyze:
    with st.spinner("⚡ Analysing..."):
        input_df, comp = engineer_features(raw)
        prob = model.predict_proba(input_df)[0][1]
        pred = model.predict(input_df)[0]
        
        triage_label, triage_css = get_triage(prob, comp['ischemic_signal'])
        reasons = get_clinical_reasoning(raw, comp, prob)

    st.markdown("---")
    st.markdown("<div class='section-title'>📋 DIAGNOSTIC RESULT</div>", unsafe_allow_html=True)

    c_gauge, c_stats, c_triage = st.columns([1.2, 1.4, 1.4])
    
    with c_gauge:
        st.plotly_chart(make_gauge(prob), use_container_width=True)
    
    with c_stats:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Risk Probability</div>
            <div class='metric-value'>{prob*100:.1f}<span class='metric-unit'>%</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class='metric-card' style='margin-top: 12px;'>
            <div class='metric-label'>Ischemic Signal</div>
            <div style='font-size: 1.4rem; font-weight: 700; color: {"#FF6B7A" if comp["ischemic_signal"] else "#00FF88"}; font-family: Space Grotesk;'>
                {'🔴 ACTIVE' if comp['ischemic_signal'] else '✅ Inactive'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c_triage:
        st.markdown(f"""
        <div class='triage-result {triage_css}'>
            <div class='triage-label'>{triage_label}</div>
            <div class='triage-detail'>Probability: {prob*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    if pred == 1 and prob > 0.5:
        st.markdown(f"""
        <div class='emergency-banner'>
            <div class='emergency-title'>🚨 CARDIOVASCULAR RISK DETECTED 🚨</div>
            <div class='emergency-text'>
                Risk Level: {prob*100:.1f}% {'| Ischemic Signal ACTIVE' if comp['ischemic_signal'] else ''}<br>
                <strong>⚠️ Contact cardiologist or visit hospital IMMEDIATELY</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>📊 Model Metrics</div>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.markdown("<div class='metric-card'><div class='metric-label'>Accuracy</div><div class='metric-value'>94.04%</div></div>", unsafe_allow_html=True)
    m2.markdown("<div class='metric-card'><div class='metric-label'>Sensitivity</div><div class='metric-value'>95.15%</div></div>", unsafe_allow_html=True)
    m3.markdown("<div class='metric-card'><div class='metric-label'>Specificity</div><div class='metric-value'>92.93%</div></div>", unsafe_allow_html=True)
    m4.markdown("<div class='metric-card'><div class='metric-label'>ROC-AUC</div><div class='metric-value'>0.9851</div></div>", unsafe_allow_html=True)
    m5.markdown("<div class='metric-card'><div class='metric-label'>Precision</div><div class='metric-value'>93.09%</div></div>", unsafe_allow_html=True)
    m6.markdown("<div class='metric-card'><div class='metric-label'>F1 Score</div><div class='metric-value'>0.9411</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>⚡ Feature Impact</div>", unsafe_allow_html=True)
    fig_contrib = make_contribution_chart(model, input_df)
    if fig_contrib:
        st.plotly_chart(fig_contrib, use_container_width=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>🩺 Clinical Reasoning</div>", unsafe_allow_html=True)
    for i, (tag, text) in enumerate(reasons):
        css = f'reason-tag reason-{tag}'
        st.markdown(f'<div class="{css}" style="animation-delay: {i*0.08}s">{text}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-title'>💊 Recommendation</div>", unsafe_allow_html=True)
    recs = {
        '🚨 CRITICAL RISK': ("EMERGENCY: Acute Ischemia", "Assume acute event. ECG + troponins + cardiology NOW."),
        '⚠️ HIGH RISK': ("Urgent Cardiology", "Resting ECG, stress test, echo within 48h."),
        '⚠️ MODERATE RISK': ("Scheduled Consultation", "Preventative care within 2 weeks. Lifestyle + BP."),
        '✅ LOW RISK': ("Routine Monitoring", "Maintain healthy lifestyle. Annual checkup."),
    }
    action, detail = recs.get(triage_label, ("Unknown", ""))
    st.markdown(f"""
    <div class='glass-card'>
        <div style='font-size: 1.1rem; font-weight: 700; color: #00D9FF; margin-bottom: 8px; font-family: Space Grotesk;'>{action}</div>
        <div style='color: #b0bec5; font-size: 0.95rem;'>{detail}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("⚕️ Disclaimer: MaLCaDD is a screening tool. Requires professional clinical interpretation. Air University | 2025")

else:
    st.markdown("""
    <div class='glass-card' style='text-align: center; padding: 80px 40px;'>
        <div style='font-size: 5rem; margin-bottom: 24px; animation: pulse 2s infinite;'>❤️</div>
        <h2 style='color: #00D9FF; font-size: 2rem; font-family: Space Grotesk; margin-bottom: 16px;'>Ready to Begin Assessment</h2>
        <p style='color: #b0bec5; font-size: 1rem; max-width: 600px; margin: 0 auto 32px;'>
            Enter patient data in the sidebar, select symptoms above, then click <strong>ANALYZE PATIENT</strong> for instant AI-powered risk assessment.
        </p>
    </div>
    """, unsafe_allow_html=True)