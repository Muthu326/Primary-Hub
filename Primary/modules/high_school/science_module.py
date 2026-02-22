import streamlit as st
import random
from utils.database import save_result

def render_hs_science_module(token, grade):
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #4CAF50; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Science Exploration / அறிவியல் 🔬</h2>
        <p style='margin: 0; color: #e0e0e0;'>Grade {grade} Laboratory of Knowledge</p>
    </div>
    """.format(grade=grade), unsafe_allow_html=True)

    if 'hs_science_q' not in st.session_state:
        st.session_state.hs_science_q = 1
        st.session_state.hs_science_score = 0
        st.session_state.hs_science_answered = False
        st.session_state.hs_science_result = None
        st.session_state.current_hs_science_q = None

    # Sample High School Science Questions (Biology, Physics, Chemistry)
    questions_pool = [
        {"q": "Which gas is essential for photosynthesis?", "o": ["Oxygen", "Carbon Dioxide", "Nitrogen"], "a": "Carbon Dioxide", "logic": "Plants use Carbon Dioxide (CO2) from the air to make food through photosynthesis."},
        {"q": "What is the chemical formula for Water?", "o": ["CO2", "H2O", "O2"], "a": "H2O", "logic": "Water is made of 2 atoms of Hydrogen and 1 atom of Oxygen (H2O)."},
        {"q": "What is the Power House of the Cell?", "o": ["Nucleus", "Mitochondria", "Ribosome"], "a": "Mitochondria", "logic": "Mitochondria generate most of the chemical energy needed to power the cell's biochemical reactions."},
        {"q": "Newton's First Law is also known as the Law of ___:", "o": ["Gravity", "Inertia", "Force"], "a": "Inertia", "logic": "The Law of Inertia states that an object will remain at rest unless acted upon by an external force."},
        {"q": "Which part of the human eye is sensitive to light?", "o": ["Pupil", "Retina", "Iris"], "a": "Retina", "logic": "The Retina contains photoreceptor cells (rods and cones) that convert light into neural signals."}
    ]

    if st.session_state.hs_science_q <= 10:
        if st.session_state.current_hs_science_q is None:
            st.session_state.current_hs_science_q = random.choice(questions_pool)
        
        q = st.session_state.current_hs_science_q
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"Question: **{st.session_state.hs_science_q}/10**")
            st.progress(st.session_state.hs_science_q / 10)
            st.metric("Score", st.session_state.hs_science_score)

        with col2:
            st.subheader(q['q'])
            st.write("### Choose the correct scientific answer:")
            
            btn_cols = st.columns(len(q['o']))
            if not st.session_state.hs_science_answered:
                for i, opt in enumerate(q['o']):
                    if btn_cols[i].button(opt, key=f"s_opt_{i}"):
                        st.session_state.hs_science_answered = True
                        if opt == q['a']:
                            st.session_state.hs_science_result = "correct"
                            st.session_state.hs_science_score += 1
                        else:
                            st.session_state.hs_science_result = "incorrect"
                        st.rerun()
            else:
                if st.session_state.hs_science_result == "correct":
                    st.success("Correct! Future Scientist! 🌟")
                else:
                    st.error(f"Incorrect. The scientific fact is: {q['a']}")
                    with st.expander("Scientific Logic", expanded=True):
                        st.write(q['logic'])
                
                if st.button("Next Experiment ➡️", use_container_width=True):
                    st.session_state.hs_science_q += 1
                    st.session_state.hs_science_answered = False
                    st.session_state.current_hs_science_q = None
                    if st.session_state.hs_science_q > 10:
                        save_result(token, "HS_Science", st.session_state.hs_science_score)
                    st.rerun()
    else:
        st.success("Great Discoveries! You finished the Science challenge!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.hs_science_score}/10")
        if st.button("Back to Dashboard", use_container_width=True):
            if 'hs_science_q' in st.session_state: del st.session_state.hs_science_q
            st.session_state.page = "dashboard"
            st.rerun()
