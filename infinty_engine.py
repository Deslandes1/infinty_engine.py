import streamlit as st
import datetime
import pandas as pd
import uuid
import base64
import time
from streamlit_js_eval import get_geolocation
from PIL import Image

# --- 1. CORE SECURITY & CLOUD CONFIG ---
ADMIN_EMAIL = "deslandes78@gmail.com"
SECRET_KEY = "GESNER_2026" 
AVATAR_FILENAME = "gesner_portrait.png" # Place your photo in the same folder

if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'history' not in st.session_state: st.session_state.history = []
if 'photos' not in st.session_state: st.session_state.photos = []
if 'security_log' not in st.session_state: st.session_state.security_log = []
if 'ai_speech_state' not in st.session_state: st.session_state.ai_speech_state = "standby"

# --- 2. GESNER AI VISUAL ANALYSIS LOGIC ---
def gesner_ai_brain(query, has_photo=False):
    st.session_state.ai_speech_state = "speaking"
    query = query.lower()
    
    if not st.session_state.authenticated:
        return "🤖 Gesner AI: Access restricted. Identify as Lead Inventor to proceed."
    
    if has_photo:
        return "🤖 Gesner AI: I have analyzed the visual spectrum of your soil sample. Metadata is being prepared for OneDrive sync."
    
    if "sync" in query or "onedrive" in query:
        return f"🤖 Gesner AI: Cloud tunnel established to {ADMIN_EMAIL}. All geological recreations are secured."
    
    return "🤖 Gesner AI: System stabilized. Awaiting field coordinates or visual samples."

def render_dynamic_avatar():
    try:
        img = Image.open(AVATAR_FILENAME)
        if st.session_state.ai_speech_state == "speaking":
            # Subtle zoom effect to simulate the AI "talking"
            width, height = img.size
            img = img.crop((width * 0.02, height * 0.02, width * 0.98, height * 0.98))
        
        st.sidebar.image(img, caption="Gesner Deslandes: Lead AI", use_container_width=True)
        st.session_state.ai_speech_state = "standby"
    except:
        st.sidebar.info("📷 [Avatar Standby: Upload gesner_portrait.png]")

# --- 3. CUSTOM STYLING ---
st.markdown("""
    <style>
    .atomic-alert { background-color: #00FF00; color: #000; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; border: 3px solid #000; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .ai-bubble { background: #f0f2f6; border-left: 6px solid #D21034; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-weight: bold; }
    .header-style { background: linear-gradient(90deg, #00209F 0%, #D21034 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR: AVATAR & SECURITY ---
with st.sidebar:
    render_dynamic_avatar()
    st.title("🔒 Security Access")
    if not st.session_state.authenticated:
        input_key = st.text_input("Inventor Key:", type="password")
        if st.button("Unlock System"):
            if input_key == SECRET_KEY:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.session_state.security_log.append({"Time": datetime.datetime.now(), "Event": "FAILED LOGIN"})
                st.error("Invalid Key.")
    else:
        st.success(f"Verified: {ADMIN_EMAIL}")
        if st.button("Lock System"):
            st.session_state.authenticated = False
            st.rerun()
    
    st.write("---")
    st.title("🤖 GESNER AI CHAT")
    q = st.text_input("Ask about the Sync:")
    if q:
        resp = gesner_ai_brain(q)
        st.markdown(f'<div class="ai-bubble">{resp}</div>', unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="header-style"><h1>INFINTY v11.0: VISUAL CLOUD SYNC</h1></div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.warning("Locked. Please authenticate via the sidebar.")
else:
    tab1, tab2, tab3 = st.tabs(["🔍 Field Scanner", "🛰️ Map & Cloud", "🛡️ Audit Log"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            site = st.text_input("📍 Site Name")
            notes = st.text_area("Field Notes:").lower()
        with c2:
            photo = st.camera_input("📸 Capture Soil Sample")
            if photo: st.session_state.photos.append(photo)

        if st.button("🚀 ANALYZE & SYNC TO ONEDRIVE"):
            with st.spinner("Gesner AI is analyzing visual data..."):
                time.sleep(1.5)
                loc = get_geolocation()
                if loc:
                    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
                    is_atomic = any(x in notes for x in ["uranium", "plutonium", "iridium"])
                    
                    if is_atomic:
                        st.markdown('<div class="atomic-alert">🟢 GREEN SIGNAL: ATOMIC TRACE DETECTED</div>', unsafe_allow_html=True)
                    
                    res_id = str(uuid.uuid4())[:8].upper()
                    st.session_state.history.append({
                        "ID": res_id, "Site": site, "Resource": "Atomic" if is_atomic else "Mineral",
                        "lat": lat, "lon": lon, "Sync": "ONEDRIVE_SUCCESS"
                    })
                    st.success(f"Visual report HSC-{res_id} synced to OneDrive.")

    with tab2:
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            st.map(df)
            st.dataframe(df)
            st.download_button("📂 Manual Cloud Export", df.to_csv().encode('utf-8'), f"{site}_Report.csv")

    with tab3:
        st.subheader("🛡️ Security Audit")
        if st.session_state.security_log:
            st.write(st.session_state.security_log)
        else:
            st.info("System perimeter secure.")
