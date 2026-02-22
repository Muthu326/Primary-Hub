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

    if 'hs_math_q' not in st.session_state:
        st.session_state.hs_math_q = 1
        st.session_state.hs_math_score = 0
        st.session_state.hs_math_answered = False
        st.session_state.hs_math_result = None
        st.session_state.current_hs_math_q = None

    if st.session_state.hs_math_q <= 10:
        if st.session_state.current_hs_math_q is None:
            # Topic selection based on Grade
            if grade <= 7:
                topics = ['Algebra Bases', 'Geometry']
            else:
                topics = ['Trigonometry', 'Algebraic Equations', 'Statistics']
            
            topic = random.choice(topics)
            
            if topic == 'Algebra Bases':
                x = random.randint(2, 6)
                eq = f"{x}x = {x*x}"
                q = f"Solve for x: {eq}"
                a = str(x)
                o = [str(x), str(x+2), str(x*2)]
                logic = f"Divide both sides by {x}: x = {x*x}/{x} = {x}."
            elif topic == 'Geometry':
                r = random.randint(7, 14)
                q = f"Area of a circle with radius r={r}? (Take π ≈ 22/7)"
                a = str(int((22/7) * r * r))
                o = [a, str(int(2 * (22/7) * r)), str(r*r)]
                logic = f"Area = πr² = (22/7) * {r} * {r} = {a}."
            elif topic == 'Algebraic Equations':
                a_val = random.randint(1, 5)
                b_val = random.randint(1, 5)
                # (x + a)(x + b) = x^2 + (a+b)x + ab
                q = f"Expand (x + {a_val})(x + {b_val})"
                a = f"x² + {a_val+b_val}x + {a_val*b_val}"
                o = [a, f"x² + {a_val*b_val}x + {a_val+b_val}", f"x² + {a_val+b_val}"]
                logic = f"Using FOIL/Distribution: x(x) + x({b_val}) + {a_val}(x) + {a_val}({b_val}) = x² + {a_val+b_val}x + {a_val*b_val}."
            else: # Trigonometry or Stats
                q = "What is sin(90°)?"
                a = "1"
                o = ["0", "0.5", "1"]
                logic = "The value of the sine function at 90 degrees is exactly 1."

            st.session_state.current_hs_math_q = {"q": q, "a": a, "o": random.sample(o, len(o)), "logic": logic}

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
