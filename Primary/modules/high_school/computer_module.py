import streamlit as st
import random
from utils.database import save_result

def render_hs_computer_module(token, grade):
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #607D8B; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Computer & Productivity Skills / கணினித் திறன் 💻</h2>
        <p style='margin: 0; color: #e0e0e0;'>Grade {grade} Word, Excel & Tech Basics</p>
    </div>
    """.format(grade=grade), unsafe_allow_html=True)

    if 'hs_comp_q' not in st.session_state:
        st.session_state.hs_comp_q = 1
        st.session_state.hs_comp_score = 0
        st.session_state.hs_comp_answered = False
        st.session_state.hs_comp_result = None
        st.session_state.current_hs_comp_q = None

    # Sample Computer Science Questions (Hardware, Word, Excel)
    questions_pool = [
        {"q": "What is the shortcut to 'Copy' a text in MS Word?", "o": ["Ctrl + V", "Ctrl + C", "Ctrl + X"], "a": "Ctrl + C", "logic": "Ctrl + C is used for Copying, whereas Ctrl + V is for Pasting."},
        {"q": "In MS Excel, what is a collection of cells called?", "o": ["Worksheet", "Folder", "Presentation"], "a": "Worksheet", "logic": "A worksheet is a single page in an Excel workbook consisting of rows and columns of cells."},
        {"q": "Which of these is used to 'SAVE' a document?", "o": ["Ctrl + S", "Ctrl + P", "Ctrl + N"], "a": "Ctrl + S", "logic": "Ctrl + S is the universal shortcut to save files in most software."},
        {"q": "Which part is the 'Brain' of the computer?", "o": ["RAM", "Monitor", "CPU"], "a": "CPU", "logic": "The Central Processing Unit (CPU) performs all the calculations and instructions and is often called the brain."},
        {"q": "How many bits make 1 Byte?", "o": ["4", "10", "8"], "a": "8", "logic": "In computer science, 8 bits group together to form 1 Byte."}
    ]

    if st.session_state.hs_comp_q <= 10:
        if st.session_state.current_hs_comp_q is None:
            st.session_state.current_hs_comp_q = random.choice(questions_pool)
        
        q = st.session_state.current_hs_comp_q
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"Question: **{st.session_state.hs_comp_q}/10**")
            st.progress(st.session_state.hs_comp_q / 10)
            st.metric("Score", st.session_state.hs_comp_score)

        with col2:
            st.subheader(q['q'])
            st.write("### Choose the correct tech solution:")
            
            btn_cols = st.columns(len(q['o']))
            if not st.session_state.hs_comp_answered:
                for i, opt in enumerate(q['o']):
                    if btn_cols[i].button(opt, key=f"c_opt_{i}"):
                        st.session_state.hs_comp_answered = True
                        if opt == q['a']:
                            st.session_state.hs_comp_result = "correct"
                            st.session_state.hs_comp_score += 1
                        else:
                            st.session_state.hs_comp_result = "incorrect"
                        st.rerun()
            else:
                if st.session_state.hs_comp_result == "correct":
                    st.success("Correct! Digital Expert! 💻")
                else:
                    st.error(f"Incorrect. The correct answer is: {q['a']}")
                    with st.expander("Tech Explanation", expanded=True):
                        st.write(q['logic'])
                
                if st.button("Next Task ➡️", use_container_width=True):
                    st.session_state.hs_comp_q += 1
                    st.session_state.hs_comp_answered = False
                    st.session_state.current_hs_comp_q = None
                    if st.session_state.hs_comp_q > 10:
                        save_result(token, "HS_Computer", st.session_state.hs_comp_score)
                    st.rerun()
    else:
        st.success("Tech Savvy! You finished the Computer challenge!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.hs_comp_score}/10")
        if st.button("Back to Dashboard", use_container_width=True):
            if 'hs_comp_q' in st.session_state: del st.session_state.hs_comp_q
            st.session_state.page = "dashboard"
            st.rerun()
