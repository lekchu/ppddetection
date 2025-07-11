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

    name = st.text_input("Your Name")
    age = st.slider("Age", 18, 45, 28)
    pregnant = st.radio("Are you currently pregnant?", ["Yes", "No"])
    recent_birth = st.radio("Have you given birth recently?", ["Yes", "No"])
    family_support = st.selectbox("How would you rate your family support?", ["High", "Medium", "Low"])

    if st.button("Start Questionnaire"):
        if not name.strip():
            st.warning("Please enter your name before proceeding.")
        else:
            st.session_state.user_data = {
                "Name": name,
                "Age": age,
                "Pregnant": pregnant,
                "RecentBirth": recent_birth,
                "FamilySupport": family_support
            }
            st.session_state.page = "questionnaire"
            st.success("Starting questionnaire... please wait ⏳")
            st.stop()

# QUESTIONNAIRE PAGE
elif st.session_state.page == "questionnaire":
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

    st.progress((st.session_state.q_index + 1) / len(questions))

    if st.session_state.q_index < len(questions):
        q, options = questions[st.session_state.q_index]
        st.subheader(f"Q{st.session_state.q_index+1}: {q}")
        ans = st.radio("Select your response:", options)
        if st.button("Next"):
            if ans is not None:
                st.session_state.answers.append(score_map[options.index(ans)])
                st.session_state.q_index += 1
                st.experimental_rerun()
            else:
                st.warning("Please select an option before continuing.")
    else:
        go_to("result")

# RESULT PAGE
elif st.session_state.page == "result":
    score = sum(st.session_state.answers)
    user_info = st.session_state.user_data
    input_data = pd.DataFrame([{
        "Age": user_info["Age"],
        "FamilySupport": user_info["FamilySupport"],
        **{f"Q{i+1}": val for i, val in enumerate(st.session_state.answers)},
        "EPDS_Score": score
    }])

    pred = model.predict(input_data)[0]
    label = le.inverse_transform([pred])[0]

    st.header("🧾 Your Depression Risk Result")
    st.markdown(f"### **{user_info['Name']}, your predicted risk level is:**")
    st.success(f"💡 {label} (Score: {score}/30)")

    # Advice based on label
    if label.lower() == "low":
        st.info("You seem to be doing well. Keep nurturing your mental health and seek support when needed. 🌼")
    elif label.lower() == "moderate":
        st.warning("You might be experiencing moderate symptoms of postpartum depression. Consider speaking with a healthcare provider.")
    else:
        st.error("You are showing signs of high risk for postpartum depression. Please reach out to a mental health professional or support group immediately. 💬")

    st.progress(score / 30)

    if st.button("🔁 Start Over"):
        st.session_state.page = "intro"
        st.session_state.answers = []
        st.session_state.q_index = 0
        st.experimental_rerun()


    
