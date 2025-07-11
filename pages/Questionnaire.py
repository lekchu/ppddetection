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
