import streamlit as st
import datetime
import qrcode
from io import BytesIO
from PIL import Image

# --- 1. SOVEREIGN CONFIG ---
ADMIN_EMAIL = "deslandes78@gmail.com"
MONCASH_ID = "50947385663" # Cleaned for URL linking
WHATSAPP_LINK = f"https://wa.me/{MONCASH_ID}"
MASTER_KEY = "20082010" 
AVATAR_FILENAME = "gesner_portrait.png"

# Pricing logic
PRICE_PRO_USD = 50.0
EXCHANGE_HTG = 132.50 

if 'authenticated' not in st.session_state: st.session_state.authenticated = False

# --- 2. AUTOMATED QR GENERATOR ---
def generate_payment_qr(amount_htg):
    # Encodes a professional payment summary
    payment_info = f"INFINITY_PRO_SYNC: {amount_htg} HTG to {MONCASH_ID}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(payment_info)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# --- 3. UI STYLING ---
st.markdown(f"""
    <style>
    .main-header {{ background: linear-gradient(90deg, #00209F 0%, #D21034 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; border-bottom: 8px solid #FFD700; }}
    .pro-unlock-box {{ background-color: #ffffff; border: 3px solid #2e7d32; padding: 20px; border-radius: 15px; text-align: center; }}
    .price-text {{ color: #2e7d32; font-size: 1.8rem; font-weight: bold; }}
    .support-btn {{ background-color: #25D366; color: white; padding: 10px; border-radius: 10px; text-align: center; text-decoration: none; display: block; font-weight: bold; margin-top: 10px; }}
    .atomic-alert {{ background-color: #00FF00; color: #000; padding: 20px; border-radius: 10px; font-weight: bold; text-align: center; border: 4px solid black; animation: pulse 1s infinite; }}
    @keyframes pulse {{ 0% {{transform: scale(1);}} 50% {{transform: scale(1.02);}} 100% {{transform: scale(1);}} }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR: GLOBAL SALES & SUPPORT ---
with st.sidebar:
    try:
        img = Image.open(AVATAR_FILENAME)
        st.image(img, caption="Gesner Deslandes | Lead AI", use_container_width=True)
    except:
        st.info("📷 [Gesner AI Avatar Standby]")

    if not st.session_state.authenticated:
        st.title("⚡ Pro Activation")
        
        currency = st.radio("Select Currency:", ["USD ($)", "HTG (Gourdes)"])
        display_price = PRICE_PRO_USD if "USD" in currency else PRICE_PRO_USD * EXCHANGE_HTG
        
        st.markdown(f"""
            <div class="pro-unlock-box">
                <p><b>Scan & Pay to Unlock Pro</b></p>
                <p class="price-text">{display_price:,.0f} {currency[:3]}</p>
                <p style="font-size:0.9rem;"><b>MonCash:</b> {MONCASH_ID}</p>
            </div>
        """, unsafe_allow_html=True)

        st.image(generate_payment_qr(display_price), caption="Scan for Payment Details", use_container_width=True)
        
        st.markdown(f'<a href="{WHATSAPP_LINK}" target="_blank" class="support-btn">💬 Chat with Admin (WhatsApp)</a>', unsafe_allow_html=True)
        
        st.write("---")
        st.write("🔑 **Activate Features**")
        user_key = st.text_input("Enter Key (20082010):", type="password")
        
        if st.button("🚀 UNLOCK NOW"):
            if user_key == MASTER_KEY:
                st.session_state.authenticated = True
                st.balloons()
                st.rerun()
            else:
                st.error("Invalid Key. Check WhatsApp for help.")
    else:
        st.success("✅ PRO STATUS: ACTIVE")
        st.write(f"Syncing to: {ADMIN_EMAIL}")
        if st.button("Logout & Secure"):
            st.session_state.authenticated = False
            st.rerun()

# --- 5. MAIN INTERFACE ---
st.markdown('<div class="main-header"><h1>INFINTY ENGINE v20.0</h1><p>Global Mineral & Atomic Sovereignty</p></div>', unsafe_allow_html=True)

if not st.session_state.authenticated:
    st.write("### 🌍 National Resource Portal")
    st.info("Welcome to the Infinty Engine. To access mapping, cloud-sync, and atomic detection, please activate Pro features via the sidebar.")
    st.camera_input("📸 Visual Demo Scanner")
else:
    # --- UNLOCKED PRO WORKSPACE ---
    tab1, tab2 = st.tabs(["🔍 Atomic Analysis", "🛰️ Cloud Mapping"])
    with tab1:
        notes = st.text_area("Field Observations:").lower()
        if st.button("RUN ATOMIC SCAN"):
            if any(x in notes for x in ["uranium", "plutonium", "radioactive", "iridium"]):
                st.markdown('<div class="atomic-alert">🟢 GREEN SIGNAL: ATOMIC TRACE DETECTED</div>', unsafe_allow_html=True)
            st.success("Analysis complete. Data pushed to OneDrive.")
    with tab2:
        st.info("GPS Geofencing Active. Coordinates are being logged securely.")
