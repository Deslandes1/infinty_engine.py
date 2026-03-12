import streamlit as st
import datetime
import uuid
import json
from fpdf import FPDF
# --- 1. CONFIGURATION ET DONNÉES ---
RESOURCE_CLASSES = {
    "précieux": ["or", "argent", "platine", "palladium", "rhodium", "diamant", "émeraude"],
    "énergie": ["uranium", "thorium", "plutonium", "lithium", "cobalt", "nickel", "pétrole", "gaz"],
    "industriel": ["cuivre", "fer", "aluminium", "zinc", "bauxite", "titane", "iridium"],
    "terres_rares": ["néodyme", "lanthane", "cérium", "gadolinium", "scandium"]
}
MARKET_HUB = {
    "or": 167290.0, "uranium": 194.45, "iridium": 256230.0, "cuivre": 12.92,
    "lithium": 18500.0, "platine": 34200.0, "argent": 980.0, "thorium": 150.0
}
HTG_RATE = 131.19
MASTER_KEY = "20082010"
MONCASH_ID = "50947385663"
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'discovery_log' not in st.session_state: st.session_state.discovery_log = []
# --- 2. FONCTIONS TECHNIQUES ---
def analyze_resource(text):
    text = text.lower()
    for category, minerals in RESOURCE_CLASSES.items():
        for m in minerals:
            if m in text: return m, category
    return "Minéral Inconnu", "Non classé"
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 32, 159)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, "INFINITY ENGINE v33.0", ln=True, align='C')
    pdf.ln(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"ID RAPPORT : {data['id']}", ln=True)
    pdf.cell(0, 10, f"SITE : {data['site']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"RESSOURCE : {data['res'].upper()}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Valeur USD : ${data['usd']:,.2f}", ln=True)
    pdf.cell(0, 10, f"Valeur HTG : {data['htg']:,.2f} HTG", ln=True)
    return pdf.output(dest='S')
# --- 3. INTERFACE UTILISATEUR ---
st.set_page_config(page_title="Infinity Engine v33.0", layout="wide")
st.markdown("""
    <style>
    .main-header { background: linear-gradient(135deg, #00209F 0%, #D21034 100%); color: white; padding: 20px; border-radius: 15px; text-align: center; }
    .report-card { border: 2px solid #00209F; padding: 20px; border-radius: 10px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)
with st.sidebar:
    st.title("🛡️ Accès Moteur")
    if not st.session_state.authenticated:
        st.write(f"Payez via MonCash: **{MONCASH_ID}**")
        if st.text_input("Clé:", type="password") == MASTER_KEY:
            st.session_state.authenticated = True
            st.rerun()
        else:
         st.success("Accès Autorisé")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()
st.markdown('<div class="main-header"><h1>INFINITY ENGINE v33.0</h1></div>', unsafe_allow_html=True)
if st.session_state.authenticated:
    col1, col2 = st.columns([2, 1])
    with col1:
        site = st.text_input("Site:", "Grand Goâve")
        photo = st.camera_input("Scan")
        notes = st.text_area("Indices détectés:")
        weight = st.number_input("Masse (kg):", value=1.0)
        if st.button("🚀 ANALYSER"):
            if photo:
                res_name, res_cat = analyze_resource(notes)
                usd_val = MARKET_HUB.get(res_name, 0) * weight
                htg_val = usd_val * HTG_RATE
                rep_id = f"HSC-{uuid.uuid4().hex[:6].upper()}"
                # On définit report_data AVANT de l'utiliser
                report_data = {
                    "id": rep_id, "res": res_name, "cat": res_cat,
                    "site": site, "usd": usd_val, "htg": htg_val, "date": str(datetime.date.today())
                }
                st.session_state.discovery_log.append(report_data)
                st.markdown(f"""
                <div class="report-card">
                    <h3>Ressource: {res_name.upper()}</h3>
                    <p>Valeur: {usd_val:,.2f} USD / {htg_val:,.2f} HTG</p>
                </div>
                """, unsafe_allow_html=True)
        pdf_bytes = generate_pdf(report_data)
st.download_button("📥 Télécharger PDF", pdf_bytes, f"{rep_id}.pdf", "application/pdf")else:
st.error("Capture photo requise.") 
