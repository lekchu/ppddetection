import streamlit as st
import base64

# Set background image style
def set_page_style():
    def get_base64_bg(image_file):
        with open(image_file, "rb") as f:
            return base64.b64encode(f.read()).decode()

    bg = get_base64_bg("assets/background.png")
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

# EPDS response scoring per question
Q_RESPONSES = {
    f"Q{i+1}": {
        "As much as I always could": 0,
        "Not quite so much now": 1,
        "Definitely not so much now": 2,
        "Not at all": 3
    } if i < 2 else {
        "No, not at all": 0,
        "Not very often": 1,
        "Yes, sometimes": 2,
        "Yes, most of the time": 3
    } for i in range(10)
}
