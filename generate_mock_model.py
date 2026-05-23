import pickle
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.pipeline import Pipeline

def main():
    print("Generating mock dataset for MaLCaDD_FINAL.pkl...")
    
    # Define exact feature groups as per requirements
    scaled_cols = [
        'Age', 'Systolic_BP', 'Diastolic_BP', 'Pulse_Pressure', 
        'Total_Cholesterol', 'Glucose', 'BMI', 'CV_Risk_Score', 'Symptom_Burden'
    ]
    
    passthrough_cols = [
        'Gender', 'Pain_Arms_Jaw_Back', 'Shortness_of_Breath', 'Fatigue', 
        'Palpitations', 'Sedentary_Lifestyle', 'Smoking_Level', 
        'Clinical_Vulnerability', 'Ischemic_Signal', 'Chest_Pain_Weighted', 
        'Hypertension_Stage', 'Metabolic_Risk_Score', 'Age_Gender_Risk'
    ]
    
    # Complete list of 22 features in order
    all_features = scaled_cols + passthrough_cols
    
    # Generate some mock data (100 samples)
    np.random.seed(42)
    n_samples = 100
    
    data = {}
    # Random values within reasonable ranges
    data['Age'] = np.random.randint(20, 90, size=n_samples)
    data['Systolic_BP'] = np.random.randint(80, 220, size=n_samples)
    data['Diastolic_BP'] = np.random.randint(50, 140, size=n_samples)
    data['Pulse_Pressure'] = data['Systolic_BP'] - data['Diastolic_BP']
    data['Total_Cholesterol'] = np.random.randint(100, 400, size=n_samples)
    data['Glucose'] = np.random.randint(60, 400, size=n_samples)
    data['BMI'] = np.random.uniform(15, 50, size=n_samples)
    data['Gender'] = np.random.randint(0, 2, size=n_samples) # 1=Male, 0=Female
    
    # Lifestyle & Symptoms
    data['Pain_Arms_Jaw_Back'] = np.random.randint(0, 2, size=n_samples)
    data['Shortness_of_Breath'] = np.random.randint(0, 2, size=n_samples)
    data['Fatigue'] = np.random.randint(0, 2, size=n_samples)
    data['Palpitations'] = np.random.randint(0, 2, size=n_samples)
    data['Sedentary_Lifestyle'] = np.random.randint(0, 2, size=n_samples)
    
    # Simple inputs for computed features
    cigs = np.random.randint(0, 60, size=n_samples)
    data['Smoking_Level'] = np.where(cigs == 0, 0, np.where(cigs <= 5, 1, np.where(cigs <= 15, 2, 3)))
    
    family_hist = np.random.randint(0, 2, size=n_samples)
    stress = np.random.randint(0, 2, size=n_samples)
    data['Clinical_Vulnerability'] = family_hist + stress
    
    chest_pain = np.random.randint(0, 2, size=n_samples)
    data['Ischemic_Signal'] = chest_pain * data['Pain_Arms_Jaw_Back']
    data['Chest_Pain_Weighted'] = chest_pain * 3.0
    
    # Symptoms burden: sum of chest_pain, shortness_of_breath, fatigue, palpitations, radiating
    data['Symptom_Burden'] = (chest_pain + data['Shortness_of_Breath'] + 
                              data['Fatigue'] + data['Palpitations'] + 
                              data['Pain_Arms_Jaw_Back'])
    
    # Hypertension Stage (0-3 ordinal, AHA 2017)
    sbp = data['Systolic_BP']
    dbp = data['Diastolic_BP']
    ht_stage = []
    for s, d in zip(sbp, dbp):
        if s >= 140 or d >= 90:
            ht_stage.append(3)
        elif (130 <= s <= 139) or (80 <= d <= 89):
            ht_stage.append(2)
        elif (120 <= s <= 129) and d < 80:
            ht_stage.append(1)
        else:
            ht_stage.append(0)
    data['Hypertension_Stage'] = np.array(ht_stage)
    
    # Metabolic Risk Score
    data['Metabolic_Risk_Score'] = (
        (data['BMI'] >= 25).astype(int) + 
        (data['Glucose'] >= 100).astype(int) + 
        (data['Total_Cholesterol'] >= 200).astype(int)
    )
    
    # Age Gender Risk
    data['Age_Gender_Risk'] = np.where(
        ((data['Gender'] == 1) & (data['Age'] >= 45)) | 
        ((data['Gender'] == 0) & (data['Age'] >= 55)), 
        1, 0
    )
    
    # CV Risk Score (0-15)
    cv_score = []
    for a, h_stg, smk, chol, gluc, b in zip(data['Age'], data['Hypertension_Stage'], 
                                            data['Smoking_Level'], data['Total_Cholesterol'], 
                                            data['Glucose'], data['BMI']):
        score = 0
        if a >= 70: score += 4
        elif a >= 60: score += 3
        elif a >= 50: score += 2
        elif a >= 40: score += 1
        score += h_stg
        score += smk
        if chol >= 240: score += 2
        elif chol >= 200: score += 1
        if gluc >= 126: score += 2
        elif gluc >= 100: score += 1
        if b >= 30: score += 1
        cv_score.append(min(score, 15))
    data['CV_Risk_Score'] = np.array(cv_score)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Rearrange in the exact expected order
    df = df[all_features]
    
    # Generate labels (1 = CVD risk, 0 = no CVD risk)
    # We base it on CV Risk Score and symptoms to make the model training somewhat logical
    probability = (df['CV_Risk_Score'] / 15.0) * 0.7 + (df['Ischemic_Signal'] * 0.3)
    y = np.where(probability > 0.4, 1, 0)
    
    # Define ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('scaler', StandardScaler(), scaled_cols),
            ('passthrough', 'passthrough', passthrough_cols)
        ]
    )
    
    # Define VotingClassifier with LogisticRegression and KNN
    # KNeighborsClassifier must use weights='uniform' or 'distance', standard defaults
    voting_clf = VotingClassifier(
        estimators=[
            ('lr', LogisticRegression(max_iter=1000, random_state=42)),
            ('knn', KNeighborsClassifier(n_neighbors=5))
        ],
        voting='soft'
    )
    
    # Assemble Pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', voting_clf)
    ])
    
    # Fit the pipeline
    pipeline.fit(df, y)
    print("Model successfully trained on dummy data.")
    
    # Save the model pipeline to MaLCaDD_FINAL.pkl
    model_filename = 'MaLCaDD_FINAL.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(pipeline, f)
        
    print(f"Saved trained model to {model_filename}")

if __name__ == '__main__':
    main()
