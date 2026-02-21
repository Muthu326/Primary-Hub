import streamlit as st
import random
from utils.database import save_result

def render_listening_module(language, token):
    # Seed based on token to ensure unique experience per student
    random.seed(token)
    import time
    
    st.markdown("""
    <div style='background-color: #34495e; color: white; padding: 15px; border-radius: 10px; border-left: 8px solid #E91E63; margin-bottom: 20px;'>
        <h2 style='margin: 0; color: white;'>Listening Skill / கேட்டல் திறன் 🎧</h2>
        <p style='margin: 0; color: #e0e0e0;'>10-Question Story Challenge! / 10 கதைகள் சவால்!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'listen_q' not in st.session_state:
        st.session_state.listen_q = 1
        st.session_state.listen_score = 0

    stories_pool = [
        {"title": "The Thirsty Crow", "story": "Once there was a clever crow. He was thirsty. He found a pot with little water. He dropped pebbles to raise the water level.", "q": "What did the crow use?", "options": ["Pebbles", "Sticks", "Sand"], "ans": "Pebbles", "level": 1},
        {"title": "The Lion and Mouse", "story": "A small mouse saved a lion's life by cutting a net. Small friends can be great friends.", "q": "Who saved the lion?", "options": ["Mouse", "Tiger", "Dog"], "ans": "Mouse", "level": 1},
        {"title": "The Hare and Tortoise", "story": "The tortoise won because he was slow and steady. The hare slept because of overconfidence.", "q": "Why did the tortoise win?", "options": ["Slow and Steady", "Speed", "Luck"], "ans": "Slow and Steady", "level": 1},
        {"title": "The Ant and Grasshopper", "story": "The ant worked hard in summer. The grasshopper sang. In winter, the ant had food but the grasshopper was hungry.", "q": "Who was hungry in winter?", "options": ["Grasshopper", "Ant", "Bird"], "ans": "Grasshopper", "level": 2},
        {"title": "The Honest Woodcutter", "story": "A woodcutter lost his axe in the river. A deity offered a gold axe, but he refused saying only the iron one was his. He was rewarded for honesty.", "q": "Was he honest?", "options": ["Yes", "No", "Maybe"], "ans": "Yes", "level": 2},
        {"title": "The Boy Who Cried Wolf", "story": "A boy lied about a wolf. One day a real wolf came, and no one helped him.", "q": "What is the lesson?", "options": ["Don't Lie", "Wolves are fast", "Running is fun"], "ans": "Don't Lie", "level": 2},
        {"title": "The Fox and Grapes", "story": "A fox failed to reach some grapes and called them sour. We often hate what we can't have.", "q": "Why did he call them sour?", "options": ["Couldn't reach", "They were red", "He was full"], "ans": "Couldn't reach", "level": 3},
        {"title": "The Golden Touch", "story": "King Midas wanted everything he touched to turn to gold. He soon couldn't eat or hug his daughter.", "q": "Was the wish good?", "options": ["No", "Yes", "Very Good"], "ans": "No", "level": 3},
        {"title": "The Ugly Duckling", "story": "A duckling felt ugly because he was different. Later, he grew into a beautiful swan.", "q": "What did he become?", "options": ["Swan", "Duck", "Eagle"], "ans": "Swan", "level": 3},
        {"title": "The Bundle of Sticks", "story": "An old man showed his sons that sticks together are strong, but alone mereka break easily.", "q": "Unity is...?", "options": ["Strength", "Weakness", "Boring"], "ans": "Strength", "level": 3}
    ]
    
    if st.session_state.listen_q <= 10:
        story = stories_pool[st.session_state.listen_q - 1]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Progress")
            st.write(f"Question: **{st.session_state.listen_q}/10**")
            st.progress(st.session_state.listen_q / 10)
            
            diff_color = "#E91E63"
            st.markdown(f"<div style='background: {diff_color}; color: white; padding: 5px 10px; border-radius: 5px; text-align: center; font-weight: bold;'>Level {story['level']}</div>", unsafe_allow_html=True)
            
        with col2:
            st.subheader(f"Story: {story['title']}")
            st.info(story['story'])
            st.divider()
            st.write(f"**{story['q']}**")
            
            user_choice = st.radio("Select Answer:", story['options'], key=f"listen_in_{st.session_state.listen_q}")
            
            if st.button("Submit Answer", use_container_width=True):
                if user_choice == story['ans']:
                    st.success("Correct! 🎉")
                    st.session_state.listen_score += 1
                else:
                    st.error(f"Try again! (Correct: {story['ans']})")
                
                st.session_state.listen_q += 1
                if st.session_state.listen_q > 10:
                    save_result(token, "Listening", st.session_state.listen_score)
                time.sleep(1)
                st.rerun()
    else:
        st.success("Great Observation! You finished the Listening challenge!")
        st.balloons()
        st.write(f"### Final Score: {st.session_state.listen_score}/10")
        if st.button("Back to Dashboard", use_container_width=True):
            if 'listen_q' in st.session_state: del st.session_state.listen_q
            st.session_state.page = "dashboard"
            st.rerun()
