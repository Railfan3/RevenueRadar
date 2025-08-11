import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import hashlib
import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import time

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

USERS_FILE = "users.json"
OTP_FILE = "otp_data.json"

# Email configuration - Set these in your environment or here
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",  # For Gmail
    "smtp_port": 587,
    "email": os.getenv("SENDER_EMAIL", "your-email@gmail.com"),  # Your email
    "password": os.getenv("EMAIL_PASSWORD", "your-app-password"),  # App password for Gmail
    "sender_name": "Sales Dashboard"
}

# -----------------------
# Compatibility function for older Streamlit versions
# -----------------------
def trigger_rerun():
    """Compatible rerun function for older Streamlit versions"""
    try:
        if hasattr(st, 'rerun'):
            st.rerun()
        elif hasattr(st, 'experimental_rerun'):
            st.experimental_rerun()
        else:
            st.markdown('<meta http-equiv="refresh" content="0">', unsafe_allow_html=True)
    except:
        st.markdown("""
            <script>
                setTimeout(function() {
                    window.location.reload();
                }, 100);
            </script>
        """, unsafe_allow_html=True)

# -----------------------
# EMAIL FUNCTIONS
# -----------------------
def send_otp_email(recipient_email, otp, purpose):
    """Send OTP via email"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['email']}>"
        msg['To'] = recipient_email
        
        if purpose == "registration":
            msg['Subject'] = "Email Verification - Sales Dashboard"
            body = f"""
            <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8fafc; border-radius: 10px;">
                    <h2 style="color: #667eea; text-align: center;">Welcome to Sales Dashboard!</h2>
                    <p style="color: #374151; font-size: 16px;">Thank you for registering with us. Please verify your email address to complete your registration.</p>
                    
                    <div style="background-color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0; border: 2px solid #667eea;">
                        <h3 style="color: #1f2937; margin-bottom: 10px;">Your Verification Code</h3>
                        <div style="font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; font-family: monospace;">
                            {otp}
                        </div>
                        <p style="color: #6b7280; margin-top: 15px; font-size: 14px;">This code will expire in 10 minutes</p>
                    </div>
                    
                    <p style="color: #374151; font-size: 14px;">If you didn't request this verification, please ignore this email.</p>
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                    <p style="color: #6b7280; font-size: 12px; text-align: center;">© 2024 Sales Dashboard. All rights reserved.</p>
                </div>
            </body>
            </html>
            """
        else:  # login
            msg['Subject'] = "Login Verification - Sales Dashboard"
            body = f"""
            <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8fafc; border-radius: 10px;">
                    <h2 style="color: #667eea; text-align: center;">Login Verification</h2>
                    <p style="color: #374151; font-size: 16px;">Someone is trying to log in to your Sales Dashboard account. If this was you, please use the verification code below:</p>
                    
                    <div style="background-color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0; border: 2px solid #667eea;">
                        <h3 style="color: #1f2937; margin-bottom: 10px;">Your Login Code</h3>
                        <div style="font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; font-family: monospace;">
                            {otp}
                        </div>
                        <p style="color: #6b7280; margin-top: 15px; font-size: 14px;">This code will expire in 5 minutes</p>
                    </div>
                    
                    <p style="color: #dc2626; font-size: 14px;"><strong>Security Notice:</strong> If you didn't request this login, please secure your account immediately.</p>
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                    <p style="color: #6b7280; font-size: 12px; text-align: center;">© 2024 Sales Dashboard. All rights reserved.</p>
                </div>
            </body>
            </html>
            """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['email'], recipient_email, text)
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

# -----------------------
# CSS for Professional Dark/Light Theme with Better Contrast
# -----------------------
def apply_theme(mode):
    if mode == "Dark":
        st.markdown(
            """
            <style>
                /* Import Google Fonts */
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
                
                /* Main app background */
                .stApp {
                    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                    color: #f1f5f9 !important;
                    font-family: 'Inter', sans-serif;
                }
                
                /* Sidebar styling */
                .css-1d391kg, .css-1lcbmhc, .css-17eq0hr, section[data-testid="stSidebar"] {
                    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
                }
                
                .css-1d391kg .css-1aumxhk, section[data-testid="stSidebar"] .css-1aumxhk {
                    color: #f1f5f9 !important;
                }
                
                /* Main content area */
                .css-1v3fvcr, .main .block-container {
                    background-color: transparent !important;
                    padding-top: 2rem !important;
                }
                
                /* Text styling with high contrast */
                .css-1aumxhk, h1, h2, h3, h4, h5, h6 {
                    color: #f1f5f9 !important;
                    font-weight: 600 !important;
                }
                
                p, div, span, label, .stMarkdown {
                    color: #e2e8f0 !important;
                }
                
                /* Specific text elements */
                .stTextInput label, .stSelectbox label, .stMultiSelect label, .stRadio label {
                    color: #f1f5f9 !important;
                    font-weight: 500 !important;
                }
                
                .stTextInput div[data-baseweb="input"] input {
                    color: #f1f5f9 !important;
                }
                
                /* Button styling */
                .stButton > button {
                    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
                    color: #ffffff !important;
                    border: none !important;
                    border-radius: 8px !important;
                    padding: 0.75rem 1.5rem !important;
                    font-weight: 600 !important;
                    font-family: 'Inter', sans-serif !important;
                    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
                    transition: all 0.3s ease !important;
                }
                
                .stButton > button:hover {
                    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6) !important;
                }
                
                .stButton > button:focus {
                    outline: 2px solid #60a5fa !important;
                    outline-offset: 2px !important;
                }
                
                /* Form submit button */
                .stForm .stButton > button {
                    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
                    box-shadow: 0 4px 15px rgba(5, 150, 105, 0.4) !important;
                }
                
                .stForm .stButton > button:hover {
                    background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
                    box-shadow: 0 6px 20px rgba(5, 150, 105, 0.6) !important;
                }
                
                /* Input field styling */
                .stTextInput > div > div > input, 
                .stTextInput > div > div > textarea,
                .stSelectbox > div > div,
                .stMultiSelect > div > div,
                .stRadio > div {
                    background-color: #1e293b !important;
                    color: #f1f5f9 !important;
                    border: 2px solid #334155 !important;
                    border-radius: 8px !important;
                }
                
                .stTextInput > div > div > input:focus,
                .stSelectbox > div > div:focus-within {
                    border-color: #3b82f6 !important;
                    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
                }
                
                /* Radio button styling */
                .stRadio > div > label > div:first-child {
                    background-color: #1e293b !important;
                    border: 2px solid #334155 !important;
                }
                
                /* Metric containers */
                .metric-card {
                    background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
                    border: 1px solid #475569 !important;
                    border-radius: 12px !important;
                    padding: 1.5rem !important;
                    margin: 0.5rem 0 !important;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
                    backdrop-filter: blur(10px) !important;
                }
                
                .metric-card h4 {
                    color: #60a5fa !important;
                    margin-bottom: 10px !important;
                    font-weight: 600 !important;
                }
                
                .metric-card h2 {
                    color: #f1f5f9 !important;
                    margin: 0 !important;
                    font-weight: 700 !important;
                }
                
                .metric-card p {
                    color: #cbd5e1 !important;
                    margin: 5px 0 0 0 !important;
                    font-size: 14px !important;
                }
                
                /* Success/Error/Info messages */
                .stSuccess {
                    background-color: rgba(34, 197, 94, 0.15) !important;
                    border: 1px solid rgba(34, 197, 94, 0.5) !important;
                    color: #22c55e !important;
                    border-radius: 8px !important;
                }
                
                .stError {
                    background-color: rgba(239, 68, 68, 0.15) !important;
                    border: 1px solid rgba(239, 68, 68, 0.5) !important;
                    color: #ef4444 !important;
                    border-radius: 8px !important;
                }
                
                .stInfo {
                    background-color: rgba(59, 130, 246, 0.15) !important;
                    border: 1px solid rgba(59, 130, 246, 0.5) !important;
                    color: #60a5fa !important;
                    border-radius: 8px !important;
                }
                
                .stWarning {
                    background-color: rgba(245, 158, 11, 0.15) !important;
                    border: 1px solid rgba(245, 158, 11, 0.5) !important;
                    color: #f59e0b !important;
                    border-radius: 8px !important;
                }
                
                /* DataFrame styling */
                .dataframe {
                    background-color: #1e293b !important;
                    color: #f1f5f9 !important;
                }
                
                /* Plotly charts */
                .js-plotly-plot {
                    background: rgba(30, 41, 59, 0.6) !important;
                    border-radius: 12px !important;
                }
                
                /* Custom styles */
                .title-container {
                    text-align: center;
                    padding: 2rem 0;
                    margin-bottom: 2rem;
                }
                
                .title-container h1 {
                    color: #f1f5f9 !important;
                    font-size: 3rem !important;
                    font-weight: 700 !important;
                    margin-bottom: 0.5rem !important;
                    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                }
                
                .divider {
                    height: 2px;
                    background: linear-gradient(90deg, transparent, #3b82f6, transparent);
                    margin: 2rem 0;
                    border-radius: 1px;
                }
            </style>
            """, unsafe_allow_html=True)
    else:  # Light mode
        st.markdown(
            """
            <style>
                /* Import Google Fonts */
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
                
                /* Main app background */
                .stApp {
                    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                    color: #0f172a !important;
                    font-family: 'Inter', sans-serif;
                }
                
                /* Sidebar styling */
                .css-1d391kg, .css-1lcbmhc, .css-17eq0hr, section[data-testid="stSidebar"] {
                    background: rgba(255, 255, 255, 0.95) !important;
                    backdrop-filter: blur(10px) !important;
                    border-right: 1px solid #e2e8f0 !important;
                }
                
                .css-1d391kg .css-1aumxhk, section[data-testid="stSidebar"] .css-1aumxhk {
                    color: #0f172a !important;
                }
                
                /* Main content area */
                .css-1v3fvcr, .main .block-container {
                    background: rgba(255, 255, 255, 0.8) !important;
                    backdrop-filter: blur(10px) !important;
                    border-radius: 20px !important;
                    margin: 1rem !important;
                    padding: 2rem !important;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
                }
                
                /* Text styling with high contrast */
                .css-1aumxhk, h1, h2, h3, h4, h5, h6 {
                    color: #0f172a !important;
                    font-weight: 600 !important;
                }
                
                p, div, span, label, .stMarkdown {
                    color: #334155 !important;
                }
                
                /* Specific text elements */
                .stTextInput label, .stSelectbox label, .stMultiSelect label, .stRadio label {
                    color: #0f172a !important;
                    font-weight: 500 !important;
                }
                
                .stTextInput div[data-baseweb="input"] input {
                    color: #0f172a !important;
                }
                
                /* Button styling */
                .stButton > button {
                    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
                    color: #ffffff !important;
                    border: none !important;
                    border-radius: 8px !important;
                    padding: 0.75rem 1.5rem !important;
                    font-weight: 600 !important;
                    font-family: 'Inter', sans-serif !important;
                    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
                    transition: all 0.3s ease !important;
                }
                
                .stButton > button:hover {
                    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
                    transform: translateY(-2px) !important;
                    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
                }
                
                .stButton > button:focus {
                    outline: 2px solid #3b82f6 !important;
                    outline-offset: 2px !important;
                }
                
                /* Form submit button */
                .stForm .stButton > button {
                    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
                    box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3) !important;
                }
                
                .stForm .stButton > button:hover {
                    background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
                    box-shadow: 0 8px 25px rgba(5, 150, 105, 0.4) !important;
                }
                
                /* Input field styling */
                .stTextInput > div > div > input, 
                .stTextInput > div > div > textarea,
                .stSelectbox > div > div,
                .stMultiSelect > div > div,
                .stRadio > div {
                    background-color: #ffffff !important;
                    color: #0f172a !important;
                    border: 2px solid #e2e8f0 !important;
                    border-radius: 8px !important;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
                }
                
                .stTextInput > div > div > input:focus,
                .stSelectbox > div > div:focus-within {
                    border-color: #3b82f6 !important;
                    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
                }
                
                /* Radio button styling */
                .stRadio > div > label > div:first-child {
                    background-color: #ffffff !important;
                    border: 2px solid #e2e8f0 !important;
                }
                
                /* Metric containers */
                .metric-card {
                    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
                    border: 1px solid #e2e8f0 !important;
                    border-radius: 12px !important;
                    padding: 1.5rem !important;
                    margin: 0.5rem 0 !important;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
                }
                
                .metric-card h4 {
                    color: #3b82f6 !important;
                    margin-bottom: 10px !important;
                    font-weight: 600 !important;
                }
                
                .metric-card h2 {
                    color: #0f172a !important;
                    margin: 0 !important;
                    font-weight: 700 !important;
                }
                
                .metric-card p {
                    color: #64748b !important;
                    margin: 5px 0 0 0 !important;
                    font-size: 14px !important;
                }
                
                /* Success/Error/Info messages */
                .stSuccess {
                    background-color: rgba(34, 197, 94, 0.1) !important;
                    border: 1px solid rgba(34, 197, 94, 0.3) !important;
                    color: #047857 !important;
                    border-radius: 8px !important;
                }
                
                .stError {
                    background-color: rgba(239, 68, 68, 0.1) !important;
                    border: 1px solid rgba(239, 68, 68, 0.3) !important;
                    color: #dc2626 !important;
                    border-radius: 8px !important;
                }
                
                .stInfo {
                    background-color: rgba(59, 130, 246, 0.1) !important;
                    border: 1px solid rgba(59, 130, 246, 0.3) !important;
                    color: #1d4ed8 !important;
                    border-radius: 8px !important;
                }
                
                .stWarning {
                    background-color: rgba(245, 158, 11, 0.1) !important;
                    border: 1px solid rgba(245, 158, 11, 0.3) !important;
                    color: #d97706 !important;
                    border-radius: 8px !important;
                }
                
                /* DataFrame styling */
                .dataframe {
                    background-color: #ffffff !important;
                    color: #0f172a !important;
                }
                
                /* Plotly charts */
                .js-plotly-plot {
                    background: rgba(255, 255, 255, 0.8) !important;
                    border-radius: 12px !important;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
                }
                
                /* Custom styles */
                .title-container {
                    text-align: center;
                    padding: 2rem 0;
                    margin-bottom: 2rem;
                }
                
                .title-container h1 {
                    color: #0f172a !important;
                    font-size: 3rem !important;
                    font-weight: 700 !important;
                    margin-bottom: 0.5rem !important;
                    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }
                
                .divider {
                    height: 2px;
                    background: linear-gradient(90deg, transparent, #3b82f6, transparent);
                    margin: 2rem 0;
                    border-radius: 1px;
                }
            </style>
            """, unsafe_allow_html=True)

# -----------------------
# OTP FUNCTIONS (Enhanced with Email)
# -----------------------
def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def save_otp_data(identifier, otp, purpose, expiry_minutes=10):
    """Save OTP data to file"""
    otp_data = load_otp_data()
    otp_data[identifier] = {
        "otp": otp,
        "purpose": purpose,
        "expires_at": (datetime.now() + timedelta(minutes=expiry_minutes)).isoformat(),
        "attempts": 0,
        "created_at": datetime.now().isoformat()
    }
    
    with open(OTP_FILE, "w") as f:
        json.dump(otp_data, f, indent=4)

def load_otp_data():
    """Load OTP data from file"""
    if os.path.exists(OTP_FILE):
        try:
            with open(OTP_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def verify_otp(identifier, otp_input, purpose):
    """Verify OTP"""
    otp_data = load_otp_data()
    
    if identifier not in otp_data:
        return False, "No OTP found. Please request a new one."
    
    data = otp_data[identifier]
    
    # Check if expired
    try:
        expires_at = datetime.fromisoformat(data["expires_at"])
        if datetime.now() > expires_at:
            del otp_data[identifier]
            with open(OTP_FILE, "w") as f:
                json.dump(otp_data, f, indent=4)
            return False, "OTP has expired. Please request a new one."
    except:
        return False, "Invalid OTP data. Please request a new OTP."
    
    # Check attempts
    if data.get("attempts", 0) >= 3:
        del otp_data[identifier]
        with open(OTP_FILE, "w") as f:
            json.dump(otp_data, f, indent=4)
        return False, "Too many failed attempts. Please request a new OTP."
    
    # Check purpose match
    if data.get("purpose") != purpose:
        return False, "Invalid OTP for this operation."
    
    # Verify OTP
    if data["otp"] == otp_input:
        del otp_data[identifier]
        with open(OTP_FILE, "w") as f:
            json.dump(otp_data, f, indent=4)
        return True, "OTP verified successfully"
    else:
        data["attempts"] = data.get("attempts", 0) + 1
        otp_data[identifier] = data
        with open(OTP_FILE, "w") as f:
            json.dump(otp_data, f, indent=4)
        
        remaining = 3 - data["attempts"]
        if remaining > 0:
            return False, f"Invalid OTP. {remaining} attempts remaining."
        else:
            del otp_data[identifier]
            with open(OTP_FILE, "w") as f:
                json.dump(otp_data, f, indent=4)
            return False, "Too many failed attempts. Please request a new OTP."

# -----------------------
# USER FUNCTIONS
# -----------------------
def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."
    return True, "Password is valid"

def register_user(username, password, email):
    """Register new user"""
    users = load_users()
    
    if username in users:
        return False, "Username already exists"
    
    for user_data in users.values():
        if user_data.get("email") == email:
            return False, "Email already registered"
    
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "verified": True,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    save_users(users)
    return True, "Registration successful"

def get_user_by_email(email):
    """Get user by email address"""
    users = load_users()
    for username, user_data in users.items():
        if user_data.get("email") == email:
            return username, user_data
    return None, None

def get_user_by_username(username):
    """Get user by username"""
    users = load_users()
    if username in users:
        return username, users[username]
    return None, None

def update_last_login(username):
    """Update user's last login time"""
    users = load_users()
    if username in users:
        users[username]["last_login"] = datetime.now().isoformat()
        save_users(users)

# -----------------------
# Initialize session state variables
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "register"
if "theme" not in st.session_state:
    st.session_state.theme = "Light"
if "login_step" not in st.session_state:
    st.session_state.login_step = "credentials"
if "register_step" not in st.session_state:
    st.session_state.register_step = "details"
if "current_identifier" not in st.session_state:
    st.session_state.current_identifier = ""
if "registration_data" not in st.session_state:
    st.session_state.registration_data = {}

# -----------------------
# AUTH SCREENS
# -----------------------
def show_register():
    st.markdown('<div class="title-container"><h1>📝 Create Your Account</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.register_step == "details":
        st.markdown("### 👤 Account Information")
        
        with st.form("registration_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username", placeholder="Choose a unique username")
                email = st.text_input("Email Address", placeholder="your.email@example.com")
            
            with col2:
                password = st.text_input("Password", type="password", placeholder="Create a strong password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown("#### 🔒 Password Requirements:")
            st.markdown("""
            - At least 8 characters long
            - Contains uppercase and lowercase letters  
            - Contains at least one digit (0-9)
            - Contains at least one special character (!@#$%^&*(),.?\":{}|<>)
            """)
            
            submitted = st.form_submit_button("📧 Verify Email & Create Account", use_container_width=True)
            
            if submitted:
                if not all([username, email, password, confirm_password]):
                    st.error("❌ Please fill in all fields.")
                elif not validate_email(email):
                    st.error("❌ Please enter a valid email address.")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match.")
                else:
                    valid, msg = validate_password(password)
                    if not valid:
                        st.error(f"❌ {msg}")
                    else:
                        users = load_users()
                        if username in users:
                            st.error("❌ Username already exists. Please choose a different one.")
                        elif any(user_data.get("email") == email for user_data in users.values()):
                            st.error("❌ Email already registered. Please use a different email.")
                        else:
                            st.session_state.registration_data = {
                                "username": username,
                                "email": email,
                                "password": password
                            }
                            
                            # Generate OTP and send email
                            otp = generate_otp()
                            save_otp_data(email, otp, "registration", 10)
                            st.session_state.current_identifier = email
                            
                            # Try to send email
                            if EMAIL_CONFIG['email'] != "your-email@gmail.com" and EMAIL_CONFIG['password'] != "your-app-password":
                                email_sent, email_msg = send_otp_email(email, otp, "registration")
                                if email_sent:
                                    st.success("✅ Verification email sent! Please check your inbox.")
                                else:
                                    st.warning(f"⚠️ Email sending failed: {email_msg}")
                                    st.info(f"📱 Demo OTP for testing: **{otp}**")
                            else:
                                st.warning("⚠️ Email not configured. Using demo mode.")
                                st.info(f"📱 Demo OTP for testing: **{otp}**")
                            
                            st.session_state.register_step = "otp_verification"
                            time.sleep(1)
                            trigger_rerun()
    
    elif st.session_state.register_step == "otp_verification":
        st.markdown("### 🔑 Email Verification")
        
        st.info(f"📧 Verify your email: **{st.session_state.current_identifier}**")
        st.markdown("Enter the 6-digit verification code sent to your email:")
        
        with st.form("email_verification_form"):
            otp_input = st.text_input("Verification Code", max_chars=6, placeholder="000000")
            
            col1, col2 = st.columns(2)
            with col1:
                verify_clicked = st.form_submit_button("✅ Complete Registration", use_container_width=True)
            with col2:
                resend_clicked = st.form_submit_button("🔄 Resend OTP", use_container_width=True)
            
            if verify_clicked:
                if not otp_input or len(otp_input) != 6:
                    st.error("❌ Please enter a valid 6-digit verification code.")
                else:
                    success, message = verify_otp(st.session_state.current_identifier, otp_input, "registration")
                    if success:
                        reg_data = st.session_state.registration_data
                        reg_success, reg_message = register_user(
                            reg_data["username"],
                            reg_data["password"],
                            reg_data["email"]
                        )
                        
                        if reg_success:
                            st.session_state.register_step = "details"
                            st.session_state.current_identifier = ""
                            st.session_state.registration_data = {}
                            
                            st.success("🎉 Registration successful! You can now login.")
                            time.sleep(2)
                            st.session_state.page = "login"
                            trigger_rerun()
                        else:
                            st.error(f"❌ Registration failed: {reg_message}")
                    else:
                        st.error(f"❌ {message}")
            
            elif resend_clicked:
                otp = generate_otp()
                save_otp_data(st.session_state.current_identifier, otp, "registration", 10)
                
                if EMAIL_CONFIG['email'] != "your-email@gmail.com" and EMAIL_CONFIG['password'] != "your-app-password":
                    email_sent, email_msg = send_otp_email(st.session_state.current_identifier, otp, "registration")
                    if email_sent:
                        st.success("✅ New verification email sent!")
                    else:
                        st.warning(f"⚠️ Email sending failed: {email_msg}")
                        st.info(f"📱 Demo OTP: **{otp}**")
                else:
                    st.success(f"✅ New verification code: **{otp}**")
        
        if st.button("⬅️ Back to Registration"):
            st.session_state.register_step = "details"
            st.session_state.current_identifier = ""
            st.session_state.registration_data = {}
            trigger_rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🔑 Already have an account?")
    if st.button("Sign In to Your Account", use_container_width=True):
        st.session_state.page = "login"
        st.session_state.login_step = "credentials"
        st.session_state.register_step = "details"
        trigger_rerun()

def show_login():
    st.markdown('<div class="title-container"><h1>🔐 Welcome Back</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.login_step == "credentials":
        st.markdown("### 🔑 Login to Your Account")
        
        with st.form("login_form"):
            login_method = st.radio("Choose login method:", ["Username", "Email"])
            
            if login_method == "Username":
                identifier = st.text_input("Username", placeholder="Enter your username")
            else:
                identifier = st.text_input("Email", placeholder="Enter your email address")
            
            submitted = st.form_submit_button("🚀 Send Login OTP", use_container_width=True)
            
            if submitted:
                if not identifier:
                    st.error(f"❌ Please enter your {login_method.lower()}.")
                else:
                    if login_method == "Email":
                        if not validate_email(identifier):
                            st.error("❌ Please enter a valid email address.")
                            return
                        username, user_data = get_user_by_email(identifier)
                    else:
                        username, user_data = get_user_by_username(identifier)
                    
                    if not username:
                        st.error(f"❌ No account found with this {login_method.lower()}.")
                    else:
                        otp = generate_otp()
                        save_otp_data(identifier, otp, "login", 5)
                        st.session_state.current_identifier = identifier
                        
                        # Send OTP via email
                        email_address = user_data["email"] if login_method == "Username" else identifier
                        
                        if EMAIL_CONFIG['email'] != "your-email@gmail.com" and EMAIL_CONFIG['password'] != "your-app-password":
                            email_sent, email_msg = send_otp_email(email_address, otp, "login")
                            if email_sent:
                                st.success("✅ Login OTP sent to your email!")
                            else:
                                st.warning(f"⚠️ Email sending failed: {email_msg}")
                                st.info(f"📱 Demo OTP: **{otp}**")
                        else:
                            st.warning("⚠️ Email not configured. Using demo mode.")
                            st.info(f"📱 Demo OTP: **{otp}**")
                        
                        st.session_state.login_step = "otp_verification"
                        time.sleep(1)
                        trigger_rerun()
    
    elif st.session_state.login_step == "otp_verification":
        st.markdown("### 🔑 Verify Login OTP")
        
        st.info(f"🔐 Enter the OTP sent to your registered email")
        
        with st.form("otp_verification_form"):
            otp_input = st.text_input("Enter the 6-digit OTP", max_chars=6, placeholder="000000")
            
            col1, col2 = st.columns(2)
            with col1:
                verify_clicked = st.form_submit_button("✅ Verify & Login", use_container_width=True)
            with col2:
                resend_clicked = st.form_submit_button("🔄 Resend OTP", use_container_width=True)
            
            if verify_clicked:
                if not otp_input or len(otp_input) != 6:
                    st.error("❌ Please enter a valid 6-digit OTP.")
                else:
                    success, message = verify_otp(st.session_state.current_identifier, otp_input, "login")
                    if success:
                        if validate_email(st.session_state.current_identifier):
                            username, user_data = get_user_by_email(st.session_state.current_identifier)
                        else:
                            username, user_data = get_user_by_username(st.session_state.current_identifier)
                        
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        update_last_login(username)
                        
                        st.session_state.login_step = "credentials"
                        st.session_state.current_identifier = ""
                        
                        st.success("🎉 Login successful! Redirecting to dashboard...")
                        time.sleep(1)
                        trigger_rerun()
                    else:
                        st.error(f"❌ {message}")
            
            elif resend_clicked:
                # Find user email for resending
                if validate_email(st.session_state.current_identifier):
                    email_address = st.session_state.current_identifier
                else:
                    username, user_data = get_user_by_username(st.session_state.current_identifier)
                    email_address = user_data["email"] if user_data else None
                
                if email_address:
                    otp = generate_otp()
                    save_otp_data(st.session_state.current_identifier, otp, "login", 5)
                    
                    if EMAIL_CONFIG['email'] != "your-email@gmail.com" and EMAIL_CONFIG['password'] != "your-app-password":
                        email_sent, email_msg = send_otp_email(email_address, otp, "login")
                        if email_sent:
                            st.success("✅ New OTP sent to your email!")
                        else:
                            st.warning(f"⚠️ Email sending failed: {email_msg}")
                            st.info(f"📱 Demo OTP: **{otp}**")
                    else:
                        st.success(f"✅ New OTP: **{otp}**")
        
        if st.button("⬅️ Back to Login"):
            st.session_state.login_step = "credentials"
            st.session_state.current_identifier = ""
            trigger_rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🆕 New to Sales Dashboard?")
    if st.button("Create New Account", use_container_width=True):
        st.session_state.page = "register"
        st.session_state.login_step = "credentials"
        st.session_state.register_step = "details"
        trigger_rerun()

# -----------------------
# DASHBOARD FUNCTIONS
# -----------------------
def create_sample_data():
    """Create sample sales data if CSV doesn't exist"""
    if not os.path.exists("salesdata.csv"):
        st.info("Creating sample sales data...")
        
        dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
        regions = ['North', 'South', 'East', 'West', 'Central']
        categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books', 'Beauty', 'Automotive']
        products = [
            'Smartphone Pro', 'Laptop Ultra', 'Wireless Headphones', 'Smart Watch', 'Tablet',
            'Designer Jeans', 'Cotton T-Shirt', 'Winter Jacket', 'Running Shoes', 'Formal Shirt',
            'Garden Tools Set', 'Plant Pots', 'Outdoor Furniture', 'BBQ Grill', 'Lawn Mower',
            'Football', 'Tennis Racket', 'Yoga Mat', 'Dumbbells', 'Bicycle',
            'Programming Book', 'Novel', 'Cookbook', 'Travel Guide', 'Children Book'
        ]
        
        data = []
        for date in dates:
            daily_sales = random.randint(1, 10)
            for _ in range(daily_sales):
                product = random.choice(products)
                category = 'Electronics' if product in products[:5] else \
                          'Clothing' if product in products[5:10] else \
                          'Home & Garden' if product in products[10:15] else \
                          'Sports' if product in products[15:20] else 'Books'
                
                quantity = random.randint(1, 50)
                base_price = random.uniform(50, 2000)
                revenue = round(base_price * quantity, 2)
                
                data.append({
                    'Date': date,
                    'Region': random.choice(regions),
                    'Category': category,
                    'Product': product,
                    'Quantity': quantity,
                    'Revenue': revenue
                })
        
        df = pd.DataFrame(data)
        df.to_csv("salesdata.csv", index=False)
        st.success("✅ Sample data created successfully!")

def show_dashboard():
    apply_theme(st.session_state.theme)
    
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        new_theme = st.selectbox(
            "🎨 Theme:", 
            ["Light", "Dark"], 
            index=0 if st.session_state.theme == "Light" else 1
        )
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            trigger_rerun()
        
        st.markdown("---")
        
        st.markdown("## 👤 User Info")
        st.success(f"**{st.session_state.username}**")
        
        users = load_users()
        user_data = users.get(st.session_state.username, {})
        if user_data.get("last_login"):
            try:
                last_login = datetime.fromisoformat(user_data["last_login"])
                st.info(f"🕐 Last login: {last_login.strftime('%Y-%m-%d %H:%M')}")
            except:
                pass
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.login_step = "credentials"
            st.session_state.current_identifier = ""
            st.session_state.page = "register"
            trigger_rerun()

    create_sample_data()
    
    @st.cache_data
    def load_sales_data():
        try:
            return pd.read_csv("salesdata.csv", parse_dates=["Date"])
        except:
            return pd.read_csv("salesdata.csv", parse_dates=["Date"])

    try:
        df = load_sales_data()
    except:
        try:
            @st.cache
            def load_data_old():
                return pd.read_csv("salesdata.csv", parse_dates=["Date"])
            df = load_data_old()
        except Exception as e:
            st.error(f"❌ Error loading sales data: {e}")
            st.info("Please ensure 'salesdata.csv' exists in the same directory as this script.")
            return

    with st.sidebar:
        st.markdown("## 🔍 Data Filters")
        
        min_date = df["Date"].min().date()
        max_date = df["Date"].max().date()
        
        try:
            date_range = st.date_input(
                "📅 Date Range:",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        except:
            start_date = st.date_input("Start Date:", min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("End Date:", max_date, min_value=min_date, max_value=max_date)
            date_range = (start_date, end_date)
        
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range[0]
        
        region_filter = st.multiselect(
            "🌍 Regions:",
            options=sorted(df["Region"].unique()),
            default=sorted(df["Region"].unique())
        )
        
        category_filter = st.multiselect(
            "📂 Categories:",
            options=sorted(df["Category"].unique()),
            default=sorted(df["Category"].unique())
        )
        
        top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(20).index.tolist()
        product_filter = st.multiselect(
            "🏷️ Products (Top 20):",
            options=top_products,
            default=top_products
        )

    df_filtered = df[
        (df["Region"].isin(region_filter)) &
        (df["Category"].isin(category_filter)) &
        (df["Product"].isin(product_filter)) &
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date)
    ]

    st.markdown('<div class="title-container"><h1>📊 Sales Analytics Dashboard</h1></div>', unsafe_allow_html=True)
    st.markdown(f"## Welcome back, **{st.session_state.username}**! 👋")
    
    if df_filtered.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust your filter criteria.")
        return

    st.markdown("## 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = df_filtered['Revenue'].sum()
    total_quantity = df_filtered['Quantity'].sum()
    avg_order_value = df_filtered['Revenue'].mean()
    total_orders = len(df_filtered)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h4>💰 Total Revenue</h4>
                <h2>₹{total_revenue:,.2f}</h2>
                <p>{((total_revenue / df['Revenue'].sum()) * 100):.1f}% of total</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h4>📦 Total Quantity</h4>
                <h2>{total_quantity:,}</h2>
                <p>Units sold</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <h4>🏷️ Avg Order Value</h4>
                <h2>₹{avg_order_value:,.2f}</h2>
                <p>Per transaction</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <h4>📋 Total Orders</h4>
                <h2>{total_orders:,}</h2>
                <p>Transactions</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("## 📊 Sales Analytics")
    
    st.markdown("### 🏆 Top 10 Products by Revenue")
    top_products_data = df_filtered.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(10).reset_index()
    
    if not top_products_data.empty:
        fig1 = px.bar(
            top_products_data,
            x="Revenue",
            y="Product",
            orientation='h',
            color="Revenue",
            color_continuous_scale="viridis",
            title="Top Performing Products"
        )
        fig1.update_layout(
            height=500,
            xaxis_title="Revenue (₹)",
            yaxis_title="Products",
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Monthly Revenue Trend")
        monthly_data = df_filtered.groupby(df_filtered["Date"].dt.to_period("M"))["Revenue"].sum().reset_index()
        monthly_data["Date"] = monthly_data["Date"].astype(str)
        
        if not monthly_data.empty:
            fig2 = px.line(
                monthly_data,
                x="Date",
                y="Revenue",
                markers=True,
                title="Revenue Over Time"
            )
            fig2.update_traces(line=dict(color='#3b82f6', width=3))
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Revenue by Category")
        category_data = df_filtered.groupby("Category")["Revenue"].sum().reset_index()
        
        if not category_data.empty:
            fig3 = px.pie(
                category_data,
                names="Category",
                values="Revenue",
                title="Revenue Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Revenue by Region")
        region_data = df_filtered.groupby("Region")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=True)
        
        if not region_data.empty:
            fig4 = px.bar(
                region_data,
                x="Revenue",
                y="Region",
                orientation='h',
                color="Revenue",
                color_continuous_scale="plasma",
                title="Regional Performance"
            )
            fig4.update_layout(height=350)
            st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Quantity by Region")
        region_qty_data = df_filtered.groupby("Region")["Quantity"].sum().reset_index()
        
        if not region_qty_data.empty:
            fig5 = px.pie(
                region_qty_data,
                names="Region",
                values="Quantity",
                title="Quantity Distribution",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig5.update_layout(height=350)
            st.plotly_chart(fig5, use_container_width=True)

    st.markdown("### 📈 Sales Performance Analysis")
    
    weekly_data = df_filtered.groupby(df_filtered["Date"].dt.dayofweek)["Revenue"].mean().reset_index()
    weekly_data["Day"] = weekly_data["Date"].map({
        0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
        4: "Friday", 5: "Saturday", 6: "Sunday"
    })
    
    if not weekly_data.empty:
        fig6 = px.bar(
            weekly_data,
            x="Day",
            y="Revenue",
            color="Revenue",
            color_continuous_scale="blues",
            title="Average Revenue by Day of Week"
        )
        fig6.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("## 📄 Detailed Sales Data")
    
    search_term = st.text_input("🔍 Search in data:", placeholder="Search by product, region, category...")
    
    if search_term:
        mask = df_filtered.astype(str).apply(
            lambda x: x.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        display_df = df_filtered[mask]
    else:
        display_df = df_filtered

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Showing Records", f"{len(display_df):,}")
    with col2:
        st.metric("📈 Total Records", f"{len(df_filtered):,}")
    with col3:
        if len(df_filtered) > 0:
            st.metric("📋 Filter Match", f"{(len(display_df)/len(df_filtered)*100):.1f}%")

    if len(display_df) > 100:
        st.info(f"📄 Showing first 100 rows of {len(display_df):,} records. Use search to filter data.")
        display_df = display_df.head(100)
    
    display_df_formatted = display_df.copy()
    display_df_formatted["Revenue"] = display_df_formatted["Revenue"].apply(lambda x: f"₹{x:,.2f}")
    display_df_formatted["Date"] = display_df_formatted["Date"].dt.strftime("%Y-%m-%d")
    
    st.dataframe(
        display_df_formatted,
        use_container_width=True,
        height=400
    )
    
    if st.button("📥 Download Filtered Data as CSV"):
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="💾 Click to Download CSV",
            data=csv,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# -----------------------
# MAIN APPLICATION LOGIC
# -----------------------
def main():
    apply_theme(st.session_state.theme)
    
    if not st.session_state.logged_in:
        if st.session_state.page == "login":
            show_login()
        elif st.session_state.page == "register":
            show_register()
    else:
        show_dashboard()

# -----------------------
# RUN APPLICATION
# -----------------------
if __name__ == "__main__":
    main()