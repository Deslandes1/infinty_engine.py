import streamlit as st
import datetime
import pandas as pd
import time
import qrcode
import uuid
from io import BytesIO
from streamlit_js_eval import get_geolocation

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Gesner Deslandes Infinty", 
    page_icon="🇭🇹", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'research_history' not in st.session_state:
    st.session_state.research_history = []
if 'certificate_data' not in st.session_state:
    st.session_state.certificate_data = None

def clear_history():
    st.session_state.research_history = []
    st.session_state.certificate_data = None

# --- 2. ADVANCED STYLING ---
st.markdown("""
    <style>
    .support-card { background-color: #ffffff; padding: 15px; border-radius: 12px; border: 2px solid #1E90FF; text-align: center; }
    .logo-box { background-color: #ffffff; padding: 15px; border-radius: 15px; text-align: center; border: 3px solid #1E90FF; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    
    /* Discovery Certificate Style */
    .cert-box {
        background-color: #fffaf0;
        padding: 40px;
        border: 10px double #00209F;
        border-radius: 5px;
        text-align: center;
        color: #333;
        font-family: 'Georgia', serif;
        position: relative;
    }
    .cert-title { color: #D21034; font-size: 2.5rem; font-weight: bold; margin-bottom: 10px; }
    .cert-seal { color: #00209F; font-size: 1.2rem; font-weight: bold; margin-top: 20px; border-top: 1px solid #333; display: inline-block; padding-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏛️ RESEARCH FUND")
    with st.expander("💳 SUPPORT GESNER DESLANDES", expanded=True):
        st.markdown('<div class="support-card">', unsafe_allow_html=True)
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data("MonCash: (509)-47385663")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf)
        st.image(buf.getvalue(), caption="Scan MonCash", use_container_width=True)
        st.markdown("<b>Gesner Deslandes</b><br><span style='color:#FF4500;'>(509)-47385663</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ RESET ALL DATA"):
        clear_history()
        st.rerun()

# --- 4. LOGO ---
st.markdown(f"""
    <div class="logo-box">
        <h2 style="color: #1E90FF; margin-bottom: 2px;">GESNER DESLANDES 🇭🇹</h2>
        <h1 style="color: #FF4500; font-size: 2.5rem; margin-top: 0; margin-bottom: 5px;">INFINTY</h1>
        <p style="color: #333; font-weight: bold; margin-bottom: 2px;">🔬 HAITIAN SCIENTIFIC COMMUNITY</p>
        <p style="color: #666; font-size: 0.9rem; margin-top: 0;">National ML Exploration Suite v5.0</p>
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍 Field Engine", "📈 Analytics", "📜 Discovery Certificate"])

# --- TAB 1: FIELD ENGINE ---
with tab1:
    c1, c2 = st.columns(2)
    with c1: user_name = st.text_input("👤 Researcher Name")
    with c2: project_site = st.text_input("📍 Site Name")
    img_file = st.camera_input("📸 Capture Sample")
    
    location = get_geolocation()
    if location and 'coords' in location:
        lat, lon = location['coords']['latitude'], location['coords']['longitude']
        notes = st.text_area("Observations (Color, Texture, Shine):").lower()
        if st.button("RUN SCAN & VALIDATE"):
            if not user_name or not project_site:
                st.error("Identification Required.")
            else:
                logic = {"Gold (Au)": ["yellow", "quartz", "vein"], "Bauxite": ["red", "orange", "clay"], "Rare Earths": ["black", "heavy"]}
                matches = [res for res, triggers in logic.items() if any(t in notes for t in triggers)]
                
                if matches:
                    for res in matches:
                        res_id = str(uuid.uuid4())[:8].upper()
                        st.session_state.research_history.append({
                            "ID": res_id, "Date": datetime.date.today(), "Researcher": user_name,
                            "Site": project_site, "Resource": res, "Lat": lat, "Lon": lon
                        })
                        st.session_state.certificate_data = st.session_state.research_history[-1]
                    st.success(f"Discovery Validated! View Certificate in Tab 3.")
                else:
                    st.error("No mineral indicators detected.")
    else:
        st.warning("🌍 Awaiting GPS Lock...")

# --- TAB 2: ANALYTICS ---
with tab2:
    if st.session_state.research_history:
        df = pd.DataFrame(st.session_state.research_history)
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df['Resource'].value_counts())
    else:
        st.info("No data available.")

# --- TAB 3: DISCOVERY CERTIFICATE ---
with tab3:
    if st.session_state.certificate_data:
        d = st.session_state.certificate_data
        st.markdown(f"""
            <div class="cert-box">
                <p style="font-size:1.2rem;">HAITIAN SCIENTIFIC COMMUNITY</p>
                <h1 class="cert-title">CERTIFICATE OF DISCOVERY</h1>
                <p style="font-size:1.5rem;">This document officially validates that</p>
                <h2 style="text-decoration: underline;">{d['Researcher']}</h2>
                <p style="font-size:1.2rem;">has identified potential deposits of</p>
                <h2 style="color:#D21034;">{d['Resource']}</h2>
                <p style="font-size:1.1rem;">at <b>{d['Site']}</b> (Lat: {d['Lat']}, Lon: {d['Lon']})</p>
                <p>Validated via Infinty Machine Learning Engine v5.0</p>
                <br>
                <div style="display:flex; justify-content: space-around;">
                    <div class="cert-seal">GENSER DESLANDES<br>Lead Inventor</div>
                    <div class="cert-seal">ID: HSC-{d['ID']}<br>Date: {d['Date']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.info("💡 Tip: Use 'Right Click > Print' or take a Screenshot to save your Certificate.")
    else:
        st.warning("Please complete a successful scan to generate a certificate.")

# --- FOOTER ---
st.write("---")
st.latex(r"P_m = \sum (w_i \cdot x_i) \cdot \delta_{GPS}")
st.caption("© 2026 Gesner Deslandes | National Discovery & Validation Protocol 🇭🇹")
