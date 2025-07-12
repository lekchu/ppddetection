elif st.session_state.page == "result":
    st.title("🎯 Your Result")
    score = sum(st.session_state.answers)
    user = st.session_state.user_data

    # Prepare input for prediction
    input_df = pd.DataFrame([{
        "Age": user["Age"],
        "FamilySupport": user["FamilySupport"],
        **{f"Q{i+1}": v for i, v in enumerate(st.session_state.answers)},
        "EPDS_Score": score
    }])

    prediction = model.predict(input_df)[0]
    label = le.inverse_transform([prediction])[0]

    st.success(f"Hi {user['Name']}, your predicted risk level is: **{label}**")
    st.progress(score / 30)

    # Risk-based feedback
    if label.lower() == "low":
        st.balloons()
        st.info("✅ You are likely in a good emotional state. Keep taking care of yourself! 💚")
    elif label.lower() == "moderate":
        st.warning("⚠️ You may be showing some signs of concern. Please talk to someone or consult a provider.")
    else:
        st.error("🚨 High risk detected. We strongly recommend speaking with a mental health professional.")

    # CSV download (without using dict | merge)
    merged_result = user.copy()
    merged_result.update({"Score": score, "Risk": label})
    result_csv = pd.DataFrame([merged_result])

    st.download_button("📥 Download Result as CSV", data=result_csv.to_csv(index=False), file_name="ppd_result.csv")

    # Restart
    if st.button("🔁 Start Over"):
        for key in ["page", "user_data", "answers", "q_index"]:
            st.session_state.pop(key, None)
        st.rerun()
