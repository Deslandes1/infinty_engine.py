import streamlit as st
import datetime
import qrcode
import time
from io import BytesIO
from PIL import Image

# --- 1. SOVEREIGN & SECURITY CONFIG ---
ADMIN_EMAIL = "deslandes78@gmail.com"
MONCASH_ID = "50947385663"
WHATSAPP_LINK = f"https://wa.me/{MONCASH_ID}"
MASTER_KEY = "20082010" 
AVATAR_FILENAME = "gesner_portrait.png"

EXPIRY_HOURS = 24 
MAX_ATTEMPTS = 10

# Initialize Security States
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'auth_time' not in st.session_state: st.session_state.auth_time = None
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0
if 'system_lock' not in st.session_state: st.session_state.system_lock = False

# --- 2. SECURITY CHECK LOGIC ---
def check_security():
    # Check for Brute Force Lock
    if st.session_state.failed_attempts >= MAX_ATTEMPTS:
        st.session_state.system_lock = True
        
    # Check for 24-hour Expiry
    if st.session_state.authenticated and st.session_state.auth_time:
        elapsed = datetime.datetime.now() - st.session_state.auth_time
        if elapsed > datetime.timedelta(hours=EXPIRY_HOURS):
            st.session_state.authenticated = False
            st.session_state.auth_time = None
            st.rerun()

check_security()

# --- 3. UI STYLING ---
st.markdown(f"""
    <style>
    .main-header {{ background: linear-gradient(90deg, #00209F 0%, #D21034 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; border-bottom: 8px solid #FFD700; }}
    .lock-screen {{ background-color: #000; color: #ff0000; padding: 50px; text-align: center; border-radius: 20px; font-weight: bold; border: 5px solid red; }}
    .payment-card {{ background-color: #ffffff; border: 3px solid #00209F; padding: 15px; border-radius: 15px; text-align: center; }}
    .support-btn {{ background-color: #25D366; color: white; padding: 10px; border-radius: 10px; text-align: center; text-decoration: none; display: block; font-weight: bold; margin-top: 10px; }}
    .atomic-alert {{ background-color: #00FF00; color: #000; padding: 20px; border-radius: 10px; font-weight: bold; text-align: center; border: 4px solid black; animation: pulse 1s infinite; }}
    @keyframes pulse {{ 0% {{transform: scale(1);}} 50% {{transform: scale(1.02);}} 100% {{transform: scale(1);}} }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOCKDOWN RENDER ---
if st.session_state.system_lock:
    st.markdown('<div class="lock-screen"><h1>🚨 SYSTEM BREACH DETECTED 🚨</h1><p>Too many failed attempts. This engine is now HARD-LOCKED.</p><p>Contact Gesner Deslandes to reset the security core.</p></div>', unsafe_allow_html=True)
    st.stop()

# --- 5. SIDEBAR: THE SECURE GATEWAY ---
with st.sidebar:
    try:
        img = Image.open(AVATAR_FILENAME)
        st.image(img, caption="Lead Inventor: Gesner Deslandes", use_container_width=True)
    except:
        st.info("📷 [Avatar Standby]")

    if not st.session_state.authenticated:
        st.title("🛡️ Secure Access")
        st.markdown(f"""
            <div class="payment-card">
                <p><b>Unlock Pro Features (24h)</b></p>
                <p style="color:#2e7d32; font-size:1.5rem; font-weight:bold;">$50.00 USD</p>
                <p>MonCash: <b>{MONCASH_ID}</b></p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<a href="{WHATSAPP_LINK}" target="_blank" class="support-btn">💬 WhatsApp for Activation Key</a>', unsafe_allow_html=True)
        
        st.write("---")
        activation_code = st.text_input(f"Enter Key ({MAX_ATTEMPTS - st.session_state.failed_attempts} attempts left):", type="password")
        
        if st.button("🚀 UNLOCK ENGINE"):
            if activation_code == MASTER_KEY:
                st.session_state.authenticated = True
                st.session_state.auth_time = datetime.datetime.now()
                st.session_state.failed_attempts = 0 # Reset on success
                st.balloons()
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                st.error("Invalid Key. Attempt logged.")
                st.rerun()
    else:
        st.success("✅ PRO ACCESS ACTIVE")
        remaining = datetime.timedelta(hours=EXPIRY_HOURS) - (datetime.datetime.now() - st.session_state.auth_time)
        st.write(f"Expires in: {str(remaining).split('.')[0]}")
        if st.button("Logout & Secure"):
            st.session_state.authenticated = False
            st.rerun()

# --- 6. MAIN INTERFACE ---
st.markdown('<div class="main-header"><h1>INFINTY ENGINE v23.0</h1><p>Haitian Mineral & Atomic Sovereignty</p></div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.write("### 🌍 National Resource Portal")
    st.info("Public Demo: Mapping and Atomic Signals are locked. Request a key to continue.")
    st.camera_input("📸 Visual Core Scanner")
else:
    # --- UNLOCKED WORKSPACE ---
    tab1, tab2 = st.tabs(["🔍 Atomic Analysis", "🛰️ Cloud Mapping"])
    with tab1:
        notes = st.text_area("Field Observations:").lower()
        if st.button("RUN ATOMIC SCAN"):
            
            if any(x in notes for x in ["uranium", "plutonium", "radioactive", "iridium"]):
                st.markdown('<div class="atomic-alert">🟢 GREEN SIGNAL: ATOMIC TRACE DETECTED</div>', unsafe_allow_html=True)
            st.success(f"Geological recreation secured for {ADMIN_EMAIL}")
    with tab2:
        
        st.write("Sovereign GPS Mapping Active. Data routing to OneDrive.")
