import streamlit as st
import base64
import pandas as pd
import joblib

# Load ML model & label encoder
model = joblib.load("model/ppd_model_pipeline.pkl")
le = joblib.load("model/label_encoder.pkl")

# Background setup
@st.cache_data(show_spinner=False)
def get_base64_bg(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_file):
    bg = get_base64_bg(image_file)
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("assets/background.png")

# Setup page
st.set_page_config(page_title="PPD Predictor", layout="wide")

# Session state init
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "answers" not in st.session_state:
    st.session_state.answers = []
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# Question list
questions = [
    ("I have been able to laugh and see the funny side of things", ["As much as I always could", "Not quite so much now", "Definitely not so much now", "Not at all"]),
    ("I have looked forward with enjoyment to things", ["As much as I ever did", "Rather less than I used to", "Definitely less than I used to", "Hardly at all"]),
    ("I have blamed myself unnecessarily when things went wrong", ["No, never", "Not very often", "Yes, some of the time", "Yes, most of the time"]),
    ("I have been anxious or worried for no good reason", ["No, not at all", "Hardly ever", "Yes, sometimes", "Yes, very often"]),
    ("I have felt scared or panicky for no very good reason", ["No, not at all", "No, not much", "Yes, sometimes", "Yes, quite a lot"]),
    ("Things have been getting on top of me", ["No, I have been coping as well as ever", "No, most of the time I have coped quite well", "Yes, sometimes I haven't been coping as well", "Yes, most of the time I haven't been able to cope at all"]),
    ("I have been so unhappy that I have had difficulty sleeping", ["No, not at all", "Not very often", "Yes, sometimes", "Yes, most of the time"]),
    ("I have felt sad or miserable", ["No, not at all", "Not very often", "Yes, quite often", "Yes, most of the time"]),
    ("I have been so unhappy that I have been crying", ["No, never", "Only occasionally", "Yes, quite often", "Yes, most of the time"]),
    ("The thought of harming myself has occurred to me", ["Never", "Hardly ever", "Sometimes", "Yes, quite often"])
]
score_map = {0: 0, 1: 1, 2: 2, 3: 3}

# =============================
# SECTION 1: HOME (User Inputs)
# =============================
if st.session_state.page == "home":
    st.image("assets/mom_baby.png", width=200)
    st.markdown("<h1 style='text-align:center;'>🧠 Postpartum Depression Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>A supportive step-by-step mental health check 🌸</h4>", unsafe_allow_html=True)

    name = st.text_input("Your Name")
    age = st.slider("Age", 18, 45, 28)
    pregnant = st.radio("Are you currently pregnant?", ["Yes", "No"])
    recent_birth = st.radio("Have you given birth recently?", ["Yes", "No"])
    family_support = st.selectbox("How would you rate your family support?", ["High", "Medium", "Low"])

    if st.button("Start Questionnaire"):
        if not name.strip():
            st.warning("Please enter your name before continuing.")
        else:
            st.session_state.user_data = {
                "Name": name.strip(),
                "Age": age,
                "Pregnant": pregnant,
                "RecentBirth": recent_birth,
                "FamilySupport": family_support
            }
            st.session_state.page = "questionnaire"
            st.rerun()
