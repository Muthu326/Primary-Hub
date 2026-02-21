import streamlit as st
import random
from utils.database import save_result

def render_speaking_module(language, token):
    # Seed based on token to ensure unique experience per student
    random.seed(token)
    import time
    
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #2196F3; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Speaking Skill / மேடை பேச்சுத் திறன் 🎤</h2>
        <p style='margin: 0; color: #e0e0e0;'>10-Step Confidence Builder! / 10 படிகள் பேச்சாற்றல் சவால்!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'speak_q' not in st.session_state:
        st.session_state.speak_q = 1
        st.session_state.speak_score = 0

    steps = [
        {"topic": "Hand Washing (Class 1) / கைகளை கழுவுதல்", "ta": "சுத்தம் மற்றும் ஆரோக்கியம்", "points": ["நாம் தினமும் கைகளை கழுவ வேண்டும். / We must wash hands daily.", "சுத்தமாக இருந்தால் நோய் வராது. / Cleanliness prevents disease.", "முடிவு: சுத்தம் = ஆரோக்கியம் / Conclusion: Cleanliness = Health"]},
        {"topic": "Sharing with Friends (Class 2) / பகிர்ந்து கொள்ளுதல்", "ta": "நட்பு மற்றும் ஒற்றுமை", "points": ["பகிர்ந்தால் நட்பு அதிகரிக்கும். / Sharing increases friendship.", "பகிர்ந்து கொள்வது நல்ல பழக்கம். / Sharing is a good habit.", "முடிவு: பகிர்வு = நட்பு / Conclusion: Sharing = Friendship"]},
        {"topic": "Healthy Food (Class 3) / ஆரோக்கியமான உணவு", "ta": "சத்தான உணவு", "points": ["பழங்கள், காய்கறிகள் சாப்பிட்டால் உடல் ஆரோக்கியமாகும். / Fruits and vegetables make the body healthy.", "சத்தான உணவு நல்ல உடல் கொடுக்கும். / Nutritious food gives a healthy body.", "முடிவு: சத்தான உணவு = நல்ல உடல் / Conclusion: Healthy Food = Healthy Body"]},
        {"topic": "Effort without Fear (Class 4) / முயற்சி", "ta": "தன்னம்பிக்கை மற்றும் பொறுமை", "points": ["தோல்வி வந்தாலும் பயப்பட வேண்டாம். / Don't be afraid of failure.", "மீண்டும் முயற்சி செய்தால் வெற்றி வரும். / Success comes with repeated effort.", "முடிவு: முயற்சி = வெற்றி / Conclusion: Effort = Success"]},
        {"topic": "Self-Confidence (Class 5) / தன்னம்பிக்கை", "ta": "நம்பிக்கை மற்றும் சாதனை", "points": ["நான் செய்ய முடியும் என்று தினமும் சொல்லுதல். / Say 'I can do it' every day.", "தன்னம்பிக்கை இருந்தால் சாதனைகள் செய்யலாம். / Confidence leads to achievements.", "முடிவு: தன்னம்பிக்கை = வெற்றி / Conclusion: Confidence = Success"]},
        {"topic": "Introduce Yourself / உங்களைப் பற்றி", "ta": "அறிமுகம்", "points": ["My name is...", "I am studying in grade..."]},
        {"topic": "APJ Abdul Kalam / அப்துல் கலாம்", "ta": "தலைவர்கள்", "points": ["He was the Missile Man.", "He loved students."]},
        {"topic": "Mahatma Gandhi / மகாத்மா காந்தி", "ta": "தலைவர்கள்", "points": ["He fought for freedom.", "He followed Ahimsa."]},
        {"topic": "My Aim / என் லட்சியம்", "ta": "எதிர்காலம்", "points": ["I want to become a...", "I will work hard for it."]},
        {"topic": "Final Speed Round / வேகப் பேச்சு", "ta": "தன்னம்பிக்கை", "points": ["I am confident! / எனக்குத் தன்னம்பிக்கை உண்டு!", "I can speak on any stage! / என்னால் எந்த மேடையிலும் பேச முடியும்!"]}
    ]
    
    if st.session_state.speak_q <= 10:
        step = steps[st.session_state.speak_q - 1]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Progress")
            st.write(f"Step: **{st.session_state.speak_q}/10**")
            st.progress(st.session_state.speak_q / 10)
            
            st.divider()
            st.info("💡 Pronounce each word clearly!")
            
        with col2:
            st.subheader(f"Step {st.session_state.speak_q}: {step['topic']}")
            st.markdown(f"**Tamil:** {step['ta']}")
            st.success("Points to speak / பேச வேண்டிய குறிப்புகள்:")
            for p in step['points']:
                st.write(f"✅ {p}")
            
            st.divider()
            if st.button("I Spoke Clearly! / நான் தெளிவாகப் பேசினேன்!", use_container_width=True):
                st.session_state.speak_score += 1
                st.session_state.speak_q += 1
                if st.session_state.speak_q > 10:
                    save_result(token, "Speaking", 100)
                time.sleep(0.5)
                st.rerun()
    else:
        st.success("Orator! You finished the Speaking challenge!")
        st.balloons()
        st.write(f"### Completion: 10/10 Steps")
        if st.button("Back to Dashboard", use_container_width=True):
            if 'speak_q' in st.session_state: del st.session_state.speak_q
            st.session_state.page = "dashboard"
            st.rerun()
