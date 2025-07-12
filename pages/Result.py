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
        st.balloons()
        st.info("You seem to be doing well. Keep nurturing your mental health and seek support when needed. 🌼")
    elif label.lower() == "moderate":
        st.warning("You might be experiencing moderate symptoms of postpartum depression. Consider speaking with a healthcare provider.")
    else:
        st.error("You are showing signs of high risk for postpartum depression. Please reach out to a mental health professional or support group immediately. 💬")

    st.progress(score / 30)
 # Download result as CSV
    csv_data = pd.DataFrame.from_dict([user_info | {"Score": score, "Risk Level": label}])
    st.download_button("📥 Download Result as CSV", data=csv_data.to_csv(index=False), file_name="ppd_result.csv", mime="text/csv")

    if st.button("🔁 Start Over"):
        st.session_state.page = "intro"
        st.session_state.answers = []
        st.session_state.q_index = 0
        st.experimental_rerun()
