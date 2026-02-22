import streamlit as st
import random
from utils.database import save_result

def render_hs_social_module(token, grade):
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #795548; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Social Science / சமூக அறிவியல் 🌍</h2>
        <p style='margin: 0; color: #e0e0e0;'>Grade {grade} History & Geography Expedition</p>
    </div>
    """.format(grade=grade), unsafe_allow_html=True)

    if 'hs_social_q' not in st.session_state:
        st.session_state.hs_social_q = 1
        st.session_state.hs_social_score = 0
        st.session_state.hs_social_answered = False
        st.session_state.hs_social_result = None
        st.session_state.current_hs_social_q = None

    # Sample High School Social Science Questions (History, Civics, Geography, Economics)
    questions_pool = [
        {"q": "Who is known as the 'Father of the Indian Constitution'?", "o": ["Mahatma Gandhi", "Dr. B.R. Ambedkar", "Jawaharlal Nehru"], "a": "Dr. B.R. Ambedkar", "logic": "Dr. Ambedkar was the chairman of the drafting committee of the Indian Constitution."},
        {"q": "Which is the longest river in the world?", "o": ["Amazon", "Nile", "Ganga"], "a": "Nile", "logic": "The Nile is generally accepted as the longest river, flowing through northeastern Africa."},
        {"q": "In which year did India get Independence?", "o": ["1942", "1947", "1950"], "a": "1947", "logic": "India gained independence from British rule on August 15, 1947."},
        {"q": "Which is the smallest continent by land area?", "o": ["Europe", "Australia", "Antarctica"], "a": "Australia", "logic": "Australia is the smallest continent and also a country."},
        {"q": "What is the capital of Tamil Nadu?", "o": ["Madurai", "Coimbatore", "Chennai"], "a": "Chennai", "logic": "Chennai is the capital and largest city of Tamil Nadu."}
    ]

    if st.session_state.hs_social_q <= 10:
        if st.session_state.current_hs_social_q is None:
            st.session_state.current_hs_social_q = random.choice(questions_pool)
        
        q = st.session_state.current_hs_social_q
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"Question: **{st.session_state.hs_social_q}/10**")
            st.progress(st.session_state.hs_social_q / 10)
            st.metric("Score", st.session_state.hs_social_score)

        with col2:
            st.subheader(q['q'])
            st.write("### Choose the correct historical or geographical fact:")
            
            btn_cols = st.columns(len(q['o']))
            if not st.session_state.hs_social_answered:
                for i, opt in enumerate(q['o']):
                    if btn_cols[i].button(opt, key=f"ss_opt_{i}"):
                        st.session_state.hs_social_answered = True
                        if opt == q['a']:
                            st.session_state.hs_social_result = "correct"
                            st.session_state.hs_social_score += 1
                        else:
                            st.session_state.hs_social_result = "incorrect"
                        st.rerun()
            else:
                if st.session_state.hs_social_result == "correct":
                    st.success("Correct! Well informed citizen! 🌍")
                else:
                    st.error(f"Incorrect. The fact is: {q['a']}")
                    with st.expander("Historical Context", expanded=True):
                        st.write(q['logic'])
                
                if st.button("Next Destination ➡️", use_container_width=True):
                    st.session_state.hs_social_q += 1
                    st.session_state.hs_social_answered = False
                    st.session_state.current_hs_social_q = None
                    if st.session_state.hs_social_q > 10:
                        save_result(token, "HS_Social", st.session_state.hs_social_score)
                    st.rerun()
    else:
        st.success("World Explorer! You finished the Social Science challenge!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.hs_social_score}/10")
        if st.button("Back to Dashboard", use_container_width=True):
            if 'hs_social_q' in st.session_state: del st.session_state.hs_social_q
            st.session_state.page = "dashboard"
            st.rerun()
