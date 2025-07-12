import streamlit as st
import pandas as pd
import joblib

# Load the model and label encoder
model = joblib.load("model/ppd_model_pipeline.pkl")
le = joblib.load("model/label_encoder.pkl")

# Set page config
st.set_page_config(page_title="PPD Predictor - Result", layout="wide")

# Check session state
if "user_data" not in st.session_state or "answers" not in st.session_state:
    st.warning("⚠️ Please complete the questionnaire first.")
    st.stop()

# Retrieve data
user = st.session_state.user_data
answers = st.session_state.answers
score = sum(answers)

# Title and score display
st.title("🎯 Prediction Result")
st.markdown(f"### Hello, **{user['Name']}**!")
st.markdown(f"Your **EPDS score** is: **{score} / 30**")

# Create input DataFrame
input_df = pd.DataFrame([{
    "Age": user["Age"],
    "FamilySupport": user["FamilySupport"],
    **{f"Q{i+1}": val for i, val in enumerate(answers)},
    "EPDS_Score": score
}])

# Make prediction
prediction = model.predict(input_df)[0]
label = le.inverse_transform([prediction])[0]

st.success(f"Predicted Risk Level: **{label}**")
st.progress(score / 30)

# Risk-based advice
if label.lower() == "low":
    st.balloons()
    st.info("✅ You seem emotionally well. Keep practicing self-care and reach out for support when needed. 💚")
elif label.lower() == "moderate":
    st.warning("⚠️ You may have moderate risk. Consider speaking with a healthcare provider or mental health counselor.")
else:
    st.error("🚨 High risk detected. Please speak to a licensed mental health professional as soon as possible.")

# Create result for download
merged_result = user.copy()
merged_result.update({"Score": score, "Risk Level": label})
download_df = pd.DataFrame([merged_result])

st.download_button(
    label="📥 Download Result as CSV",
    data=download_df.to_csv(index=False),
    file_name="ppd_result.csv",
    mime="text/csv"
)

# Restart flow
if st.button("🔁 Start Over"):
    for key in ["user_data", "answers", "q_index"]:
        st.session_state.pop(key, None)
    st.switch_page("pages/1_Home.py")
