
   import streamlit as st

st.set_page_config(page_title="PPD Predictor - Home", layout="wide")

st.title("🧠 Postpartum Depression Predictor")
st.image("assets/mom_baby.png", width=250)

st.markdown("This tool helps assess postpartum depression risk based on the **Edinburgh Postnatal Depression Scale (EPDS)**.")

name = st.text_input("Your Name")
age = st.slider("Age", 18, 45, 28)
pregnant = st.radio("Are you currently pregnant?", ["Yes", "No"])
recent_birth = st.radio("Have you recently given birth?", ["Yes", "No"])
family_support = st.selectbox("How would you rate your family support?", ["High", "Medium", "Low"])

if st.button("Start Questionnaire"):
    if not name.strip():
        st.warning("Please enter your name before starting.")
    else:
        st.session_state.user_data = {
            "Name": name.strip(),
            "Age": age,
            "Pregnant": pregnant,
            "RecentBirth": recent_birth,
            "FamilySupport": family_support
        }
        st.session_state.answers = []
        st.session_state.q_index = 0
        st.switch_page("pages/2_Questionnaire.py")
