import streamlit as st
import random
from utils.database import save_result

def render_aptitude_module(language, token):
    # random.seed(token)
    import time
    
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #ff9800; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Brain Puzzles / மூளை திறன் 🧩</h2>
        <p style='margin: 0; color: #e0e0e0;'>Test your logic with 10 puzzles! / 10 புதிர்களைத் தீர்க்கவும்!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'apt_q' not in st.session_state:
        st.session_state.apt_q = 1
        st.session_state.apt_score = 0
        st.session_state.apt_answered = False
        st.session_state.apt_result = None
        st.session_state.current_apt_q = None

    if st.session_state.apt_q <= 10:
        # Generate question if not exists for this step
        if st.session_state.current_apt_q is None:
            if st.session_state.apt_q <= 3: # Easy
                patterns = [
                    ("🍎 🍌 🍎 🍌 ... ?", "🍎"),
                    ("⭐ 🌙 ⭐ 🌙 ... ?", "⭐"),
                    ("🐶 🐱 🐶 🐱 ... ?", "🐶"),
                    ("🌞 ☁️ 🌞 ☁️ ... ?", "🌞")
                ]
            elif st.session_state.apt_q <= 7: # Moderate
                patterns = [
                    ("1 2 3 1 2 ... ?", "3"),
                    ("A B A B C A B ... ?", "A"),
                    ("Circle Square Circle ... ?", "Square"),
                    ("Up Down Up Down ... ?", "Up")
                ]
            else: # Hard
                patterns = [
                    ("2 4 6 8 ... ?", "10"),
                    ("5 10 15 20 ... ?", "25"),
                    ("A C E G ... ?", "I"),
                    ("10 9 8 7 ... ?", "6")
                ]
            st.session_state.current_apt_q = random.choice(patterns)

        pat, ans = st.session_state.current_apt_q
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Progress")
            st.write(f"Puzzle: **{st.session_state.apt_q}/10**")
            st.progress(st.session_state.apt_q / 10)
            
            # Difficulty indicator
            diff_color = "#4CAF50" if st.session_state.apt_q <= 3 else ("#FF9800" if st.session_state.apt_q <= 7 else "#F44336")
            diff_text = "Level 1" if st.session_state.apt_q <= 3 else ("Level 2" if st.session_state.apt_q <= 7 else "Level 3")
            st.markdown(f"<div style='background: {diff_color}; color: white; padding: 5px 10px; border-radius: 5px; text-align: center; font-weight: bold;'>{diff_text}</div>", unsafe_allow_html=True)
            
        with col2:
            st.subheader("Which comes next? / அடுத்து வருவது எது?")
            st.info(f"### {pat}")
            
            user_choice = st.text_input("Your Answer / உங்கள் பதில்:", placeholder="Type here...", key=f"apt_ans_{st.session_state.apt_q}", disabled=st.session_state.apt_answered)
            
            if not st.session_state.apt_answered:
                if st.button("Submit / சமர்ப்பிக்கவும்", use_container_width=True):
                    st.session_state.apt_answered = True
                    if user_choice.strip().upper() == ans.upper():
                        st.session_state.apt_result = "correct"
                        st.session_state.apt_score += 1
                    else:
                        st.session_state.apt_result = "incorrect"
                        st.session_state.apt_final_ans = ans # Store correct answer to show
                    st.rerun()
            else:
                if st.session_state.apt_result == "correct":
                    st.success("Brilliant! / அற்புதம்! 🌟")
                else:
                    st.error(f"Try harder! / மீண்டும் முயற்சி செய்! (Ans: {st.session_state.apt_final_ans})")
                
                if st.button("Next Puzzle / அடுத்த புதிர் ➡️", use_container_width=True):
                    st.session_state.apt_q += 1
                    st.session_state.apt_answered = False
                    st.session_state.apt_result = None
                    st.session_state.current_apt_q = None
                    if st.session_state.apt_q > 10:
                        save_result(token, "Aptitude", st.session_state.apt_score)
                    st.rerun()
    else:
        st.success("Puzzle Master! You finished the challenge! / நீங்கள் சவாலை முடித்துவிட்டீர்கள்!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.apt_score}/10")
        if st.button("Back to Dashboard / முகப்பிற்குத் திரும்பவும்", use_container_width=True):
            if 'apt_q' in st.session_state: del st.session_state.apt_q
            st.session_state.page = "dashboard"
            st.rerun()
