import streamlit as st
import random
import json
import os
from utils.database import save_result

# --- EDUGAIN-STYLE MATH LOGIC ---

def render_math_module(language, token):
    if 'math_history' not in st.session_state:
        st.session_state.math_history = []
    
    if 'math_q' not in st.session_state:
        st.session_state.math_q = 1
        st.session_state.math_score = 0
        st.session_state.math_answered = False
        st.session_state.math_result = None
        st.session_state.current_math_q = None

    if st.session_state.math_q <= 10:
        # Generate Edugain-style question
        if st.session_state.current_math_q is None:
            max_attempts = 15
            while max_attempts > 0:
                q_num = st.session_state.math_q
                if q_num <= 3: # Class 1-2: Basic Addition
                    n1 = random.randint(1, 20)
                    n2 = random.randint(1, 15)
                    ans = n1 + n2
                    q_text = f"Basic Addition / அடிப்படை கூட்டல்"
                    body = f"{n1} + {n2} = ?"
                    options = sorted(list(set([ans, ans+random.randint(1,3), abs(ans-random.randint(1,3)) or ans+5])))
                    logic = f"Logic: Adding {n1} and {n2} gives {ans}. / விளக்கம்: {n1} மற்றும் {n2}-ஐ கூட்டினால் {ans} வரும்."
                
                elif q_num <= 7: # Class 3-4: Mental Math / Missing Number
                    n1 = random.randint(15, 60)
                    ans = random.randint(70, 150)
                    missing = ans - n1
                    q_text = f"Find the missing number / விடுபட்ட எண்ணைக் கண்டுபிடி:"
                    body = f"{n1} + [ ? ] = {ans}"
                    options = sorted(list(set([missing, missing+random.randint(5,10), missing-random.randint(2,5) if missing > 5 else missing+15])))
                    logic = f"Logic: To find the missing number, subtract {n1} from {ans} ({ans} - {n1} = {missing})."
                
                else: # Class 5+: Word Logic / Multi-step
                    n1 = random.randint(10, 25)
                    n2 = random.randint(4, 12)
                    ans = n1 * n2
                    q_text = f"Word Problem / வாழ்க்கைக் கணக்கு:"
                    body = f"If 1 box has {n1} pens, how many pens are in {n2} boxes? / 1 பெட்டியில் {n1} பேனாக்கள் இருந்தால், {n2} பெட்டிகளில் எத்தனை இருக்கும்?"
                    options = sorted(list(set([ans, ans-n1, ans+n1, ans+10])))
                    logic = f"Logic: Multiply the number of pens by the number of boxes: {n1} x {n2} = {ans}."

                if body not in st.session_state.math_history:
                    st.session_state.math_history.append(body)
                    st.session_state.current_math_q = {
                        'q_text': q_text, 'body': body, 'ans': ans, 'options': options, 'logic': logic
                    }
                    break
                max_attempts -= 1

        q = st.session_state.current_math_q
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("#### Progress")
            st.write(f"Question: **{st.session_state.math_q}/10**")
            st.progress(st.session_state.math_q / 10)
            st.metric("Score", st.session_state.math_score)
            
        with col2:
            st.subheader(q['q_text'])
            st.markdown(f"<div style='background: white; padding: 30px; border-radius: 15px; border: 2px solid #ffcc00; text-align: center; margin-bottom: 20px;'><h1 style='color: #2c3e50;'>{q['body']}</h1></div>", unsafe_allow_html=True)
            
            # Adaptive Choice Buttons
            st.write("### Select Answer / பதிலை தேர்ந்தெடுக்கவும்:")
            btn_cols = st.columns(len(q['options']))
            
            if not st.session_state.math_answered:
                for i, opt in enumerate(q['options']):
                    if btn_cols[i].button(str(opt), key=f"math_opt_{i}", use_container_width=True):
                        st.session_state.math_answered = True
                        if opt == q['ans']:
                            st.session_state.math_result = "correct"
                            st.session_state.math_score += 1
                        else:
                            st.session_state.math_result = "incorrect"
                        st.rerun()
            else:
                if st.session_state.math_result == "correct":
                    st.success("Correct! Excellent! / சரியான பதில்! அற்புதம்! ✨")
                else:
                    st.error(f"Incorrect / தவறு. (Correct: {q['ans']})")
                    # Show Edugain-style explanation
                    with st.expander("🛠️ Show How to Solve / எப்படி தீர்ப்பது?", expanded=True):
                        st.write(q['logic'])
                
                if st.button("Next Question / அடுத்த கேள்வி ➡️", use_container_width=True):
                    st.session_state.math_q += 1
                    st.session_state.math_answered = False
                    st.session_state.math_result = None
                    st.session_state.current_math_q = None
                    if st.session_state.math_q > 10:
                        save_result(token, "Mathematics", st.session_state.math_score)
                    st.rerun()
    else:
        st.success("Challenge Completed! / சவால் முடிந்தது!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.math_score}/10")
        if st.button("Back to Dashboard", use_container_width=True):
            if 'math_q' in st.session_state: del st.session_state.math_q
            st.session_state.page = "dashboard"
            st.rerun()
