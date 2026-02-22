import streamlit as st
from utils.database import init_db, validate_token, request_token
from modules.math_module import render_math_module
from modules.aptitude_module import render_aptitude_module
from modules.typing_module import render_typing_module
from modules.listening_module import render_listening_module
from modules.writing_module import render_writing_module
from modules.speaking_module import render_speaking_module
from modules.parent_module import render_parent_corner
from admin.admin_panel import render_admin_panel
from utils.telegram_bot import send_telegram_alert
import os
import json
from datetime import datetime
import time
from dotenv import load_dotenv

# Load Local Environment Variables
load_dotenv()

# --- EMBEDDED DATA (to prevent FileNotFoundError on deployment) ---
LANGS = {
    "ui": {
        "school_name": "Koilankulam Primary School / கோலியன்குளம் தொடக்கப்பள்ளி",
        "celebration": "100th Year Celebration / 100வது ஆண்டு விழா",
        "welcome": "Welcome to Primary Learn Hub / கற்றல் மையத்திற்கு வரவேற்பிறோம்",
        "enter_token": "Enter Student Token / டோக்கனை உள்ளிடவும்",
        "login_btn": "Login / உள்நுழைய 🚀",
        "signup_btn": "Request New Access / புதிய அனுமதியைக் கோரவும் 📝",
        "invalid_token": "Invalid or Pending Token / தவறான அல்லது நிலுவையில் உள்ள டோக்கன்",
        "hello": "Hello / வணக்கம்",
        "grade": "Grade / வகுப்பு",
        "choose": "Explore / ஆராயுங்கள்",
        "math": "Math / கணிதம் 🔢",
        "aptitude": "Aptitude / மூளை திறன் 🧩",
        "typing": "Typing / தட்டச்சு ⌨️",
        "listening": "Listening / கேட்டல் 🎧",
        "writing": "Writing / எழுதுதல் ✍️",
        "speaking": "Speaking / பேசுதல் 🎤",
        "parent": "Parent Corner / பெற்றோர் பகுதி",
        "logout": "Logout / வெளியேறு",
        "back": "Dashboard / முகப்பு"
    }
}
MATH_POOL = {
    "addition": [{"n1": 5, "n2": 3, "ans": 8}, {"n1": 10, "n2": 5, "ans": 15}],
    "subtraction": [{"n1": 10, "n2": 4, "ans": 6}, {"n1": 15, "n2": 7, "ans": 8}]
}
B_LANG = LANGS['ui']

# Page Config
st.set_page_config(
    page_title="Primary Learn Hub - Koilyankulam",
    page_icon="🎓",
    layout="wide"
)

# Initialize Database
init_db()

# --- PREMIUM CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Clean Light Background */
    .stApp {
        background: #f8f9fa;
    }

    /* Global Text Visibility - Main Content Only */
    .main .stMarkdown p, 
    .main .stMarkdown li, 
    .main .stMarkdown span,
    .main h1, .main h2, .main h3, .main h4,
    .main .stSubheader, .main label p {
        color: #2c3e50 !important;
    }

    /* Fixed Sidebar Visibility */
    [data-testid="stSidebar"] {
        background-color: #34495e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton>button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }

    /* Login Box - Clean & Professional */
    .login-box {
        background: white;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f1f3f5 !important;
        border-radius: 10px 10px 0 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #6c757d !important;
        font-weight: bold !important;
    }

    .stTabs [aria-selected="true"] {
        color: #34495e !important;
        border-bottom: 3px solid #34495e !important;
    }

    /* Primary Action Buttons - BRUTE FORCE CONTRAST */
    .stButton > button {
        background: #34495e !important;
        border-radius: 12px !important;
        height: 54px !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
    }

    /* Target every possible text element inside the button */
    .stButton > button label,
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    .stButton > button * {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    .stButton > button:hover {
        background: #2c3e50 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.3) !important;
    }
    
    /* Input Field Clarity */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
        color: #2c3e50 !important;
        border: 1px solid #ced4da !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# --- MAIN UI ---
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.title(f"{B_LANG['school_name']}")
        st.subheader(f"{B_LANG['celebration']}")
        st.divider()
        
        tab1, tab2 = st.tabs([B_LANG['login_btn'], B_LANG['signup_btn']])
        
        with tab1:
            with st.form("login_form", clear_on_submit=False):
                token_input = st.text_input(B_LANG['enter_token'], placeholder="e.g. STUD001")
                submit_btn = st.form_submit_button(B_LANG['login_btn'], use_container_width=True)
                
                if submit_btn:
                    clean_token = token_input.strip().upper()
                    if clean_token:
                        user = validate_token(clean_token)
                        if user:
                            # user now returns (name, grade, status, school_type)
                            name, grade, status, school_type = user
                            if status in ['active', 'admin']:
                                st.session_state.authenticated = True
                                st.session_state.user_data = {
                                    'name': name, 
                                    'grade': grade, 
                                    'status': status, 
                                    'token': clean_token,
                                    'school_type': school_type
                                }
                                st.success(f"Logging in as {name}...")
                                time.sleep(0.5)
                                st.rerun()
                            elif status == 'pending':
                                st.warning("⏳ Your token is PENDING approval. Please ask your teacher to approve it! / உங்கள் டோக்கன் அனுமதிக்காக காத்திருக்கிறது. தயவுசெய்து உங்கள் ஆசிரியரிடம் கேளுங்கள்!")
                        else:
                            st.error(f"{B_LANG['invalid_token']} - Check ID: {clean_token}")
                    else:
                        st.warning("Please enter your token! / டோக்கனை உள்ளிடவும்!")
                    
        with tab2:
            st.subheader("Register New Student")
            
            # Division Selection - Guaranteed Separation Logic
            sch_col, gr_col = st.columns(2)
            with sch_col:
                sch_type = st.radio("School Division", ["Primary", "High School"], horizontal=True, key="sch_type_radio")
            with gr_col:
                # Use separate components to prevent grade overlap
                if sch_type == "Primary":
                    new_grade = st.selectbox("Grade / வகுப்பு (Primary)", [1, 2, 3, 4, 5], key="primary_grade_select")
                else:
                    new_grade = st.selectbox("Grade / வகுப்பு (High School)", [6, 7, 8, 9, 10], key="hs_grade_select")
            
            # Registration Details Form
            with st.form("registration_details_form", clear_on_submit=True):
                new_name = st.text_input("Student Full Name / மாணவர் பெயர்")
                new_parent = st.text_input("Parent's Name / பெற்றோர் பெயர்")
                new_year = st.text_input("Academic Year / கல்வி ஆண்டு (e.g., 2024-25)")
                
                submit_req = st.form_submit_button("Send Request / கோரிக்கையை அனுப்பு", use_container_width=True)
                
                if submit_req:
                    if new_name.strip() and new_parent.strip():
                        req_tk = request_token(new_name.strip(), new_grade, new_parent.strip(), new_year.strip(), sch_type)
                        st.success(f"✅ **Registration Complete!** Your ID: **{req_tk}**")
                        st.info(f"📢 **Next Steps:** Tell your teacher your ID (**{req_tk}**).")
                        
                        # Telegram Alert
                        msg = f"🏫 *New Student Access Request*\n\n*Student:* {new_name}\n*Parent:* {new_parent}\n*Grade:* {new_grade}\n*Division:* {sch_type}\n*Year:* {new_year}\n*Token:* `{req_tk}`\n\n_Please approve in the Admin Panel._"
                        send_telegram_alert(msg)
                    else:
                        st.warning("Please enter both Student and Parent names! / மாணவர் மற்றும் பெற்றோர் பெயர்களை உள்ளிடவும்!")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"### {B_LANG['hello']}, {st.session_state.user_data['name']}!")
        st.caption(f"📍 {st.session_state.user_data['school_type']} Section")
        st.divider()
        if st.button(f"🏠 {B_LANG['back']}", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
        if st.button(f"🚪 {B_LANG['logout']}", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = None
            st.rerun()

    # Routing
    if st.session_state.user_data['status'] == 'admin':
        render_admin_panel()
    elif st.session_state.page == 'dashboard':
        # Live Time & Header Section
        now = datetime.now().strftime("%I:%M:%S %p | %d %b %Y")
        st.markdown(f"""
        <div style='background: #34495e; color: white; padding: 10px 30px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 1.2rem; font-weight: bold;'>{B_LANG['school_name']}</span>
            <span style='font-size: 1rem;'>🕒 {now}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='title-area'>
            <div class='welcome-text'>{B_LANG['celebration']}</div>
            <h2 style='margin-top:20px; color:#333;'>{B_LANG['choose']}</h2>
        </div>
        """, unsafe_allow_html=True)
        # Dashboard Routing based on School Type
        is_hs = st.session_state.user_data['school_type'] == "High School"
        sch_title = "High School Hub" if is_hs else "Primary Learn Hub"
        st.markdown(f"<h2 style='text-align: center; color: #34495e;'>{sch_title}</h2>", unsafe_allow_html=True)
        
        # Primary Dashboard (Grades 1-5)
        if not is_hs:
            m1, m2, m3 = st.columns(3)
            with m1:
                if st.button(B_LANG['math']): st.session_state.page = 'math'; st.rerun()
            with m2:
                if st.button(B_LANG['aptitude']): st.session_state.page = 'aptitude'; st.rerun()
            with m3:
                if st.button(B_LANG['typing']): st.session_state.page = 'typing'; st.rerun()
            
            m4, m5, m6 = st.columns(3)
            with m4:
                if st.button(B_LANG['listening']): st.session_state.page = 'listening'; st.rerun()
            with m5:
                if st.button(B_LANG['writing']): st.session_state.page = 'writing'; st.rerun()
            with m6:
                if st.button(B_LANG['speaking']): st.session_state.page = 'speaking'; st.rerun()
        
        # High School Dashboard (Grades 6-10)
        else:
            h1, h2, h3 = st.columns(3)
            with h1:
                if st.button("Tamil / தமிழ் 📕"): st.session_state.page = 'hs_tamil'; st.rerun()
            with h2:
                if st.button("English / ஆங்கிலம் 📘"): st.session_state.page = 'hs_english'; st.rerun()
            with h3:
                if st.button("Mathematics / கணிதம் 🔢"): st.session_state.page = 'hs_math'; st.rerun()
            
            h4, h5, h6 = st.columns(3)
            with h4:
                if st.button("Science / அறிவியல் 🔬"): st.session_state.page = 'hs_science'; st.rerun()
            with h5:
                if st.button("Social Science / சமூகம் 🌍"): st.session_state.page = 'hs_social'; st.rerun()
            with h6:
                if st.button("Computer & Excel / கணினி 💻"): st.session_state.page = 'hs_computer'; st.rerun()

        st.divider()
        if st.button(B_LANG['parent'], use_container_width=True, type="primary"):
            st.session_state.page = 'parent'; st.rerun()
            
    # Module rendering
    elif st.session_state.page == 'math': render_math_module('Combined', st.session_state.user_data['token'])
    elif st.session_state.page == 'aptitude': render_aptitude_module('Combined', st.session_state.user_data['token'])
    elif st.session_state.page == 'typing': render_typing_module('Combined', st.session_state.user_data['token'])
    elif st.session_state.page == 'listening': render_listening_module('Combined', st.session_state.user_data['token'])
    elif st.session_state.page == 'writing': render_writing_module('Combined', st.session_state.user_data['token'])
    elif st.session_state.page == 'speaking': render_speaking_module('Combined', st.session_state.user_data['token'])
    elif st.session_state.page == 'parent': render_parent_corner(st.session_state.user_data['token'])
    
    # High School Modules
    from modules.high_school.tamil_module import render_hs_tamil_module
    from modules.high_school.english_module import render_hs_english_module
    from modules.high_school.math_module import render_hs_math_module
    from modules.high_school.science_module import render_hs_science_module
    from modules.high_school.social_module import render_hs_social_module
    from modules.high_school.computer_module import render_hs_computer_module

    if st.session_state.page == 'hs_tamil': render_hs_tamil_module(st.session_state.user_data['token'], st.session_state.user_data['grade'])
    elif st.session_state.page == 'hs_english': render_hs_english_module(st.session_state.user_data['token'], st.session_state.user_data['grade'])
    elif st.session_state.page == 'hs_math': render_hs_math_module(st.session_state.user_data['token'], st.session_state.user_data['grade'])
    elif st.session_state.page == 'hs_science': render_hs_science_module(st.session_state.user_data['token'], st.session_state.user_data['grade'])
    elif st.session_state.page == 'hs_social': render_hs_social_module(st.session_state.user_data['token'], st.session_state.user_data['grade'])
    elif st.session_state.page == 'hs_computer': render_hs_computer_module(st.session_state.user_data['token'], st.session_state.user_data['grade'])
