import streamlit as st
import base64
import joblib
import pandas as pd

# Load model
model = joblib.load("model/ppd_model_pipeline.pkl")
le = joblib.load("model/label_encoder.pkl")

# Set page config
st.set_page_config(page_title="Postpartum Depression Predictor", layout="wide")

# Background styling
@st.cache_data(show_spinner=False)
def get_base64_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

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

# Session state init
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "answers" not in st.session_state:
    st.session_state.answers = []
if "q_index" not in st.session_state:
    st.session_state.q_index = 0

# Routing function
def go_to(page):
    st.session_state.page = page

# INTRO PAGE
if st.session_state.page == "intro":
    st.image("assets/mom_baby.png", width=200)
    st.title("🧠 Postpartum Depression Predictor")
    st.markdown("""
        Welcome to the Postpartum Depression Predictor 🌸

        This tool helps assess postpartum depression risk based on your responses to simple personal and emotional questions.
    """)

    with st.form("intro_form"):
        name = st.text_input("Your Name")
        age = st.slider("Age", 18, 45, 28)
        pregnant = st.radio("Are you currently pregnant?", ["Yes", "No"])
        recent_birth = st.radio("Have you given birth recently?", ["Yes", "No"])
        family_support = st.selectbox("How would you rate your family support?", ["High", "Medium", "Low"])
        submitted = st.form_submit_button("Start Questionnaire")

        if submitted:
    st.session_state.user_data = {
        "Name": name,
        "Age": age,
        "Pregnant": pregnant,
        "RecentBirth": recent_birth,
        "FamilySupport": family_support
    }
    st.session_state.page = "questionnaire"
    st.experimental_rerun()

            }
            go_to("questionnaire")
