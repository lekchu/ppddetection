import streamlit as st
import joblib

# Load model once and share with all pages
if 'model' not in st.session_state:
    st.session_state.model = joblib.load("model/ppd_model_pipeline.pkl")
if 'le' not in st.session_state:
    st.session_state.le = joblib.load("model/label_encoder.pkl")

# Initialize session values
if 'demographics' not in st.session_state:
    st.session_state.demographics = {
        'Age': 25,
        'is_pregnant': "Select...",
        'has_given_birth_recently': "Select...",
        'FamilySupport': "Select..."
    }
if 'epds_answers' not in st.session_state:
    st.session_state.epds_answers = {f"Q{i}": None for i in range(1, 11)}
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
