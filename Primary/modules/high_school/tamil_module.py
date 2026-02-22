import streamlit as st
import random
from utils.database import save_result

def render_hs_tamil_module(token, grade):
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #FF5722; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Tamil Proficiency / தமிழ் மொழித் திறன் 📕</h2>
        <p style='margin: 0; color: #e0e0e0;'>Grade {grade} Literary Challenge / இலக்கியச் சவால்</p>
    </div>
    """.format(grade=grade), unsafe_allow_html=True)

    if 'hs_tamil_q' not in st.session_state:
        st.session_state.hs_tamil_q = 1
        st.session_state.hs_tamil_score = 0
        st.session_state.hs_tamil_answered = False
        st.session_state.hs_tamil_result = None
        st.session_state.current_hs_tamil_q = None

    # Sample High School Tamil Questions (Grammar & Literature)
    questions_pool = [
        {"q": "திருக்குறளை இயற்றியவர் யார்?", "o": ["கம்பர்", "திருவள்ளுவர்", "பாரதியார்"], "a": "திருவள்ளுவர்", "logic": "திருக்குறள் திருவள்ளுவரால் இயற்றப்பட்டது."},
        {"q": "தமிழ் எழுத்துக்களின் மொத்த எண்ணிக்கை எவ்வளவு?", "o": ["216", "247", "18"], "a": "247", "logic": "உயிர் 12, மெய் 18, உயிர்மெய் 216, ஆய்தம் 1 = 247."},
        {"q": "சிலப்பதிகாரத்தின் நாயகி யார்?", "o": ["சீதை", "மணிமேகலை", "கண்ணகி"], "a": "கண்ணகி", "logic": "சிலப்பதிகாரம் கண்ணகியின் வரலாற்றைக் கூறுகிறது."},
        {"q": "மூதுரை நூலை எழுதியவர் யார்?", "o": ["ஒளவையார்", "கம்பர்", "பாரதிதாசன்"], "a": "ஒளவையார்", "logic": "மூதுரை ஒளவையாரால் எழுதப்பட்டது."},
        {"q": "இயல், இசை, நாடகம் - இவை மூன்றும் எவ்வாறு அழைக்கப்படுகின்றன?", "o": ["மும்முரசு", "முத்தமிழ்", "முக்கனி"], "a": "முத்தமிழ்", "logic": "இவை தமிழின் மூன்று பிரிவுகள் (முத்தமிழ்)."}
    ]

    if st.session_state.hs_tamil_q <= 10:
        if st.session_state.current_hs_tamil_q is None:
            st.session_state.current_hs_tamil_q = random.choice(questions_pool)
        
        q = st.session_state.current_hs_tamil_q
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"Question: **{st.session_state.hs_tamil_q}/10**")
            st.progress(st.session_state.hs_tamil_q / 10)
            st.metric("Score", st.session_state.hs_tamil_score)

        with col2:
            st.subheader(q['q'])
            st.write("### சரியான விடையைத் தேர்வு செய்க:")
            
            btn_cols = st.columns(len(q['o']))
            if not st.session_state.hs_tamil_answered:
                for i, opt in enumerate(q['o']):
                    if btn_cols[i].button(opt, key=f"t_opt_{i}"):
                        st.session_state.hs_tamil_answered = True
                        if opt == q['a']:
                            st.session_state.hs_tamil_result = "correct"
                            st.session_state.hs_tamil_score += 1
                        else:
                            st.session_state.hs_tamil_result = "incorrect"
                        st.rerun()
            else:
                if st.session_state.hs_tamil_result == "correct":
                    st.success("நன்று! மிகச் சரியான விடை! ✨")
                else:
                    st.error(f"தவறு. சரியான விடை: {q['a']}")
                    with st.expander("விளக்கம்", expanded=True):
                        st.write(q['logic'])
                
                if st.button("அடுத்த கேள்வி ➡️", use_container_width=True):
                    st.session_state.hs_tamil_q += 1
                    st.session_state.hs_tamil_answered = False
                    st.session_state.current_hs_tamil_q = None
                    if st.session_state.hs_tamil_q > 10:
                        save_result(token, "HS_Tamil", st.session_state.hs_tamil_score)
                    st.rerun()
    else:
        st.success("வாழ்த்துகள்! நீங்கள் தமிழ்த் தேர்வை முடித்துவிட்டீர்கள்!")
        st.balloons()
        st.write(f"### மொத்த மதிப்பெண்: {st.session_state.hs_tamil_score}/10")
        if st.button("முகப்பிற்குத் திரும்பவும்", use_container_width=True):
            if 'hs_tamil_q' in st.session_state: del st.session_state.hs_tamil_q
            st.session_state.page = "dashboard"
            st.rerun()
