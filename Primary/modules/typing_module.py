import streamlit as st
import random
from utils.database import save_result

def render_typing_module(language, token):
    # random.seed(token)
    import time
    
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #009688; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Typing Fun / தட்டச்சு பயிற்சி ⌨️</h2>
        <p style='margin: 0; color: #e0e0e0;'>10-Step Speed Challenge! / 10 படிகள் தட்டச்சு சவால்!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'type_q' not in st.session_state:
        st.session_state.type_q = 1
        st.session_state.type_score = 0
        st.session_state.type_answered = False
        st.session_state.type_result = None
        generate_new_typing_target(st.session_state.type_q)

    if st.session_state.type_q <= 10:
        target = st.session_state.typing_target
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Progress")
            st.write(f"Step: **{st.session_state.type_q}/10**")
            st.progress(st.session_state.type_q / 10)
            
            # Difficulty indicator
            diff_color = "#4CAF50" if st.session_state.type_q <= 3 else ("#FF9800" if st.session_state.type_q <= 7 else "#F44336")
            diff_text = "Level 1" if st.session_state.type_q <= 3 else ("Level 2" if st.session_state.type_q <= 7 else "Level 3")
            st.markdown(f"<div style='background: {diff_color}; color: white; padding: 5px 10px; border-radius: 5px; text-align: center; font-weight: bold;'>{diff_text}</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("#### Type This / இதைத் தட்டச்சு செய்க")
            st.markdown(f"<div style='background: #fff; padding: 20px; border-radius: 10px; border: 2px dashed #009688; text-align: center; margin-bottom: 20px;'><h1 style='margin: 0; color: #009688; font-size: 60px;'>{target}</h1></div>", unsafe_allow_html=True)
            
            user_input = st.text_input("Type here / இங்கே தட்டச்சு செய்யவும்:", key=f"type_in_{st.session_state.type_q}", disabled=st.session_state.type_answered)
            
            if not st.session_state.type_answered:
                if st.button("Submit / சமர்ப்பிக்கவும்", use_container_width=True):
                    st.session_state.type_answered = True
                    if user_input.strip().upper() == target.upper():
                        st.session_state.type_result = "correct"
                        st.session_state.type_score += 1
                    else:
                        st.session_state.type_result = "incorrect"
                    st.rerun()
            else:
                if st.session_state.type_result == "correct":
                    st.success("Perfect! / மிகச் சரி! 🎯")
                else:
                    st.error(f"Try again! / மீண்டும் முயற்சிக்கவும்! (Expected: {target})")
                
                if st.button("Next Step / அடுத்த படி ➡️", use_container_width=True):
                    st.session_state.type_q += 1
                    st.session_state.type_answered = False
                    st.session_state.type_result = None
                    if st.session_state.type_q <= 10:
                        generate_new_typing_target(st.session_state.type_q)
                    else:
                        save_result(token, "Typing", st.session_state.type_score)
                    st.rerun()
    else:
        st.success("Speed Demon! You finished the Typing challenge! / நீங்கள் தட்டச்சு சவாலை முடித்துவிட்டீர்கள்!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.type_score}/10")
        if st.button("Back to Dashboard / முகப்பிற்குத் திரும்பவும்", use_container_width=True):
            if 'type_q' in st.session_state: del st.session_state.type_q
            st.session_state.page = "dashboard"
            st.rerun()

def generate_new_typing_target(q_num):
    if q_num <= 3: # Level 1
        targets = ['A', 'S', 'D', 'F', 'அ', 'ஆ', 'இ', 'ஈ']
    elif q_num <= 7: # Level 2
        targets = ['CAT', 'DOG', 'SUN', 'நிலா', 'மலர்', 'கல்வி']
    else: # Level 3
        targets = ['I Love Learning', 'Hello World', 'நமது பள்ளி', 'வாழ்க தமிழ்']
    
    st.session_state.typing_target = random.choice(targets)
