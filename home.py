import streamlit as st

# Set page config
st.set_page_config(page_title="PPD App", layout="wide")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation logic
def go_to(page_name):
    st.session_state.page = page_name

# HOME PAGE
def show_home():
    st.title("🧠 Postpartum Depression Predictor")
    st.markdown("Welcome to the Postpartum Depression Predictor!")
    st.image("assets/mom_baby.png", width=250)
    st.markdown("👉 Click below to begin the questionnaire")
    if st.button("Start Questionnaire"):
        go_to("questionnaire")

# QUESTIONNAIRE PAGE
def show_questionnaire():
    st.header("📝 Questionnaire")
    st.markdown("Please answer the following questions:")

    # Sample question (you can expand this)
    answer = st.radio("Q1: Have you felt down or depressed recently?", 
                      ["Not at all", "Several days", "Nearly every day"])

    if st.button("Submit & View Result"):
        go_to("result")

# RESULT PAGE
def show_result():
    st.header("🎯 Prediction Result")
    st.markdown("Based on your answers, here is your result:")
    st.success("🔵 Risk Level: Mild")  # (Replace with actual prediction)
    if st.button("Back to Home"):
        go_to("home")

# Route to correct page
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "questionnaire":
    show_questionnaire()
elif st.session_state.page == "result":
    show_result()
