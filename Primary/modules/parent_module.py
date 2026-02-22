import streamlit as st
import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'school.db')

def render_parent_corner(token):
    # Fetch Student Info
    conn = sqlite3.connect(DB_PATH)
    student_info = pd.read_sql_query("SELECT student_name, grade, parent_name FROM tokens WHERE token = ?", conn, params=(token,))
    conn.close()
    
    student_name = student_info['student_name'].iloc[0] if not student_info.empty else "Student"
    
    st.markdown(f"""
    <div style='background-color: #f1f1f1; padding: 10px; border-radius: 5px; border-left: 5px solid #34495e; font-family: sans-serif;'>
        <h2 style='margin: 0;'>Parent's Performance Dashboard / பெற்றோர் பகுதி 👨‍👩‍👦</h2>
        <p style='color: #555;'>Tracking Progress for: <b>{student_name}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Daily Progress / தினசரி முன்னேற்றம்", "Improvement Tips / முன்னேற்ற குறிப்புகள்", "Ask Teacher / ஆசிரியரிடம் கேட்க"])
    
    with tab1:
        st.subheader("Daily Activity / இன்றைய செயல்பாடு")
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT module, score, timestamp FROM results WHERE token = ?"
        df = pd.read_sql_query(query, conn, params=(token,))
        conn.close()
        
        if not df.empty:
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            today = datetime.now().date()
            df_today = df[df['date'] == today]
            
            if not df_today.empty:
                st.success(f"Great! {student_name} completed {len(df_today)} modules today.")
                st.dataframe(df_today[['module', 'score', 'timestamp']].sort_values(by='timestamp', ascending=False), use_container_width=True)
            else:
                st.warning("No modules completed today yet. Encourage them to try one!")
            
            st.divider()
            st.write("### All-Time Performance History")
            st.dataframe(df.sort_values(by='timestamp', ascending=False), use_container_width=True)
        else:
            st.info("No learning activities detected yet.")

    with tab2:
        st.subheader("How to Improve Scores / மதிப்பெண்களை உயர்த்த")
        if not df.empty:
            avg_score = df['score'].mean()
            if avg_score < 3:
                st.error("💡 **Focus Area:** The average score is currently below 3. Suggest focusing on fundamental reading and math practice daily.")
            elif avg_score < 4.5:
                st.warning("💪 **Focus Area:** Good progress! To reach the top level, try practicing the 'Typing' and 'Aptitude' modules twice a day.")
            else:
                st.success("🌟 **Focus Area:** Excellent work! Encourage the student to maintain this consistency and try explaining the topics to others.")
        else:
            st.info("Start practicing modules to see improvement tips here!")

    with tab3:
        st.subheader("Message the Teacher / ஆசிரியருக்கு செய்தி")
        parent_query = st.text_area("Enter your question or request / உங்கள் கேள்வி அல்லது கோரிக்கையை உள்ளிடவும்")
        if st.button("Send to Teacher / அனுப்பவும்"):
            if parent_query:
                from utils.database import save_feedback
                from utils.telegram_bot import send_telegram_alert
                
                # Save to DB
                save_feedback(token, parent_query)
                
                # Send Telegram Alert
                msg = f"📩 *New Message from Parent*\n\n*Student Token:* `{token}`\n*Message:* {parent_query}\n\n_Please check the Admin Panel to reply._"
                send_telegram_alert(msg)
                
                st.success("✅ Your message has been sent to the teacher! / உங்கள் செய்தி ஆசிரியருக்கு அனுப்பப்பட்டது!")
            else:
                st.warning("Please write something first. / தயவுசெய்து எதாவது எழுதவும்.")

    st.divider()
    if st.button("Back to Dashboard / முகப்பிற்குத் திரும்பவும்"):
        st.session_state.page = "dashboard"
        st.rerun()
