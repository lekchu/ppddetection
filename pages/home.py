import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
from utils import set_page_style

set_page_style()
st.set_page_config(page_title="PPD Risk Predictor", layout="wide")

st.title("Welcome to the PPD Risk Predictor 🏡")

try:
    st.image("assets/mom_baby.png", width=300, caption="Supporting new mothers and families")
except Exception:
    st.warning("💡 Add 'assets/mom_baby.png' for the header image.")

st.markdown("""
### Understand Your Well-being 🌟

This tool uses the **Edinburgh Postnatal Depression Scale (EPDS)** and machine learning to help screen postpartum emotional health.

**You’ll get:**
- 10-question emotional check
- Personalized risk score
- Confidential guidance
""")

st.write("---")
st.subheader("Ready to Begin?")

if st.button("Start Questionnaire 🚀", use_container_width=True):
    switch_page("2_Questionnaire")
