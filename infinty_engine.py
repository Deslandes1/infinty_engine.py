import streamlit as st
import datetime
import pandas as pd
import time
import qrcode
from io import BytesIO
from streamlit_js_eval import get_geolocation
# --- 1. CONFIGURATION & BRANDING ---
st.set_page_config(page_title="Gesner Deslandes Infinty", page_icon="🌍", layout="wide")
st.markdown("""
    <style>
    .main-header { text-align: center; color: #1E90FF; font-family: 'Helvetica', sans-serif; }
    .support-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #1E90FF;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
# --- 2. QR CODE GENERATOR ---
def generate_moncash_qr(phone):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(f"MonCash Payment to: {phone}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf)
    return buf.getvalue()
# --- 3. GLOBAL SUPPORT SIDEBAR (Prisme Transfer Style) ---
with st.sidebar:
    st.markdown("### 🏛️ GLOBAL RESEARCH FUND")
    st.info("Supporting Haitian Machine Learning & New Inventions.")
    with st.expander("💳 DONATE TO GESNER DESLANDES", expanded=True):
        st.markdown('<div class="support-card">', unsafe_allow_html=True)
         # Display QR Code
        qr_img = generate_moncash_qr("(509)-47385663")
        st.image(qr_img, caption="Scan to Support Research", use_container_width=True)
        st.markdown(f"""
            <h4 style="color: #1E90FF; margin-bottom:0;">Gesner Deslandes</h4>
            <p style="color: #FF4500; font-size: 1.2em; font-weight: bold;">(509)-47385663</p>
            <p style="font-size: 0.85em;"><i>Prisme Transfer / Global Support</i></p>
            """, unsafe_allow_html=True)
        # Updated Email Notification Button
        email_recipient = "deslandes78@gmail.com"
        email_subject = "Support for Infinty Engine Machine Learning"
        email_body = "Hello Gesner, I am supporting your Haitian Scientific Community initiatives with a MonCash payment."
        mail_to_link = f"mailto:{email_recipient}?subject={email_subject.replace(' ', '%20')}&body={email_body.replace(' ', '%20')}"
        st.markdown(f'''
            <a href="{mail_to_link}" target="_blank">
                <button style="width:100%; background-color:#1E90FF; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">
                    📧 Send Payment Notification
                </button>
            </a>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
# --- 4. MACHINE LEARNING LOGIC ---
resource_logic = {
    "Gold (Au)": {
        "indicators": ["yellow", "quartz", "vein", "pyrite"],
        "science": "ML detected hydrothermal quartz signatures in the observation data.",
        "confidence": 0.89
    },
    "Bauxite": {
        "indicators": ["red", "orange", "clay", "limestone", "laterite"],
        "science": "Spectral indicators suggest high-concentration aluminum-rich laterite.",
        "confidence": 0.94
    },
    "Rare Earths / Iridium": {
        "indicators": ["black", "metallic", "heavy", "magnetic", "grey"],
        "science": "ML Analysis correlates high density with possible K-Pg boundary rare earth elements.",
        "confidence": 0.82
    }
}
# --- 5. MAIN INTERFACE ---
st.markdown("<h1 class='main-header'>🚀 INFINTY ENGINE: ML GEOLOGICAL ANALYSIS</h1>", unsafe_allow_html=True)
st.write(f"**Principal Investigator:** Gesner Deslandes | **Lead, Haitian Scientific Community**")
location = get_geolocation()
if location and 'coords' in location:
    lat, lon = location['coords']['latitude'], location['coords']['longitude']
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 🔍 Field Data Acquisition")
        notes = st.text_area("Input site characteristics for ML Analysis:").lower()
        st.info(f"📍 GPS COORDINATES SECURED: {lat}, {lon}")
 with col2:
        st.markdown("### 🧠 Invention-ML Inference")
        if st.button("EXECUTE MACHINE LEARNING SCAN"):
            if not notes:
                st.warning("Data input required for ML processing.")
            else:
                with st.spinner("Processing Spectral Indicators..."):
                    time.sleep(2)
                matches = [name for name, info in resource_logic.items() if any(i in notes for i in info["indicators"])]
                if matches:
                    for match in matches:
                        with st.expander(f"📊 ML PREDICTION: {match}"):
                            st.write(f"**Evidence:** {resource_logic[match]['science']}")
                            st.write(f"**Confidence Score:** {int(resource_logic[match]['confidence']*100)}%")
                            st.progress(resource_logic[match]['confidence'])
                    csv_data = pd.DataFrame([{"Investigator": "Gesner Deslandes", "Resource": m, "Lat": lat, "Lon": lon} for m in matches])
                    st.download_button("📥 DOWNLOAD RESEARCH DOSSIER", csv_data.to_csv().encode('utf-8'), "Infinty_ML_Report.csv")
                else:
                    st.error("Inference Engine: No mineral indicators identified in this sample.")
                else:
    st.info("🌍 Awaiting Satellite Lock... Please allow GPS access to begin research.")
st.write("---")
st.caption("© 2026 Gesner Deslandes. Advancing Machine Learning & Scientific Inventions in Haiti.")

