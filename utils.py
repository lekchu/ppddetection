import base64

def set_background(image_file):
    with open(image_file, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """
    import streamlit as st
    st.markdown(bg_img, unsafe_allow_html=True)
