import streamlit as st
import sqlite3
import os
import random
import string
import pandas as pd
import socket
from utils.database import get_connection, DB_PATH


def get_local_ip():
    """Auto-detect the computer's local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def render_admin_panel():
    st.title("👨‍🏫 Teacher / Admin Panel - Advanced Analytics")
    
    # Navigation Sidebar for Admin
    with st.sidebar:
        st.divider()
        if st.button("Logout Admin", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()

    # Load Data
    conn = get_connection()
    df_tokens = pd.read_sql_query("SELECT * FROM tokens", conn)
    df_results = pd.read_sql_query("SELECT * FROM results", conn)
    conn.close()

    pending_count = len(df_tokens[df_tokens['status'] == 'pending'])
    
    tab_guide, tab1, tab_appr, tab2, tab3, tab_acc = st.tabs([
        "📖 Admin Guide",
        "Manage All Tokens", 
        f"Approve Requests ({pending_count}) 📝", 
        "Full Monitoring", 
        "Top 5 Rankings",
        "Access & URLs 📡"
    ])

    with tab_guide:
        st.info("### 🛡️ How to Manage Your School Hub")
        st.markdown("""
        **Step 1: Student Sign-Up**
        - Students go to the website and click **'Request New Access'**.
        - They enter their **Name, Parent's Name, Class,** and **Year**.
        
        **Step 2: Your Approval (Crucial)**
        - You will get a **Telegram Alert** on your phone.
        - Go to the **'Approve Requests'** tab here.
        - Click **'Approve'** to let them in.
        
        **Step 3: Monitor Progress**
        - Go to **'Full Monitoring'** to see scores in real-time.
        - Use the **'Access & URLs'** tab to show students where to log in.
        """)
        st.success("💡 **Tip:** Keep this panel open on your main computer during class!")

    # Merge data for better monitoring
    df_merged = pd.merge(df_results, df_tokens, on='token', how='left')

    with tab1:
        st.subheader("Create New Student Tokens")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Student Name")
        with col2:
            grade = st.selectbox("Grade", [1, 2, 3, 4, 5])
        
        if st.button("Generate Token"):
            if name:
                from utils.database import request_token # Reuse the sequential logic
                token = request_token(name, grade, "Staff Generated", status='active')
                # request_token already handles the DB insert
                st.success(f"Token created for {name}: **{token}**")
                st.rerun()
            else:
                st.warning("Please enter a student name.")

        st.divider()
        st.write("### Active & Admin Tokens")
        st.write("Full control to manage every student's access.")
        
        active_tokens = df_tokens[df_tokens['status'] != 'pending']
        for _, row in active_tokens.iterrows():
            with st.expander(f"{row['student_name']} (Grade {row['grade']}) - {row['token']}"):
                st.write(f"Status: **{row['status'].upper()}**")
                if row['status'] != 'admin':
                    if st.button(f"Delete/Revoke Token: {row['token']}", key=f"del_{row['token']}"):
                        conn = get_connection()
                        c = conn.cursor()
                        c.execute("DELETE FROM tokens WHERE token=?", (row['token'],))
                        conn.commit()
                        conn.close()
                        st.warning(f"Access Revoked for {row['student_name']}")
                        st.rerun()

    with tab_appr:
        st.subheader("New Sign-Up Requests")
        pending = df_tokens[df_tokens['status'] == 'pending']
        
        if not pending.empty:
            for index, row in pending.iterrows():
                with st.expander(f"Request from: {row['student_name']} (Grade {row['grade']})"):
                    st.write(f"**Token ID:** `{row['token']}`")
                    col1, col2 = st.columns(2)
                    if col1.button(f"Approve {row['token']}", key=f"appr_{row['token']}"):
                        conn = sqlite3.connect(DB_PATH)
                        c = conn.cursor()
                        c.execute("UPDATE tokens SET status='active' WHERE token=?", (row['token'],))
                        conn.commit()
                        conn.close()
                        st.success(f"Approved {row['student_name']}!")
                        st.rerun()
                    if col2.button(f"Reject {row['token']}", key=f"rej_{row['token']}"):
                        conn = sqlite3.connect(DB_PATH)
                        c = conn.cursor()
                        c.execute("DELETE FROM tokens WHERE token=?", (row['token'],))
                        conn.commit()
                        conn.close()
                        st.warning(f"Rejected {row['student_name']}.")
                        st.rerun()
        else:
            st.info("No pending requests! Everything is up to date. ✅")

    with tab2:
        st.subheader("🔍 Student Participation & Pass Monitoring")
        
        # Filtering
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_grade = st.selectbox("Filter by Grade", ["All", 1, 2, 3, 4, 5])
        with col_f2:
            filter_pass = st.selectbox("Pass/Fail Filter (Score >= 3)", ["All", "Pass", "Fail"])

        # Apply Grade Filter
        df_mon = df_merged.copy()
        if filter_grade != "All":
            df_mon = df_mon[df_mon['grade'] == filter_grade]
        
        # Apply Pass Filter
        if filter_pass == "Pass":
            df_mon = df_mon[df_mon['score'] >= 3]
        elif filter_pass == "Fail":
            df_mon = df_mon[df_mon['score'] < 3]

        st.metric("Total Assessments Participated", len(df_mon))
        
        search_query = st.text_input("🔍 Search by Token or Student Name", "")
        if search_query:
            df_mon = df_mon[
                df_mon['token'].str.contains(search_query, case=False, na=False) | 
                df_mon['student_name'].str.contains(search_query, case=False, na=False)
            ]

        st.write("### Detailed Activity Log")
        st.write("See exactly which student (Name + Class) attended which exam using their unique token.")
        
        # Format the table for high clarity
        display_mon = df_mon[['student_name', 'parent_name', 'academic_year', 'grade', 'token', 'module', 'score', 'timestamp']].sort_values(by='timestamp', ascending=False)
        display_mon.columns = ['Student Name', 'Parent Name', 'Year', 'Class/Grade', 'Unique Token', 'Module Name', 'Marks Obtained', 'Time Taken']
        
        st.dataframe(display_mon, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("🏆 Top 5 Leaderboard")
        target_lb = st.selectbox("Leaderboard for Grade:", ["Overall", 1, 2, 3, 4, 5])
        
        df_lb = df_merged.copy()
        if target_lb != "Overall":
            df_lb = df_lb[df_lb['grade'] == int(target_lb)]
            
        if not df_lb.empty:
            top_students = df_lb.groupby(['student_name', 'token']).agg({
                'score': 'mean', 
                'module': 'count'
            }).rename(columns={'score': 'Average Score', 'module': 'Tests Completed'})
            top_5 = top_students.sort_values(by='Average Score', ascending=False).head(5)
            
            for i, (idx, row) in enumerate(top_5.iterrows()):
                st.markdown(f"#### {i+1}. {idx[0]} ({idx[1]})")
                st.progress(row['Average Score']/5.0 if row['Average Score'] <= 5 else 1.0)
                st.info(f"Avg Score: {row['Average Score']:.2f} | Tests: {int(row['Tests Completed'])}")
        else:
            st.info("No results found.")

    with tab_acc:
        st.subheader("Student Access Dashboard")
        st.write("Use these URLs to help students log in from their tablets/phones.")
        
        local_ip = get_local_ip()
        
        st.markdown(f"""
        <div style='background: #e3f2fd; padding: 20px; border-radius: 15px; border: 2px solid #1565c0;'>
            <h3 style='color: #1565c0; margin-top: 0;'>📡 School WiFi Access (Recommended)</h3>
            <p>Tell students to type this into their browser:</p>
            <h2 style='color: #0d47a1;'>http://{local_ip}:8501</h2>
            <p style='font-size: 0.9rem; color: #555;'><i>(Note: Students must be on the same WiFi as this computer)</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("""
        <div style='background: #e3f2fd; padding: 20px; border-radius: 15px; border: 2px solid #1565c0;'>
            <h3 style='color: #1565c0; margin-top: 0;'>🌐 Global Website Access</h3>
            <p>If you have deployed to the web, your permanent URL is here:</p>
            <h2 style='color: #0d47a1;'>https://primary-learn-koliyankulam.streamlit.app</h2>
            <p style='font-size: 0.9rem; color: #555;'><i>(This works from anywhere in the world with internet)</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 **Teacher Tip:** You can write the WiFi URL (the blue box) on the blackboard for the whole class to see!")

if __name__ == "__main__":
    render_admin_panel()
