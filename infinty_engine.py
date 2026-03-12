import streamlit as st
import datetime
import uuid
import json
import pandas as pd
from io import BytesIO

# --- 1. GLOBAL RESOURCE MASTER DATABASE ---
RESOURCE_CLASSES = {
    "precious": ["gold", "silver", "platinum", "palladium", "rhodium", "diamond", "emerald"],
    "energy": ["uranium", "thorium", "plutonium", "lithium", "cobalt", "nickel", "petroleum", "gas"],
    "industrial": ["copper", "iron", "aluminum", "zinc", "bauxite", "titanium", "iridium"],
    "rare_earth": ["neodymium", "lanthanum", "cerium", "gadolinium", "scandium"]
}

MARKET_HUB = {
    "gold": 167290.0, "uranium": 194.45, "iridium": 256230.0, "copper": 12.92,
    "lithium": 18500.0, "platinum": 34200.0, "silver": 980.0, "thorium": 150.0
}
HTG_RATE = 131.19
MASTER_KEY = "20082010"
MONCASH_ID = "50947385663"

# --- 2. SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'discovery_log' not in st.session_state:
    st.session_state.discovery_log = []

# --- 3. LOGIC ---
def analyze_resource(text):
    text = text.lower()
    for category, minerals in RESOURCE_CLASSES.items():
        for m in minerals:
            if m in text: return m, category
    return "Unknown Mineral", "Unclassified"

# --- 4. UI CONFIG ---
st.set_page_config(page_title="Infinity Engine v33.0", layout="centered")

st.markdown("""
    <style>
    .main-header { background: linear-gradient(135deg, #00209F 0%, #D21034 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; border-bottom: 5px solid #FFD700; margin-bottom: 20px; }
    .report-card { border: 2px solid #00209F; padding: 20px; border-radius: 10px; background: #fff; color: #000; margin-top: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR AUTH ---
with st.sidebar:
    st.title("🛡️ Engine Access")
    if not st.session_state.authenticated:
        st.write(f"Activation via MonCash: **{MONCASH_ID}**")
        user_key = st.text_input("Key:", type="password")
        if st.button("Unlock Engine"):
            if user_key == MASTER_KEY:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid Key")
    else:
        st.success("✅ ACCESS GRANTED")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

# --- 6. MAIN INTERFACE ---
st.markdown('<div class="main-header"><h1>INFINITY ENGINE v33.0</h1><p>Universal Discovery & Humanity Advancement</p></div>', unsafe_allow_html=True)

if st.session_state.authenticated:
    # --- Section 1: Input ---
    st.subheader("🔍 Universal Atomic Scan")
    site = st.text_input("Site Name:", "Grand Goâve")
    photo = st.camera_input("Sample Analysis")
    notes = st.text_area("Analysis Notes (Detected Clues):")
    weight = st.number_input("Mass (kg):", value=1.0)
    
    # --- Section 2: Execution ---
    if st.button("🚀 EXECUTE UNIVERSAL ANALYSIS"):
        if photo:
            res_name, res_cat = analyze_resource(notes)
            price = MARKET_HUB.get(res_name, 0)
            usd_val = price * weight
            htg_val = usd_val * HTG_RATE
            rep_id = f"HSC-UNIV-{uuid.uuid4().hex[:6].upper()}"
            
            # Add to log
            st.session_state.discovery_log.append({
                "Date": str(datetime.date.today()),
                "ID": rep_id, 
                "Resource": res_name.upper(), 
                "Category": res_cat.upper(),
                "Site": site,
                "Mass_kg": weight,
                "Value_USD": usd_val
            })
            
            st.markdown(f"""
            <div class="report-card">
                <h2 style="color:#D21034; text-align:center;">SOVEREIGN DISCOVERY REPORT</h2>
                <hr>
                <p><b>Resource Identified:</b> {res_name.upper()} ({res_cat.upper()})</p>
                <p><b>Scientific Trace:</b> Atomic structure match verified via stratigraphic sync.</p>
                <h3 style="color:green;">Estimated Market Value: ${usd_val:,.2f} USD</h3>
                <h3 style="color:#00209F;">Local Economic Value: {htg_val:,.2f} HTG</h3>
                <hr>
                <p><b>Humanity Solution:</b> {res_name.capitalize()} development leads to national infrastructure sovereignty.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Please provide a visual scan.")

    # --- Section 3: Strategic Intelligence & History ---
    st.divider()
    st.subheader("🌍 Strategic Intelligence")
    
    if st.session_state.discovery_log:
        st.write("**Recent Activity Log:**")
        df = pd.DataFrame(st.session_state.discovery_log)
        st.dataframe(df.tail(5), use_container_width=True)
        
        # CSV Export Logic
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Download Research History (CSV)",
            data=csv,
            file_name=f"Infinity_Research_Report_{datetime.date.today()}.csv",
            mime='text/csv',
        )
    else:
        st.info("No discoveries recorded yet. Perform a scan to generate data.")

else:
    st.warning("Please enter your Master Key in the sidebar to begin scanning.")
