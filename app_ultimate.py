# -*- coding: utf-8 -*-
import os
import pickle
import numpy as np
import pandas as pd
import streamlit as st
# Configure Page Settings - MUST BE FIRST STREAMLIT CALL
st.set_page_config(
    page_title="MaLCaDD - CVD Diagnosis CDSS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to render clean HTML in Streamlit (prevents markdown code blocks)
def st_html(html_content: str):
    cleaned = "".join(line.strip() for line in html_content.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)

# Custom EMR Medical Light CSS Styling
st_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    
    .app-title-container {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.025);
    }
    
    .app-title {
        color: #1E3A8A;
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .app-subtitle {
        color: #64748B;
        font-size: 1rem;
        margin-top: 0.2rem;
        font-weight: 400;
    }
    
    .performance-banner {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.025);
    }
    
    .banner-title {
        color: #1E3A8A;
        font-family: 'Outfit', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 0.5rem;
    }
    
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        transition: all 0.2s ease-in-out;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border-color: #CBD5E1;
    }
    
    .metric-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: #2563EB;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.2px;
        margin-top: 0.15rem;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #1E3A8A;
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0.25rem;
        margin-top: 1rem;
    }
    
    .card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.025);
    }
    
    .card-title {
        color: #1E3A8A;
        font-family: 'Outfit', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 0.5rem;
    }
    
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
    .triage-critical {
        background-color: #FEF2F2;
        border-left-color: #EF4444;
        color: #991B1B;
    }
    .triage-high {
        background-color: #FFF7ED;
        border-left-color: #F97316;
        color: #9A3412;
    }
    .triage-moderate {
        background-color: #FEF3C7;
        border-left-color: #D97706;
        color: #92400E;
    }
    .triage-low {
        background-color: #ECFDF5;
        border-left-color: #10B981;
        color: #065F46;
    }
    
    .gauge-wrapper {
        margin: 1.5rem 0;
    }
    
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
        width: 100%;
        border: 1px solid #CBD5E1;
    }
    
    .gauge-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .reasoning-list {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
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
    .reasoning-list li strong {
        color: #0F172A;
    }
    
    .var-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin-top: 0.5rem;
    }
    
    .var-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: left;
    }
    
    .var-label {
        font-size: 0.75rem;
        color: #64748B;
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
</style>
""")


# Helper function to auto-generate mock model if missing
def generate_mock_model_file():
    from generate_mock_model import main as train_mock
    try:
        train_mock()
        return True
    except Exception as e:
        st.error(f"Error auto-generating model pipeline: {str(e)}")
        return False

# Model Loading logic with multiple options
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
                
    # Fallback: Auto-generate the model if not found
    if loaded_model is None:
        st.warning("Model file not found. Auto-generating a clinical-signature matching VotingClassifier pipeline...")
        if generate_mock_model_file():
            # Try loading again
            try:
                with open('MaLCaDD_FINAL.pkl', 'rb') as f:
                    loaded_model = pickle.load(f)
            except Exception as e:
                st.error(f"Failed to load newly generated model: {str(e)}")
        else:
            st.error(f"Could not load or generate model. Searched paths: {searched_paths}")
            
    return loaded_model

# Load model
model = load_model()

# Title Container
st_html("""
<div class="app-title-container">
    <div class="app-title">MaLCaDD</div>
    <div class="app-subtitle">Machine Learning Cardiovascular Disease Diagnosis &mdash; Clinical Decision Support System</div>
</div>
""")

# Performance Banner Row
st_html("""
<div class="performance-banner">
    <div class="banner-title">Final Model Performance Benchmarks</div>
    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 1rem;">
        <div class="metric-card">
            <div class="metric-value">94.04%</div>
            <div class="metric-label">Accuracy</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">95.15%</div>
            <div class="metric-label">Sensitivity</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">92.93%</div>
            <div class="metric-label">Specificity</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">0.9851</div>
            <div class="metric-label">ROC-AUC</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">93.09%</div>
            <div class="metric-label">Precision</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">94.11%</div>
            <div class="metric-label">F1 Score</div>
        </div>
    </div>
</div>
""")

# Collect User Inputs in Sidebar
st.sidebar.markdown("## Patient Profile Details")

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
radiating_pain = 1 if st.sidebar.checkbox("Radiating Pain (Arms/Jaw/Back)") else 0 # Pain_Arms_Jaw_Back

# --- FEATURE ENGINEERING ---

# 1. Smoking_Level (ordinal 0-3)
if cigs_per_day == 0:
    smoking_level = 0
elif cigs_per_day <= 5:
    smoking_level = 1
elif cigs_per_day <= 15:
    smoking_level = 2
else:
    smoking_level = 3

# 2. Clinical_Vulnerability (0-2 ordinal)
clinical_vulnerability = family_history + chronic_stress

# 3. Ischemic_Signal (binary interaction)
ischemic_signal = chest_pain * radiating_pain

# 4. Chest_Pain_Weighted
chest_pain_weighted = chest_pain * 3.0

# 5. Pulse_Pressure
pulse_pressure = sbp - dbp

# 6. Symptom_Burden
symptom_burden = chest_pain + shortness_of_breath + fatigue + palpitations + radiating_pain

# 7. Hypertension_Stage (0-3 ordinal, AHA 2017)
if sbp >= 140 or dbp >= 90:
    hypertension_stage = 3
elif (130 <= sbp <= 139) or (80 <= dbp <= 89):
    hypertension_stage = 2
elif (120 <= sbp <= 129) and dbp < 80:
    hypertension_stage = 1
else:
    hypertension_stage = 0

# 8. Metabolic_Risk_Score (0-3)
metabolic_risk_score = int(bmi >= 25) + int(glucose >= 100) + int(cholesterol >= 200)

# 9. Age_Gender_Risk (binary)
age_gender_risk = 1 if ((gender == 1 and age >= 45) or (gender == 0 and age >= 55)) else 0

# 10. CV_Risk_Score (auto-computed 0-15)
cv_risk_score = 0
# Age score component
if age >= 70:
    cv_risk_score += 4
elif age >= 60:
    cv_risk_score += 3
elif age >= 50:
    cv_risk_score += 2
elif age >= 40:
    cv_risk_score += 1

# Hypertension component
cv_risk_score += hypertension_stage

# Smoking component
cv_risk_score += smoking_level

# Cholesterol component
if cholesterol >= 240:
    cv_risk_score += 2
elif cholesterol >= 200:
    cv_risk_score += 1

# Glucose component
if glucose >= 126:
    cv_risk_score += 2
elif glucose >= 100:
    cv_risk_score += 1

# BMI component
if bmi >= 30:
    cv_risk_score += 1

# Cap at 15
cv_risk_score = min(cv_risk_score, 15)


# --- MAIN SCREEN LAYOUT ---

# Initialize session state for diagnosis state
if 'diagnosed' not in st.session_state:
    st.session_state.diagnosed = False

# Sidebar Action Button
st.sidebar.markdown("---")
if not st.session_state.diagnosed:
    st.sidebar.markdown("<p style='font-size:0.85rem; color:#64748B; text-align:center;'>Double-check patient parameters before diagnostic execution.</p>", unsafe_allow_html=True)
    run_diagnosis_sidebar = st.sidebar.button("\U0001f52c Run Diagnostic Assessment", use_container_width=True, type="primary", key="sidebar_run")
    if run_diagnosis_sidebar:
        st.session_state.diagnosed = True
        st.rerun()
else:
    st.sidebar.markdown("<p style='font-size:0.85rem; color:#64748B; text-align:center;'>Clear current diagnostic results to process a new patient.</p>", unsafe_allow_html=True)
    reset_diagnosis_sidebar = st.sidebar.button("\U0001f504 Reset Diagnostic", use_container_width=True, type="secondary", key="sidebar_reset")
    if reset_diagnosis_sidebar:
        st.session_state.diagnosed = False
        st.rerun()

# Main screen routing
if not st.session_state.diagnosed:
    st_html("""
    <div class="card" style="padding: 2.5rem; text-align: center; border-radius: 12px; border: 1px solid #E2E8F0; background-color: #FFFFFF; margin-top: 1rem; margin-bottom: 1.5rem;">
        <div style="font-size: 3.5rem; margin-bottom: 1rem;">\U0001f52c</div>
        <h3 style="color: #1E3A8A; font-family: 'Outfit', sans-serif; margin-top: 0; margin-bottom: 0.75rem; font-size: 1.6rem; font-weight: 700;">
            Awaiting Patient Parameters
        </h3>
        <p style="color: #475569; font-size: 1rem; max-width: 600px; margin: 0 auto 1.5rem auto; line-height: 1.6;">
            This Clinical Decision Support System uses an ensemble machine learning voting classifier to calculate the likelihood of cardiovascular disease.
        </p>
        <div style="background-color: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 8px; padding: 1.5rem; display: inline-block; text-align: left; max-width: 550px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.01); margin-bottom: 0.5rem;">
            <span style="color: #1E3A8A; font-weight: 700; font-size: 0.95rem; text-transform: uppercase; display: block; margin-bottom: 0.75rem; letter-spacing: 0.5px;">Workflow Instructions:</span>
            <ol style="margin: 0; padding-left: 1.25rem; color: #475569; font-size: 0.95rem; line-height: 1.5;">
                <li style="margin-bottom: 0.5rem;">Input patient demographics and blood panel measurements in the sidebar.</li>
                <li style="margin-bottom: 0.5rem;">Select active symptom presentations and lifestyle factors.</li>
                <li>Click the <strong>Run Diagnostic Assessment</strong> button below to calculate results.</li>
            </ol>
        </div>
    </div>
    """)
    
    # Large, prominent button in the main screen area
    if st.button("\U0001f52c Run Diagnostic Assessment", key="main_run", type="primary", use_container_width=True):
        st.session_state.diagnosed = True
        st.rerun()
else:
    col_results, col_metrics = st.columns([3, 2])

    # Prediction Step
    if model is not None:
        # 22 columns in exact training order
        feature_order = [
            'Age', 'Systolic_BP', 'Diastolic_BP', 'Pulse_Pressure', 
            'Total_Cholesterol', 'Glucose', 'BMI', 'CV_Risk_Score', 'Symptom_Burden',
            'Gender', 'Pain_Arms_Jaw_Back', 'Shortness_of_Breath', 'Fatigue', 
            'Palpitations', 'Sedentary_Lifestyle', 'Smoking_Level', 
            'Clinical_Vulnerability', 'Ischemic_Signal', 'Chest_Pain_Weighted', 
            'Hypertension_Stage', 'Metabolic_Risk_Score', 'Age_Gender_Risk'
        ]
        
        input_data = pd.DataFrame([{
            'Age': age,
            'Systolic_BP': sbp,
            'Diastolic_BP': dbp,
            'Pulse_Pressure': pulse_pressure,
            'Total_Cholesterol': cholesterol,
            'Glucose': glucose,
            'BMI': bmi,
            'CV_Risk_Score': cv_risk_score,
            'Symptom_Burden': symptom_burden,
            'Gender': gender,
            'Pain_Arms_Jaw_Back': radiating_pain, # maps to Pain_Arms_Jaw_Back
            'Shortness_of_Breath': shortness_of_breath,
            'Fatigue': fatigue,
            'Palpitations': palpitations,
            'Sedentary_Lifestyle': sedentary_lifestyle,
            'Smoking_Level': smoking_level,
            'Clinical_Vulnerability': clinical_vulnerability,
            'Ischemic_Signal': ischemic_signal,
            'Chest_Pain_Weighted': chest_pain_weighted,
            'Hypertension_Stage': hypertension_stage,
            'Metabolic_Risk_Score': metabolic_risk_score,
            'Age_Gender_Risk': age_gender_risk
        }])
        
        # Enforce column ordering
        input_data = input_data[feature_order]
        
        # Predict Probability
        prob = model.predict_proba(input_data)[0][1]
        
        # Risk Stratification & Triage
        if prob > 0.70 and ischemic_signal == 1:
            risk_class = "CRITICAL"
            risk_color = "#EF4444" # Critical Risk: Red
            triage_style = "triage-critical"
            triage_icon = "\U0001f6a8"
        elif prob > 0.50 and ischemic_signal == 1:
            risk_class = "HIGH"
            risk_color = "#F97316" # High Risk: Orange
            triage_style = "triage-high"
            triage_icon = "\u26a0\ufe0f"
        elif prob > 0.50:
            risk_class = "MODERATE"
            risk_color = "#D97706" # Moderate Risk: Amber
            triage_style = "triage-moderate"
            triage_icon = "\u26a0\ufe0f"
        else:
            risk_class = "LOW"
            risk_color = "#10B981" # Success/Low Risk: Green
            triage_style = "triage-low"
            triage_icon = "\u2705"
            
        with col_results:
            st_html(f"""
            <div class="card">
                <div class="card-title">CVD Diagnostic Assessment</div>
                
                <div class="triage-box {triage_style}">
                    <span>{triage_icon}</span>
                    <span>TRIAGE STATUS: {risk_class} RISK ({prob*100:.1f}%)</span>
                </div>
                
                <div class="gauge-wrapper">
                    <div class="gauge-label">
                        <span>Cardiovascular Disease Risk Probability</span>
                        <span>{prob*100:.1f}%</span>
                    </div>
                    <div class="gauge-track">
                        <div class="gauge-fill" style="width: {prob*100:.1f}%; background-color: {risk_color};"></div>
                    </div>
                </div>
                <div style="font-size: 0.85rem; color: #059669; margin-top: 0.5rem; text-align: right; font-style: italic; font-weight: 600;">
                    \u26a1 Real-time prediction active. Adjusting parameters in the sidebar will update results instantly.
                </div>
            </div>
            """)
            
            # Clinical Reasoning
            reasons = []
            
            # Age
            if age >= 70:
                reasons.append("<strong>Advanced age (&ge; 70)</strong>: Significantly increases cardiovascular baseline vulnerability (+4 pts).")
            elif age >= 60:
                reasons.append("<strong>Senior age (60-69)</strong>: Contributes to increased risk scoring (+3 pts).")
            elif age >= 50:
                reasons.append("<strong>Middle-to-senior age (50-59)</strong>: Contributes to risk scoring (+2 pts).")
                
            # BP
            if hypertension_stage == 3:
                reasons.append(f"<strong>Hypertension Stage 2</strong>: Highly elevated vascular pressure detected (SBP: {sbp} mmHg / DBP: {dbp} mmHg).")
            elif hypertension_stage == 2:
                reasons.append(f"<strong>Hypertension Stage 1</strong>: Elevated vascular pressure detected (SBP: {sbp} mmHg / DBP: {dbp} mmHg).")
            elif hypertension_stage == 1:
                reasons.append(f"<strong>Elevated Blood Pressure</strong>: Mildly elevated vascular pressure detected (SBP: {sbp} mmHg / DBP: {dbp} mmHg).")
                
            # Pulse Pressure
            if pulse_pressure >= 60:
                reasons.append(f"<strong>Widened Pulse Pressure ({pulse_pressure} mmHg)</strong>: Suggests potential arterial stiffness (normal: 40-50).")
                
            # Lipids / Metabolic
            if cholesterol >= 240:
                reasons.append(f"<strong>Severely elevated Total Cholesterol ({cholesterol} mg/dL)</strong>: Poses high hypercholesterolemia risk.")
            elif cholesterol >= 200:
                reasons.append(f"<strong>Elevated Total Cholesterol ({cholesterol} mg/dL)</strong>: Promotes atherogenesis.")
                
            if glucose >= 126:
                reasons.append(f"<strong>Diabetic-range fasting Glucose ({glucose} mg/dL)</strong>: Indicates elevated metabolic cardiovascular distress.")
            elif glucose >= 100:
                reasons.append(f"<strong>Pre-diabetic fasting Glucose ({glucose} mg/dL)</strong>: Contributes to overall metabolic burden.")
                
            if bmi >= 30:
                reasons.append(f"<strong>Obese BMI class ({bmi:.1f} kg/m&sup2;)</strong>: Accelerates metabolic stress and mechanical workload on the heart.")
            elif bmi >= 25:
                reasons.append(f"<strong>Overweight BMI class ({bmi:.1f} kg/m&sup2;)</strong>: Contributes mildly to metabolic risk.")
                
            # Lifestyle
            if smoking_level >= 2:
                reasons.append(f"<strong>Active heavy smoking ({cigs_per_day} cigs/day)</strong>: Severely damages vascular endothelium and increases thrombogenicity.")
            elif smoking_level == 1:
                reasons.append(f"<strong>Active light smoking ({cigs_per_day} cigs/day)</strong>: Contributes to endothelial stress.")
                
            if sedentary_lifestyle:
                reasons.append("<strong>Sedentary lifestyle</strong>: Associated with reduced vascular elasticity and aerobic deconditioning.")
                
            if clinical_vulnerability >= 2:
                reasons.append("<strong>High clinical vulnerability</strong>: Compounding risk from positive family history and chronic stress.")
            elif family_history:
                reasons.append("<strong>Positive family history of CVD</strong>: Suggests inherited genetic susceptibility.")
                
            # Symptoms & Signals
            if ischemic_signal:
                reasons.append("<span style='color: #EF4444; font-weight: 700;'>\U0001f6a8 ACTIVE ISCHEMIC SIGNAL</span>: Co-presentation of chest pain and radiating pain (arms/jaw/back). Requires immediate ECG and triage.")
            elif chest_pain:
                reasons.append("<strong>Active chest pain reported</strong>: Major subjective indicator requiring cardiac ischemia evaluation.")
                
            if symptom_burden >= 3:
                reasons.append(f"<strong>High symptom burden ({symptom_burden}/5 active symptoms)</strong>: Points to acute clinical presentation.")
                
            # Fallback if low risk
            if not reasons:
                reasons.append("No major clinical risk markers or symptoms are currently active. Continue regular screenings.")

            # Build list html
            list_items = "".join([f"<li>{r}</li>" for r in reasons])
            
            st_html(f"""
            <div class="card">
                <div class="card-title">Clinical Reasoning & Risk Factor Breakdown</div>
                <p style="font-size: 0.95rem; color: #475569; margin-bottom: 0.5rem;">
                    The diagnostic ensemble model processed 22 parameters. The following patient factors contributed to this risk stratification:
                </p>
                <ul class="reasoning-list">
                    {list_items}
                </ul>
            </div>
            """)

        with col_metrics:
            # Diagnostic Parameters Grid
            st_html(f"""
            <div class="card">
                <div class="card-title">Engineered Clinical Indicators</div>
                <div class="var-grid">
                    <div class="var-card">
                        <div class="var-label">CV Risk Score (0-15)</div>
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
                        <div class="var-label">Metabolic Risk Score (0-3)</div>
                        <div class="var-value">{metabolic_risk_score} / 3</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Symptom Burden (0-5)</div>
                        <div class="var-value">{symptom_burden} / 5</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Smoking Level (0-3)</div>
                        <div class="var-value">Level {smoking_level}</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Clinical Vulnerability (0-2)</div>
                        <div class="var-value">{clinical_vulnerability} / 2</div>
                    </div>
                    <div class="var-card">
                        <div class="var-label">Ischemic Signal</div>
                        <div class="var-value">{"Active" if ischemic_signal == 1 else "Inactive"}</div>
                    </div>
                </div>
            </div>
            """)
            
            # Clinical Recommendations
            if risk_class == "CRITICAL":
                recommendations_html = """
                <li><strong>Immediate action required</strong>: Order 12-lead ECG, cardiac enzymes (Troponin), and consult Cardiology stat.</li>
                <li>Patient exhibits active ischemic symptoms with high model probability.</li>
                <li>Initiate continuous telemetry monitoring and secure intravenous access.</li>
                """
            elif risk_class == "HIGH":
                recommendations_html = """
                <li><strong>Urgent evaluation needed</strong>: Refer to Cardiology for stress testing or echocardiogram within 24-48 hours.</li>
                <li>Active ischemic symptoms present. Optimize medical management (e.g. antiplatelet, lipid-lowering therapies).</li>
                <li>Recommend strict monitoring of blood pressure and avoidance of heavy physical exertion.</li>
                """
            elif risk_class == "MODERATE":
                recommendations_html = """
                <li><strong>Primary care follow-up</strong>: Scheduled outpatient appointment to review metabolic profile and lifestyle risk factors.</li>
                <li>Address elevated lipids, blood glucose, or blood pressure. Consider starting pharmacological controls.</li>
                <li>Patient counseling on diet (DASH diet), physical activity, and smoking cessation.</li>
                """
            else:
                recommendations_html = """
                <li><strong>Routine surveillance</strong>: Re-evaluate during annual physical.</li>
                <li>Maintain healthy lifestyle choices. Encouraging smoking cessation if applicable.</li>
                <li>Review vitals and lipid panel during standard interval check-ups.</li>
                """
                
            st_html(f"""
            <div class="card">
                <div class="card-title">Recommended Clinical Pathway</div>
                <ul class="reasoning-list">
                    {recommendations_html}
                </ul>
            </div>
            """)
    else:
        st.error("No model pipeline could be loaded. Please ensure MaLCaDD_FINAL.pkl is present in the application folder.")
