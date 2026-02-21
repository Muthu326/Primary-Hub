import streamlit as st
import random
import json
import os
from utils.database import save_result

def render_math_module(language, token):
    # Performance & Uniqueness: Seeded Randomization
    random.seed(token)
    import time
    
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #ffcc00; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Magic Mathematics / மந்திர கணிதம் 🔢</h2>
        <p style='margin: 0; color: #e0e0e0;'>10-Question Daily Challenge! / தினசரி 10 கேள்விகள் சவால்!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'math_q' not in st.session_state:
        st.session_state.math_q = 1
        st.session_state.math_score = 0
        generate_new_math_q(token, st.session_state.math_q)

    if st.session_state.math_q <= 10:
        q = st.session_state.current_math_q
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("#### Progress / முன்னேற்றம்")
            st.write(f"Question / கேள்வி: **{st.session_state.math_q}/10**")
            st.progress(st.session_state.math_q / 10)
            
            # Difficulty indicator
            diff_color = "#4CAF50" if st.session_state.math_q <= 3 else ("#FF9800" if st.session_state.math_q <= 7 else "#F44336")
            diff_text = "Easy / எளிது" if st.session_state.math_q <= 3 else ("Moderate / நடுத்தரம்" if st.session_state.math_q <= 7 else "Hard / கடினம்")
            st.markdown(f"<div style='background: {diff_color}; color: white; padding: 5px 10px; border-radius: 5px; text-align: center; font-weight: bold;'>{diff_text}</div>", unsafe_allow_html=True)
            
            st.divider()
            st.write(f"Points Scored: {st.session_state.math_score}")
            
        with col2:
            st.markdown("#### Solve Here / இங்கே தீர்க்கவும்")
            st.info(f"### Question / கேள்வி: **{q['question']}**")
            
            user_ans = st.number_input("Your answer / உங்கள் பதில்:", value=0, key=f"math_ans_{st.session_state.math_q}")
            
            if st.button("Check Answer / சரிபார்க்கவும்", use_container_width=True):
                if user_ans == q['ans']:
                    st.success("Correct! Well done! / மிகச் சரி! 🎉")
                    st.session_state.math_score += 1
                else:
                    st.error(f"Not quite / தவறு. (Correct Ans: {q['ans']})")
                    
                st.session_state.math_q += 1
                if st.session_state.math_q <= 10:
                    generate_new_math_q(token, st.session_state.math_q)
                else:
                    save_result(token, "Mathematics", st.session_state.math_score)
                time.sleep(1)
                st.rerun()
    else:
        st.success("Great job! You finished the challenge! / நீங்கள் சவாலை முடித்துவிட்டீர்கள்!")
        st.balloons()
        st.write(f"### Final Score / இறுதி மதிப்பெண்: {st.session_state.math_score}/10")
        if st.button("Back to Dashboard / முகப்பிற்குத் திரும்பவும்", use_container_width=True):
            if 'math_q' in st.session_state: del st.session_state.math_q
            st.session_state.page = "dashboard"
            st.rerun()

def generate_new_math_q(token, q_num):
    # Progressive Difficulty & Advanced Patterns
    if q_num <= 3: # Level 1: Basics
        n1 = random.randint(1, 9)
        n2 = random.randint(1, 9)
        op = 'add'
        op_char = '+'
        ans = n1 + n2
        question_text = f"{n1} + {n2}"
    elif q_num <= 7: # Level 2: Sequences / Skip Counting
        options = ["skip_counting", "med_arithmetic"]
        choice = random.choice(options)
        if choice == "skip_counting":
            start = random.randint(2, 10)
            step = random.randint(2, 5)
            seq = [start + i*step for i in range(4)]
            ans = seq[3] + step
            op_char = "?"
            question_text = f"{seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ___ ?"
            op = "seq"
        else:
            n1 = random.randint(10, 50)
            n2 = random.randint(1, 20)
            op = random.choice(['add', 'sub'])
            if op == 'sub' and n1 < n2: n1, n2 = n2, n1
            ans = n1 + n2 if op == 'add' else n1 - n2
            op_char = '+' if op == 'add' else '-'
            question_text = f"{n1} {op_char} {n2}"
    else: # Level 3: Challenge
        choice = random.choice(["mul", "big_sub", "missing_num"])
        if choice == "mul":
            n1 = random.randint(2, 12)
            n2 = random.randint(2, 9)
            ans = n1 * n2
            op_char = "×"
            question_text = f"{n1} × {n2}"
        elif choice == "big_sub":
            n1 = random.randint(80, 150)
            n2 = random.randint(20, 75)
            ans = n1 - n2
            op_char = "-"
            question_text = f"{n1} - {n2}"
        else:
            n1 = random.randint(10, 30)
            ans = random.randint(40, 60)
            missing = ans - n1
            op_char = "+"
            question_text = f"{n1} + ___ = {ans}"
            ans = missing

    st.session_state.current_math_q = {
        'question': question_text,
        'ans': ans,
        'op_char': op_char
    }
