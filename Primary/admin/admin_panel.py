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
    # Detect Admin Division
    admin_token = st.session_state.user_data['token']
    admin_div = "High School" if (admin_token.startswith("GHS") or admin_token.startswith("GHT")) else "Primary"
    
    st.title(f"👨‍🏫 {admin_div} Admin Panel")
    if admin_token == "GHT00001":
        st.caption("🚀 High School Super Admin Access")

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
    df_feedback = pd.read_sql_query("SELECT * FROM feedback", conn)
    conn.close()

    # Filter pending count based on admin division
    pending_df = df_tokens[df_tokens['status'] == 'pending']
    if admin_div == "High School" and admin_token != "GHT00001":
        pending_df = pending_df[pending_df['school_type'] == "High School"]
    elif admin_div == "Primary":
        pending_df = pending_df[pending_df['school_type'] == "Primary"]
        
    pending_count = len(pending_df)
    
    # Filter feedback for unread count
    df_fb_merged = pd.merge(df_feedback, df_tokens[['token', 'school_type', 'student_name']], on='token', how='left')
    unread_df = df_fb_merged[df_fb_merged['status'] == 'unread']
    if admin_div == "High School" and admin_token != "GHT00001":
        unread_df = unread_df[unread_df['school_type'] == "High School"]
    elif admin_div == "Primary":
        unread_df = unread_df[unread_df['school_type'] == "Primary"]
    unread_count = len(unread_df)

    tab_guide, tab1, tab_appr, tab_msg, tab2, tab3, tab_acc = st.tabs([
        "📊 School Overview",
        "Tokens", 
        f"Approve ({pending_count})", 
        f"Messages ({unread_count}) 📩",
        "Monitoring", 
        "Rankings",
        "Access 📡"
    ])

    # Merge data for better monitoring
    df_merged = pd.merge(df_results, df_tokens, on='token', how='left')

    with tab_guide:
        st.subheader("🚀 School Operational Overview")
        
        # 1. Top Level Metrics
        m1, m2, m3, m4 = st.columns(4)
        total_active = len(df_tokens[df_tokens['status'] == 'active'])
        avg_score = df_results['score'].mean() if not df_results.empty else 0
        pass_count = len(df_results[df_results['score'] >= 3])
        pass_rate = (pass_count / len(df_results) * 100) if not df_results.empty else 0
        
        m1.metric("Active Students", total_active)
        m2.metric("Overall Avg Score", f"{avg_score:.1f}/10")
        m3.metric("Pass Rate (%)", f"{pass_rate:.1f}%")
        m4.metric("Pending Approvals", pending_count)
        
        st.divider()
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.write("### 📉 Critical Students (Need Support)")
            if not df_merged.empty:
                # Identify students with average score < 3
                crit_df = df_merged.groupby(['student_name', 'grade', 'token']).agg({'score': 'mean'}).reset_index()
                crit_df = crit_df[crit_df['score'] < 3].sort_values(by='score')
                
                if not crit_df.empty:
                    for idx, row in crit_df.iterrows():
                        st.warning(f"**{row['student_name']}** (Class {row['grade']}): Avg Score **{row['score']:.1f}/10**")
                else:
                    st.success("No students currently in critical range! 🎉")
            else:
                st.info("Waiting for assessment data...")

        with col_right:
            st.write("### 🏫 Class-wise Performance")
            if not df_merged.empty:
                def get_class_stats(group):
                    avg = group['score'].mean()
                    tests = len(group)
                    passed = len(group[group['score'] >= 3])
                    pass_rate = (passed / tests * 100) if tests > 0 else 0
                    return pd.Series({'Avg Score': f"{avg:.1f}", 'Pass Rate': f"{pass_rate:.1f}%", 'Tests': tests})
                
                class_perf = df_merged.groupby('grade').apply(get_class_stats).reset_index()
                st.dataframe(class_perf.set_index('grade'), use_container_width=True)
            else:
                st.info("No class data available yet.")

        st.write("### 📈 Student Distribution")
        if not df_tokens.empty:
            dist_df = df_tokens[df_tokens['status'] == 'active'].groupby('school_type').agg({'token': 'count'}).reset_index()
            dist_df.columns = ['Division', 'Student Count']
            st.bar_chart(dist_df.set_index('Division'))

    with tab1:
        st.subheader("Create New Student Tokens")
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Student Name")
        with col2:
            sch_div = st.selectbox("Division", ["Primary", "High School"])
        with col3:
            if sch_div == "Primary":
                grade = st.selectbox("Grade (Primary)", [1, 2, 3, 4, 5], key="admin_gr_primary")
            else:
                grade = st.selectbox("Grade (High School)", [6, 7, 8, 9, 10], key="admin_gr_hs")
        
        if st.button("Generate Token"):
            if name:
                from utils.database import request_token
                token = request_token(name, grade, "Staff Generated", "2024-25", school_type=sch_div, status='active')
                st.success(f"Token created for {name} ({sch_div}): **{token}**")
                st.rerun()
            else:
                st.warning("Please enter a student name.")

        st.divider()
        st.write(f"### {admin_div} Student Records")
        
        # Filter active tokens based on admin division
        active_tokens = df_tokens[df_tokens['status'] != 'pending']
        if admin_div == "High School" and admin_token != "GHT00001":
            active_tokens = active_tokens[active_tokens['school_type'] == "High School"]
        elif admin_div == "Primary":
            active_tokens = active_tokens[active_tokens['school_type'] == "Primary"]

        for _, row in active_tokens.iterrows():
            with st.expander(f"{row['student_name']} (Grade {row['grade']}) - {row['token']}"):
                st.write(f"Division: **{row['school_type']}**")
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
        st.subheader(f"New {admin_div} Requests")
        # pending_df contains full details from the tokens table
        if not pending_df.empty:
            for index, row in pending_df.iterrows():
                with st.expander(f"📌 {row['student_name']} (Grade {row['grade']}) - {row['token']}"):
                    st.write("### Review Applicant Details")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"👤 **Student Name:** {row['student_name']}")
                        st.write(f"👨‍👩‍👦 **Parent's Name:** {row['parent_name']}")
                    with col_b:
                        st.write(f"📅 **Academic Year:** {row['academic_year']}")
                        st.write(f"🏫 **Division:** {row['school_type']}")
                    
                    st.divider()
                    col_btn1, col_btn2 = st.columns(2)
                    if col_btn1.button(f"✅ Approve Access: {row['token']}", key=f"appr_{row['token']}", use_container_width=True):
                        conn = sqlite3.connect(DB_PATH)
                        c = conn.cursor()
                        c.execute("UPDATE tokens SET status='active' WHERE token=?", (row['token'],))
                        conn.commit()
                        conn.close()
                        st.success(f"Approved {row['student_name']}!")
                        st.rerun()
                    if col_btn2.button(f"❌ Reject & Delete: {row['token']}", key=f"rej_{row['token']}", use_container_width=True):
                        conn = sqlite3.connect(DB_PATH)
                        c = conn.cursor()
                        c.execute("DELETE FROM tokens WHERE token=?", (row['token'],))
                        conn.commit()
                        conn.close()
                        st.warning(f"Rejected {row['student_name']}.")
                        st.rerun()
        else:
            st.info(f"No pending {admin_div} requests! ✅")
            
    with tab_msg:
        st.subheader("📩 Parent Reviews & Questions")
        # df_fb_merged was created in the setup section
        display_fb = df_fb_merged.copy()
        if admin_div == "High School" and admin_token != "GHT00001":
            display_fb = display_fb[display_fb['school_type'] == "High School"]
        elif admin_div == "Primary":
            display_fb = display_fb[display_fb['school_type'] == "Primary"]
            
        if not display_fb.empty:
            for idx, row in display_fb.sort_values(by='timestamp', ascending=False).iterrows():
                status_icon = "🔵" if row['status'] == 'unread' else "⚪"
                with st.expander(f"{status_icon} From: {row['student_name']} ({row['token']}) - {row['timestamp'][:16]}"):
                    st.write(f"**Message:** {row['message']}")
                    if row['status'] == 'unread':
                        if st.button(f"Mark as Read", key=f"read_{idx}"):
                            conn = get_connection()
                            c = conn.cursor()
                            c.execute("UPDATE feedback SET status='read' WHERE token=? AND timestamp=?", (row['token'], row['timestamp']))
                            conn.commit()
                            conn.close()
                            st.rerun()
        else:
            st.info("No messages from parents yet.")

    with tab2:
        st.subheader("🔍 Assessment & Division Monitoring")
        
        # Filtering
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            div_filter = st.selectbox("Filter Division", ["All", "Primary", "High School"])
        with col_f2:
            if div_filter == "High School":
                filter_grade = st.selectbox("Filter Grade", ["All", 6, 7, 8, 9, 10])
            elif div_filter == "Primary":
                filter_grade = st.selectbox("Filter Grade", ["All", 1, 2, 3, 4, 5])
            else:
                filter_grade = st.selectbox("Filter Grade", ["All"] + list(range(1, 11)))
        with col_f3:
            filter_pass = st.selectbox("Pass/Fail Filter (Score >= 3)", ["All", "Pass", "Fail"])

        # Apply Filters
        df_mon = df_merged.copy()
        if div_filter != "All":
            df_mon = df_mon[df_mon['school_type'] == div_filter]
        if filter_grade != "All":
            df_mon = df_mon[df_mon['grade'] == int(filter_grade)]
            
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
        st.subheader("🏆 Leaderboard & Rankings")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            lb_div = st.selectbox("Rank Division:", ["All", "Primary", "High School"])
        with col_l2:
            if lb_div == "High School":
                target_lb = st.selectbox("Rank Grade:", ["Overall", 6, 7, 8, 9, 10])
            elif lb_div == "Primary":
                target_lb = st.selectbox("Rank Grade:", ["Overall", 1, 2, 3, 4, 5])
            else:
                target_lb = st.selectbox("Rank Grade:", ["Overall"])
        
        df_lb = df_merged.copy()
        if lb_div != "All":
            df_lb = df_lb[df_lb['school_type'] == lb_div]
        if target_lb != "Overall":
            df_lb = df_lb[df_lb['grade'] == int(target_lb)]
            
        if not df_lb.empty:
            # Group by token to avoid name collisions
            top_students = df_lb.groupby(['student_name', 'token', 'school_type']).agg({
                'score': 'mean', 
                'module': 'count'
            }).rename(columns={'score': 'Average Score', 'module': 'Tests Completed'})
            top_5 = top_students.sort_values(by='Average Score', ascending=False).head(5)
            
            for i, (idx, row) in enumerate(top_5.iterrows()):
                symbol = "🥇" if i == 0 else ("🥈" if i == 1 else ("🥉" if i == 2 else f"{i+1}."))
                st.markdown(f"#### {symbol} {idx[0]} (`{idx[1]}`)")
                st.caption(f"Division: {idx[2]}")
                st.progress(row['Average Score']/10.0 if row['Average Score'] <= 10 else 1.0)
                st.info(f"Avg Score: {row['Average Score']:.2f}/10 | Tests: {int(row['Tests Completed'])}")
        else:
            st.info("No assessment data available for this selection.")

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
