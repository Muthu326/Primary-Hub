import streamlit as st
import random
from utils.database import save_result

def render_writing_module(language, token):
    # random.seed(token)
    import time
    
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #9C27B0; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Writing Skill / எழுத்துப் பயிற்சி ✍️</h2>
        <p style='margin: 0; color: #e0e0e0;'>10-Sentence Story Builder! / 10 வரிகள் எழுத்து சவால்!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'write_q' not in st.session_state:
        st.session_state.write_q = 1
        st.session_state.write_sentences = []
        st.session_state.write_answered = False

    prompts = [
        "What is your name? / உன் பெயர் என்ன?",
        "Where do you live? / நீ எங்கே வசிக்கிறாய்?",
        "What is your favorite fruit? / உனக்கு பிடித்த பழம் எது?",
        "Why do you like it? / அது உனக்கு ஏன் பிடிக்கும்?",
        "Who is your best friend? / உன் சிறந்த நண்பன் யார்?",
        "What subject do you like? / உனக்கு ஒரு பிடிக்கும் பாடம் எது?",
        "What is your hobby? / உன் பொழுதுபோக்கு என்ன?",
        "What do you want to become? / நீ பெரியவனாகி என்னவாகப் போகிறாய்?",
        "Describe your school in 1 word. / உன் பள்ளியை ஒரு வார்த்தையில் விவரி.",
        "Write a thank you note to your teacher. / உன் ஆசிரியருக்கு ஒரு நன்றி குறிப்பு எழுதுக."
    ]
    
    if st.session_state.write_q <= 10:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Progress")
            st.write(f"Sentence: **{st.session_state.write_q}/10**")
            st.progress(st.session_state.write_q / 10)
            
            # Sentence History
            if st.session_state.write_sentences:
                st.divider()
                st.write("Your Story So Far:")
                for i, s in enumerate(st.session_state.write_sentences):
                    st.write(f"{i+1}. {s}")
            
        with col2:
            st.subheader(f"Step {st.session_state.write_q}: {prompts[st.session_state.write_q-1]}")
            user_text = st.text_input("Type your sentence here... / இங்கே எழுதவும்...", key=f"write_in_{st.session_state.write_q}", disabled=st.session_state.write_answered)
            
            if not st.session_state.write_answered:
                if st.button("Add to Story / கதையில் சேர்க்கவும்", use_container_width=True):
                    if len(user_text.strip()) > 3:
                        st.session_state.write_temp_text = user_text
                        st.session_state.write_answered = True
                        st.rerun()
                    else:
                        st.warning("Please write a bit more! / தயவுசெய்து இன்னும் கொஞ்சம் எழுதவும்.")
            else:
                st.success("Great sentence! / அருமையான வாக்கியம்! ✨")
                if st.button("Next Sentence / அடுத்த வரி ➡️", use_container_width=True):
                    st.session_state.write_sentences.append(st.session_state.write_temp_text)
                    st.session_state.write_q += 1
                    st.session_state.write_answered = False
                    if st.session_state.write_q > 10:
                        save_result(token, "Writing", 100)
                    st.rerun()
    else:
        st.success("Author! You finished your 10-sentence story!")
        st.balloons()
        st.write("### Your Final Piece:")
        st.info(" ".join(st.session_state.write_sentences))
        
        if st.button("Back to Dashboard", use_container_width=True):
            if 'write_q' in st.session_state: del st.session_state.write_q
            if 'write_sentences' in st.session_state: del st.session_state.write_sentences
            st.session_state.page = "dashboard"
            st.rerun()
