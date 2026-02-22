import streamlit as st
import random
from utils.database import save_result

def render_hs_english_module(token, grade):
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #2196F3; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>English Proficiency / ஆங்கில மொழித் திறன் 📘</h2>
        <p style='margin: 0; color: #e0e0e0;'>Grade {grade} Language Challenge / இலக்கணச் சவால்</p>
    </div>
    """.format(grade=grade), unsafe_allow_html=True)

    if 'hs_english_q' not in st.session_state:
        st.session_state.hs_english_q = 1
        st.session_state.hs_english_score = 0
        st.session_state.hs_english_answered = False
        st.session_state.hs_english_result = None
        st.session_state.current_hs_english_q = None

    # Sample High School English Questions (Grammar, Vocabulary, Tenses)
    questions_pool = [
        {"q": "Identity the synonym of 'Diligent':", "o": ["Lazy", "Hardworking", "Quiet"], "a": "Hardworking", "logic": "Diligent means showing care and conscientiousness in one's work."},
        {"q": "Choose the correct tense: 'I ___ to the market yesterday.'", "o": ["go", "gone", "went"], "a": "went", "logic": "The word 'yesterday' indicates the past tense, so 'went' is correct."},
        {"q": "Which of these is a 'Verb'?", "o": ["Beautiful", "Run", "Happiness"], "a": "Run", "logic": "Verbs are action words. 'Run' describes an action."},
        {"q": "Choose the correct article: 'He is ___ honest man.'", "o": ["a", "an", "the"], "a": "an", "logic": "Even though 'honest' starts with 'h', it has a vowel sound (o-nest), so we use 'an'."},
        {"q": "What is the opposite of 'Ancient'?", "o": ["Old", "Modern", "Historic"], "a": "Modern", "logic": "Ancient means very old; the opposite is modern."}
    ]

    if st.session_state.hs_english_q <= 10:
        if st.session_state.current_hs_english_q is None:
            st.session_state.current_hs_english_q = random.choice(questions_pool)
        
        q = st.session_state.current_hs_english_q
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"Question: **{st.session_state.hs_english_q}/10**")
            st.progress(st.session_state.hs_english_q / 10)
            st.metric("Score", st.session_state.hs_english_score)

        with col2:
            st.subheader(q['q'])
            st.write("### Select the correct option:")
            
            btn_cols = st.columns(len(q['o']))
            if not st.session_state.hs_english_answered:
                for i, opt in enumerate(q['o']):
                    if btn_cols[i].button(opt, key=f"e_opt_{i}"):
                        st.session_state.hs_english_answered = True
                        if opt == q['a']:
                            st.session_state.hs_english_result = "correct"
                            st.session_state.hs_english_score += 1
                        else:
                            st.session_state.hs_english_result = "incorrect"
                        st.rerun()
            else:
                if st.session_state.hs_english_result == "correct":
                    st.success("Great job! Correct Answer! ✨")
                else:
                    st.error(f"Incorrect. The correct answer is: {q['a']}")
                    with st.expander("Explanation", expanded=True):
                        st.write(q['logic'])
                
                if st.button("Next Question ➡️", use_container_width=True):
                    st.session_state.hs_english_q += 1
                    st.session_state.hs_english_answered = False
                    st.session_state.current_hs_english_q = None
                    if st.session_state.hs_english_q > 10:
                        save_result(token, "HS_English", st.session_state.hs_english_score)
                    st.rerun()
    else:
        st.success("Congratulations! You finished the English challenge!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.hs_english_score}/10")
        if st.button("Back to Dashboard", use_container_width=True):
            if 'hs_english_q' in st.session_state: del st.session_state.hs_english_q
            st.session_state.page = "dashboard"
            st.rerun()
