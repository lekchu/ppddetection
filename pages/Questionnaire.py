elif st.session_state.page == "questionnaire":
    st.title("📝 Questionnaire")
    st.progress((st.session_state.q_index + 1) / len(questions))

    if st.session_state.q_index < len(questions):
        q, options = questions[st.session_state.q_index]
        st.subheader(f"Q{st.session_state.q_index+1}: {q}")
        ans = st.radio("Your Answer:", options, key=f"q{st.session_state.q_index}")

        if st.button("Next"):
            if ans:
                st.session_state.answers.append(score_map[options.index(ans)])
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.warning("Please select an answer before moving on.")
    else:
        st.session_state.page = "result"
        st.rerun()
