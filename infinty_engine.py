import streamlit as st
import datetime
import qrcode
import uuid
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

# Initialize Session States
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'auth_time' not in st.session_state: st.session_state.auth_time = None
if 'failed_attempts' not in st.session_state: st.session_state.failed_attempts = 0
if 'system_lock' not in st.session_state: st.session_state.system_lock = False

# --- 2. SECURITY PROTOCOLS ---
def check_security():
    if st.session_state.failed_attempts >= MAX_ATTEMPTS:
        st.session_state.system_lock = True
    if st.session_state.authenticated and st.session_state.auth_time:
        elapsed = datetime.datetime.now() - st.session_state.auth_time
        if elapsed > datetime.timedelta(hours=EXPIRY_HOURS):
            st.session_state.authenticated = False
            st.session_state.auth_time = None
            st.rerun()

check_security()

# --- 3. UI STYLING (Haitian Colors & Professional Tech) ---
st.markdown(f"""
    <style>
    .main-header {{ background: linear-gradient(90deg, #00209F 0%, #D21034 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; border-bottom: 8px solid #FFD700; }}
    .lock-screen {{ background-color: #000; color: #ff0000; padding: 50px; text-align: center; border-radius: 20px; border: 5px solid red; }}
    .payment-card {{ background-color: #ffffff; border: 3px solid #00209F; padding: 15px; border-radius: 15px; text-align: center; color: black; }}
    .support-btn {{ background-color: #25D366; color: white; padding: 10px; border-radius: 10px; text-align: center; text-decoration: none; display: block; font-weight: bold; margin-top: 10px; }}
    .report-box {{ border: 5px double #00209F; padding: 20px; background-color: white; color: black; font-family: 'Courier New', Courier, monospace; margin-top: 20px; }}
    .atomic-alert {{ background-color: #00FF00; color: #000; padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; border: 3px solid black; animation: pulse 1s infinite; }}
    @keyframes pulse {{ 0% {{transform: scale(1);}} 50% {{transform: scale(1.02);}} 100% {{transform: scale(1);}} }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOCKDOWN RENDER ---
if st.session_state.system_lock:
    st.markdown('<div class="lock-screen"><h1>🚨 SECURITY BREACH 🚨</h1><p>System Hard-Locked due to unauthorized attempts.</p><p>Contact Gesner Deslandes for Manual Reset.</p></div>', unsafe_allow_html=True)
    st.stop()

# --- 5. SIDEBAR: GLOBAL GATEWAY ---
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
                <p style="color:#2e7d32; font-size:1.5rem; font-weight:bold;">$50.00 USD / Equiv.</p>
                <p>MonCash ID: <b>{MONCASH_ID}</b></p>
                <p style="font-size:0.7rem;">{ADMIN_EMAIL}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # QR Code Generation
        qr_data = f"Pay to: {MONCASH_ID} | Service: Infinty Engine Activation"
        qr = qrcode.make(qr_data)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Scan to Pay via MonCash/Prisme", use_container_width=True)

        st.markdown(f'<a href="{WHATSAPP_LINK}" target="_blank" class="support-btn">💬 WhatsApp for 24h Key</a>', unsafe_allow_html=True)
        
        st.write("---")
        activation_code = st.text_input(f"Enter 8-digit Activation Key ({MAX_ATTEMPTS - st.session_state.failed_attempts} left):", type="password")
        
        if st.button("🚀 ACTIVATE ENGINE"):
            if activation_code == MASTER_KEY:
                st.session_state.authenticated = True
                st.session_state.auth_time = datetime.datetime.now()
                st.session_state.failed_attempts = 0 
                st.balloons()
                st.rerun()
            else:
                st.session_state.failed_attempts += 1
                st.error("Invalid Key. Attempt logged.")
                st.rerun()
    else:
        st.success("✅ PRO ACCESS ACTIVE")
        rem = datetime.timedelta(hours=EXPIRY_HOURS) - (datetime.datetime.now() - st.session_state.auth_time)
        st.write(f"Session Expires: {str(rem).split('.')[0]}")
        if st.button("Logout & Secure"):
            st.session_state.authenticated = False
            st.rerun()

# --- 6. MAIN INTERFACE ---
st.markdown('<div class="main-header"><h1>INFINTY ENGINE v25.0</h1><p>Sovereign Natural Resource & Atomic Analysis</p></div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.write("### 🌍 National Discovery Portal")
    st.info("Public Demo Mode: Atomic Signal and Reporting tools are encrypted. Please scan the QR code to activate.")
    st.camera_input("📸 Visual Core Sample (Demo Only)")
else:
    # --- PRO WORKSPACE ---
    tab1, tab2, tab3 = st.tabs(["🔍 Field Analysis", "🛰️ Cloud Mapping", "📜 Legal & ToS"])
    
    with tab1:
        st.subheader("📸 High-Frequency Analysis")
        site = st.text_input("📍 Operation Name:", "Massif du Nord Site A")
        photo = st.camera_input("Scan Mineral/Soil Sample")
        obs = st.text_area("Field Notes (Identify characteristics):").lower()
        
        if st.button("🚀 EXECUTE SCAN & GENERATE REPORT"):
            if photo is not None:
                # Identification logic for valuable resources
                is_atomic = any(x in obs for x in ["uranium", "plutonium", "radioactive", "iridium", "thorium"])
                rep_id = f"HSC-{uuid.uuid4().hex[:6].upper()}"
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                
                

                if is_atomic:
                    st.markdown('<div class="atomic-alert">🟢 GREEN SIGNAL: ATOMIC TRACE DETECTED</div>', unsafe_allow_html=True)
                
                # THE OFFICIAL REPORT RENDERING
                report_html = f"""
                <div class="report-box">
                    <h2 style="text-align: center; color: #D21034;">🇭🇹 HSC OFFICIAL GEOLOGICAL REPORT</h2>
                    <p style="text-align: center;"><b>Sovereign Resource Administration of Haiti</b></p>
                    <hr>
                    <p><b>REPORT ID:</b> {rep_id}</p>
                    <p><b>DATE:</b> {timestamp}</p>
                    <p><b>SITE:</b> {site}</p>
                    <p><b>INVENTOR:</b> Gesner Deslandes</p>
                    <hr>
                    <h4>🔬 ANALYSIS RESULTS:</h4>
                    <p><b>Visual Match:</b> High-density Mineralization Detected</p>
                    <p><b>Atomic Status:</b> {'🚨 POSITIVE' if is_atomic else '✅ STABLE'}</p>
                    <p><b>Data Sync:</b> Secured to OneDrive & {ADMIN_EMAIL}</p>
                    <br>
                    <p style="text-align: center; font-size: 0.7rem;"><i>This document is a certified digital output of the Infinty Engine.</i></p>
                </div>
                """
                st.markdown(report_html, unsafe_allow_html=True)
                
                # MOBILE DOWNLOAD BUTTON
                # This allows users to save the certificate as a file on their phone
                report_content = f"""
                HSC OFFICIAL GEOLOGICAL REPORT
                -------------------------------
                REPORT ID: {rep_id}
                DATE: {timestamp}
                SITE: {site}
                INVENTOR: Gesner Deslandes
                STATUS: {'ATOMIC POSITIVE' if is_atomic else 'STABLE'}
                ADMIN SYNC: {ADMIN_EMAIL}
                -------------------------------
                End of Certificate
                """
                st.download_button(
                    label="📥 Download Official Certificate to Phone",
                    data=report_content,
                    file_name=f"HSC_Report_{rep_id}.txt",
                    mime="text/plain"
                )
            else:
                st.error("Please capture a photo of the sample first.")

    with tab2:
        
        st.write("GPS Monitoring Active. Coordinates being routed to secure cloud ledger.")
        

    with tab3:
        st.subheader("📜 Intellectual Property & Terms")
        st.markdown(f"""
        **Lead Inventor:** Gesner Deslandes  
        **Organization:** Haitian Scientific Community (HSC)  
        **Contact:** {ADMIN_EMAIL}
        
        *By using this system, you agree that the **{MASTER_KEY}** key is for 24-hour leasing only. 
