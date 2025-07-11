import streamlit as st
from utils import set_background

st.set_page_config(page_title="Home - PPD Predictor", page_icon="🧠", layout="wide")
set_background("assets/background.png")

st.image("assets/mom_baby.png", width=250)
st.title("🧠 Postpartum Depression Predictor")
st.markdown("""
Welcome to the Postpartum Depression Predictor! 🌸

This application helps assess your mental well-being after childbirth using a simple questionnaire.

👉 Navigate to the **Questionnaire** tab to begin.
""")
