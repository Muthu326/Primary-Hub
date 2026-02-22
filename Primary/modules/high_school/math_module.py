import streamlit as st
import random
import math
from utils.database import save_result

def render_hs_math_module(token, grade):
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #FFC107; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>High School Mathematics / கணிதச் சவால் 🔢</h2>
        <p style='margin: 0; color: #e0e0e0;'>Grade {grade} Advanced Problem Solving</p>
    </div>
    """.format(grade=grade), unsafe_allow_html=True)

    if 'hs_math_history' not in st.session_state:
        st.session_state.hs_math_history = []

    if st.session_state.hs_math_q <= 10:
        if st.session_state.current_hs_math_q is None:
            max_attempts = 10
            while max_attempts > 0:
                # Topic selection based on Grade
                if grade <= 7:
                    topics = ['Algebra Bases', 'Geometry', 'Integers']
                else:
                    topics = ['Trigonometry', 'Algebraic Equations', 'Statistics', 'Geometry Advanced']
                
                topic = random.choice(topics)
                
                if topic == 'Algebra Bases':
                    x = random.randint(2, 20)
                    multiplier = random.randint(2, 5)
                    eq = f"{multiplier}x = {x*multiplier}"
                    q_body = f"Solve for x: {eq}"
                    a = str(x)
                    o = [str(x), str(x+random.randint(2,5)), str(abs(x-random.randint(1,4)))]
                    logic = f"Divide both sides by {multiplier}: x = {x*multiplier}/{multiplier} = {x}."
                
                elif topic == 'Integers':
                    n1 = random.randint(-20, 20)
                    n2 = random.randint(-20, 20)
                    q_body = f"Evaluate: ({n1}) + ({n2}) = ?"
                    a = str(n1 + n2)
                    o = [a, str(n1 - n2), str(-(n1 + n2))]
                    logic = f"Adding {n1} and {n2} results in {a}."

                elif topic == 'Geometry':
                    r = random.choice([7, 14, 21, 28, 3.5])
                    q_body = f"Area of a circle with radius r={r} cm? (Take π ≈ 22/7)"
                    ans_val = (22/7) * r * r
                    a = f"{ans_val:.1f}"
                    o = [a, f"{2*(22/7)*r:.1f}", f"{r*r:.1f}"]
                    logic = f"Area = πr² = (22/7) * {r} * {r} = {a}."
                
                elif topic == 'Algebraic Equations':
                    a_val = random.randint(1, 9)
                    b_val = random.randint(1, 9)
                    q_body = f"Expand (x + {a_val})(x + {b_val})"
                    a = f"x² + {a_val+b_val}x + {a_val*b_val}"
                    o = [a, f"x² + {a_val*b_val}x + {a_val+b_val}", f"x² + {a_val+b_val}"]
                    logic = f"Using distributive property: x(x) + x({b_val}) + {a_val}(x) + {a_val}({b_val}) = x² + {a_val+b_val}x + {a_val*b_val}."
                
                elif topic == 'Geometry Advanced':
                    base = random.randint(5, 15)
                    height = random.randint(4, 12)
                    q_body = f"Calculate the Area of a Triangle with Base={base}cm and Height={height}cm."
                    ans_val = 0.5 * base * height
                    a = f"{ans_val:.1f}"
                    o = [a, f"{base*height:.1f}", f"{base+height:.1f}"]
                    logic = f"Area = 1/2 * base * height = 1/2 * {base} * {height} = {a}."

                elif topic == 'Statistics':
                    nums = [random.randint(1, 20) for _ in range(5)]
                    mean = sum(nums)/len(nums)
                    q_body = f"Find the Mean (Average) of these numbers: {nums}"
                    a = f"{mean:.1f}"
                    o = [a, f"{mean+2:.1f}", f"{mean-1.5:.1f}"]
                    logic = f"Mean = Sum / Count = ({' + '.join(map(str, nums))}) / 5 = {sum(nums)} / 5 = {a}."

                else: # Trigonometry
                    angle = random.choice([0, 30, 45, 60, 90])
                    funcs = {'sin': {30: '0.5', 45: '1/√2', 60: '√3/2', 90: '1', 0: '0'}, 
                             'cos': {30: '√3/2', 45: '1/√2', 60: '0.5', 90: '0', 0: '1'}}
                    f_name = random.choice(['sin', 'cos'])
                    q_body = f"What is the value of {f_name}({angle}°)? / {f_name}({angle}°)-இன் மதிப்பு என்ன?"
                    a = funcs[f_name][angle]
                    o = list(set([a, '0', '1', '0.5', '√3/2']))
                    logic = f"Based on the standard trigonometric table, {f_name}({angle}°) is {a}."

                # Check for Duplicates
                if q_body not in st.session_state.hs_math_history:
                    st.session_state.hs_math_history.append(q_body)
                    st.session_state.current_hs_math_q = {"q": q_body, "a": a, "o": random.sample(o, len(o)), "logic": logic}
                    break
                max_attempts -= 1

        q = st.session_state.current_hs_math_q
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"Question: **{st.session_state.hs_math_q}/10**")
            st.progress(st.session_state.hs_math_q / 10)
            st.metric("Score", st.session_state.hs_math_score)

        with col2:
            st.subheader(q['q'])
            st.write("### Choose the correct solution:")
            
            btn_cols = st.columns(len(q['o']))
            if not st.session_state.hs_math_answered:
                for i, opt in enumerate(q['o']):
                    if btn_cols[i].button(opt, key=f"m_opt_{i}"):
                        st.session_state.hs_math_answered = True
                        if opt == q['a']:
                            st.session_state.hs_math_result = "correct"
                            st.session_state.hs_math_score += 1
                        else:
                            st.session_state.hs_math_result = "incorrect"
                        st.rerun()
            else:
                if st.session_state.hs_math_result == "correct":
                    st.success("Correct! Mathematical Genius! ✨")
                else:
                    st.error(f"Incorrect. The correct expansion/answer is: {q['a']}")
                    with st.expander("Step-by-Step Logic", expanded=True):
                        st.write(q['logic'])
                
                if st.button("Next Problem ➡️", use_container_width=True):
                    st.session_state.hs_math_q += 1
                    st.session_state.hs_math_answered = False
                    st.session_state.current_hs_math_q = None
                    if st.session_state.hs_math_q > 10:
                        save_result(token, "HS_Math", st.session_state.hs_math_score)
                    st.rerun()
    else:
        st.success("Mathematical Master! You finished the High School challenge!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.hs_math_score}/10")
        if st.button("Back to Dashboard", use_container_width=True):
            if 'hs_math_q' in st.session_state: del st.session_state.hs_math_q
            st.session_state.page = "dashboard"
            st.rerun()
