import streamlit as st
import joblib
import pandas as pd
from utils import set_background

st.set_page_config(page_title="Results - PPD Predictor", layout="wide")
set_background("assets/background.png")

if "answers" in st.session_state and len(st.session_state.answers) == 10:
    score = sum(st.session_state.answers)
    model = joblib.load("model/ppd_model_pipeline.pkl")
    le = joblib.load("model/label_encoder.pkl")

    input_data = pd.DataFrame([{**{f"Q{i+1}": val for i, val in enumerate(st.session_state.answers)}, "Age": 28, "FamilySupport": "Medium", "EPDS_Score": score}])

    prediction_encoded = model.predict(input_data)[0]
    prediction_label = le.inverse_transform([prediction_encoded])[0]

    st.subheader("🎯 Prediction Result")
    st.markdown(f"### **Your Risk Level: {prediction_label}**")
    st.progress(score / 30)
else:
    st.warning("Please complete the questionnaire first.")
