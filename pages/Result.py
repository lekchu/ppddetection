
   import streamlit as st
import pandas as pd
import joblib

model = joblib.load("model/ppd_model_pipeline.pkl")
le = joblib.load("model/label_encoder.pkl")

st.set_page_config(page_title="PPD Predictor - Result", layout="wide")

if "user_data" not in st.session_state or "answers" not in st.session_state:
    st.warning("Please complete the questionnaire first.")
    st.stop()

user = st.session_state.user_data
score = sum(st.session_state.answers)

st.title("🎯 Result")
st.markdown(f"**{user['Name']}**, your EPDS score is: **{score}/30**")

input_df = pd.DataFrame([{
    "Age": user["Age"],
    "FamilySupport": user["FamilySupport"],
    **{f"Q{i+1}": v for i, v in enumerate(st.session_state.answers)},
    "EPDS_Score": score
}])

prediction = model.predict(input_df)[0]
label = le.inverse_transform([prediction])[0]

st.success(f"Predicted Risk Level: **{label}**")

# Risk-based feedback
if label.lower() == "low":
    st.balloons()
    st.info("✅ You're doing well. Continue monitoring your emotional health. 💚")
elif label.lower() == "moderate":
    st.warning("⚠️ Moderate risk. Please consider speaking with a healthcare provider.")
else:
    st.error("🚨 High risk. Contact a mental health professional immediately.")

# Download result
result_csv = pd.DataFrame([user | {"Score": score, "Risk": label}])
st.download_button("📥 Download Result as CSV", data=result_csv.to_csv(index=False), file_name="ppd_result.csv")

# Restart
if st.button("🔁 Start Over"):
    for key in ["user_data", "answers", "q_index"]:
        st.session_state.pop(key, None)
    st.switch_page("pages/1_Home.py")
