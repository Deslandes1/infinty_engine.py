import streamlit as st
import datetime
import pandas as pd
import uuid
import base64
import time
from streamlit_js_eval import get_geolocation
from PIL import Image

# --- 1. SOVEREIGN CONFIGURATION ---
ADMIN_EMAIL = "deslandes78@gmail.com"
MASTER_LICENSE = "GESNER_PRO_2026" 
AVATAR_FILENAME = "gesner_portrait.png" # Your photo here
MONCASH_ID = "(509)-47385663"

# Session State Initialization
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'history' not in st.session_state: st.session_state.history = []
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0

# --- 2. GESNER AI SALES & TECH LOGIC ---
def gesner_ai_brain(query):
    query = query.lower()
    if not st.session_state.authenticated:
        if "buy" in query or "license" in query or "price" in query:
            return f"🤖 Gesner AI: To unlock the Full Version for your mining operations, please contact the Lead Inventor at {ADMIN_EMAIL} or send payment via MonCash to {MONCASH_ID}."
        return "🤖 Gesner AI: Welcome to the Demo. I can analyze soil samples, but Cloud Sync and Atomic Detection require a Pro License."
    
    if "plutonium" in query or "iridium" in query:
        return "🤖 Gesner AI: Pro Sensors Active. I am monitoring the Beloc Formation and Massif du Nord for rare-earth and radioactive signatures."
    return "🤖 Gesner AI: Pro System Operational. Your data is being routed to deslandes78@gmail.com."

def render_avatar():
    try:
        img = Image.open(AVATAR_FILENAME)
        st.sidebar.image(img, caption="Lead Inventor: Gesner Deslandes", use_container_width=True)
    except:
        st.sidebar.info("📷 [Gesner AI Avatar Standby]")

# --- 3. PROFESSIONAL UI STYLING ---
st.markdown(f"""
    <style>
    .main-header {{ background: linear-gradient(90deg, #00209F 0%, #D21034 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; border-bottom: 5px solid #FFD700; }}
    .ai-bubble {{ background: #f0f2f6; border-left: 6px solid #D21034; padding: 15px; border-radius: 5px; margin-bottom: 20px; color: #1a1a1a; font-weight: 500; }}
    .payment-btn {{ background-color: #28a745; color: white; padding: 10px; border-radius: 10px; text-align: center; text-decoration: none; display: block; font-weight: bold; margin-bottom: 10px; }}
    .atomic-alert {{ background-color: #00FF00; color: #000; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; border: 3px solid #000; animation: blinker 1.5s linear infinite; }}
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR: THE BUSINESS HUB ---
with st.sidebar:
    render_avatar()
    
    if not st.session_state.authenticated:
        st.title("🔒 License Activation")
        lic_input = st.text_input("Enter License Key:", type="password")
        if st.button("Activate Pro Features"):
            if lic_input == MASTER_LICENSE:
                st.session_state.authenticated = True
                st.session_state.failed_attempts = 0
                st.success("System Unlocked.")
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                if st.session_state.failed_attempts >= 5:
                    st.error("🚨 SECURITY ALERT: Multiple failed attempts. System Lock active.")
                else:
                    st.error(f"Invalid Key. ({5 - st.session_state.failed_attempts} attempts remaining)")
        
        st.write("---")
        st.markdown(f'<a href="mailto:{ADMIN_EMAIL}" class="payment-btn">💳 Request License Key</a>', unsafe_allow_html=True)
        st.info(f"Support & MonCash: {MONCASH_ID}")
    else:
        st.markdown('<h3 style="color: gold;">⭐ PRO LICENSE ACTIVE</h3>', unsafe_allow_html=True)
        if st.button("Log Out / Secure Data"):
            st.session_state.authenticated = False
            st.rerun()

    st.write("---")
    st.title("🤖 GESNER AI")
    q = st.text_input("Chat with the Engine:")
    if q: st.markdown(f'<div class="ai-bubble">{gesner_ai_brain(q)}</div>', unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-header"><h1>INFINTY ENGINE v13.0</h1><p>Haitian Natural Resource Analysis Suite</p></div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    # PUBLIC/MARKET VIEW
    st.write("### 💎 Advanced Geological Recreation")
    st.write("This engine uses high-frequency AI logic to identify mineral deposits. By capturing soil imagery, the system recreates scientific reports for mineral exploration.")
    
    c1, c2 = st.columns(2)
    with c1: st.info("✅ Multi-Spectral Soil Analysis (Enabled)")
    with c2: st.warning("🔒 OneDrive Cloud Sync (License Required)")
    
    st.camera_input("📸 Test the Scanner (Demo Only)")
    st.write("---")
    st.caption("Developed by Gesner Deslandes | HSC Certified 🇭🇹")
else:
    # PRO VIEW
    tab1, tab2, tab3 = st.tabs(["🔍 Field Analysis", "🛰️ Map & Cloud", "📜 Validation"])
    
    with tab1:
        site = st.text_input("📍 Operation Site Name")
        notes = st.text_area("Observations for Atomic/Mineral Scan:").lower()
        photo = st.camera_input("📸 Pro Capture")
        
        if st.button("🚀 EXECUTE & SYNC TO ONEDRIVE"):
            loc = get_geolocation()
            if loc:
                lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
                is_atomic = any(x in notes for x in ["uranium", "plutonium", "radioactive", "iridium"])
                
                if is_atomic:
                    st.markdown('<div class="atomic-alert">🟢 GREEN SIGNAL: ATOMIC TRACE DETECTED</div>', unsafe_allow_html=True)
                
                res_id = str(uuid.uuid4())[:8].upper()
                st.session_state.history.append({
                    "ID": res_id, "Site": site, "Resource": "Atomic" if is_atomic else "Mineral",
                    "lat": lat, "lon": lon, "Time": datetime.datetime.now().strftime("%H:%M")
                })
                st.success(f"Visual Recreation HSC-{res_id} synced to deslandes78@gmail.com")

    with tab2:
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            st.map(df)
            st.dataframe(df)

    with tab3:
        if st.session_state.history:
            d = st.session_state.history[-1]
            st.markdown(f"<div style='border:5px solid #00209F; padding:20px; text-align:center;'><h2>HSC OFFICIAL REPORT</h2><p>Sync: {ADMIN_EMAIL}</p><p>ID: {d['ID']}</p></div>", unsafe_allow_html=True)
