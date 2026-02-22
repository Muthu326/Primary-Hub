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
        # Generate visual/figure puzzle if not exists
        if st.session_state.current_apt_q is None:
            # Category 1: Figure Patterns (Visual Sequences)
            patterns = [
                {"q": "🐱 🐶 🐱 🐶 ... ?", "a": "🐱", "o": ["🐱", "🐶", "🦊"], "type": "Pattern"},
                {"q": "🐘 🦒 🐘 🦒 ... ?", "a": "🐘", "o": ["🐘", "🦒", "🦓"], "type": "Pattern"},
                {"q": "🟥 🟦 🟥 🟦 ... ?", "a": "🟥", "o": ["🟥", "🟦", "🟩"], "type": "Pattern"},
                {"q": "⚽ 🏀 ⚽ 🏀 ... ?", "a": "⚽", "o": ["⚽", "🏀", "🎾"], "type": "Pattern"},
                {"q": "🚗 🚲 🚗 🚲 ... ?", "a": "🚗", "o": ["🚗", "🚲", "✈️"], "type": "Pattern"}
            ]
            
            # Category 2: Directional Logic (Figures in space)
            directions = [
                {"q": "⬆️ ➡️ ⬇️ ... ?", "a": "⬅️", "o": ["⬅️", "⬆️", "⬇️"], "type": "Logic"},
                {"q": "🔼 ◀️ 🔽 ... ?", "a": "▶️", "o": ["▶️", "◀️", "🔼"], "type": "Logic"},
                {"q": "↖️ ↗️ ↘️ ... ?", "a": "↙️", "o": ["↙️", "↖️", "↘️"], "type": "Logic"}
            ]
            
            # Category 3: Visual Odd One Out
            vision = [
                {"q": "Which one is different? / எது மாறுபடுகிறது?", "a": "🍐", "o": ["🍎", "🍐", "🍊"], "body": "🍎 🍎 🍐 🍎", "type": "Vision"},
                {"q": "Which one is different? / எது மாறுபடுகிறது?", "a": "🐱", "o": ["🐶", "🐱", "🐭"], "body": "🐶 🐶 🐱 🐶", "type": "Vision"},
                {"q": "Which one is different? / எது மாறுபடுகிறது?", "a": "🚢", "o": ["✈️", "🚢", "🚁"], "body": "✈️ ✈️ ✈️ 🚢", "type": "Vision"},
                {"q": "Which one is different? / எது மாறுபடுகிறது?", "a": "🔵", "o": ["🔴", "🔵", "🔘"], "body": "🔴 🔴 🔵 🔴", "type": "Vision"}
            ]
            
            all_puzzles = patterns + directions + vision
            st.session_state.current_apt_q = random.choice(all_puzzles)

        puzzle = st.session_state.current_apt_q
        pat = puzzle['q']
        ans = puzzle['a']
        options = puzzle['o']
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Progress / முன்னேற்றம்")
            st.write(f"Puzzle: **{st.session_state.apt_q}/10**")
            st.progress(st.session_state.apt_q / 10)
            
            # Category Indicator
            cat_color = "#4CAF50" if puzzle['type'] == "Pattern" else ("#2196F3" if puzzle['type'] == "Logic" else "#E91E63")
            st.markdown(f"<div style='background: {cat_color}; color: white; padding: 5px 10px; border-radius: 5px; text-align: center; font-weight: bold;'>{puzzle['type']}</div>", unsafe_allow_html=True)
            
        with col2:
            st.subheader(pat)
            if 'body' in puzzle:
                st.markdown(f"<p style='font-size: 40px; text-align: center; background: #f0f2f6; padding: 20px; border-radius: 10px;'>{puzzle['body']}</p>", unsafe_allow_html=True)
            else:
                st.info(f"### {pat}")
            
            st.write("### Choose the right figure / சரியான உருவத்தைத் தேர்ந்தெடுக்கவும்:")
            
            # Use columns for choice buttons
            btn_cols = st.columns(len(options))
            
            if not st.session_state.apt_answered:
                for i, opt in enumerate(options):
                    if btn_cols[i].button(opt, key=f"apt_btn_{i}_{st.session_state.apt_q}", use_container_width=True):
                        st.session_state.apt_answered = True
                        if opt == ans:
                            st.session_state.apt_result = "correct"
                            st.session_state.apt_score += 1
                        else:
                            st.session_state.apt_result = "incorrect"
                            st.session_state.apt_final_ans = ans
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
