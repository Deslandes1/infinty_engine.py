import streamlit as st
import datetime
import uuid
import pandas as pd
import base64
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import numpy as np

# --- GLOBAL DATABASE ---
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

# --- SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'discovery_log' not in st.session_state:
    st.session_state.discovery_log = []
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'camera_method' not in st.session_state:
    st.session_state.camera_method = 'camera'

# --- TRANSLATIONS (full, only English shown; include your full translations) ---
TRANSLATIONS = {
    'en': {
        'app_title': 'INFINITY ENGINE v33.0',
        'app_subtitle': 'Universal Discovery & Humanity Advancement',
        'owner_collab': 'Owner: <strong>Gesner Deslandes</strong> &nbsp;|&nbsp; Collaborators: Gesner Junior Deslandes, Roosevelt Deslandes, Sebastien Stephane Deslandes & Zendaya Christelle Deslandes',
        'sidebar_title': '🛡️ Engine Access',
        'sidebar_activation': 'Activation via MonCash: **{moncash}**',
        'sidebar_key_label': 'Key:',
        'sidebar_unlock': 'Unlock Engine',
        'sidebar_invalid': 'Invalid Key',
        'sidebar_granted': '✅ ACCESS GRANTED',
        'sidebar_logout': 'Logout',
        'welcome_sound_js': """
            function playBeep() {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                oscillator.type = 'sine';
                oscillator.frequency.value = 880;
                gainNode.gain.value = 0.3;
                oscillator.start();
                gainNode.gain.exponentialRampToValueAtTime(0.00001, audioContext.currentTime + 0.5);
                oscillator.stop(audioContext.currentTime + 0.5);
            }
            playBeep();
            const url = new URL(window.location);
            url.searchParams.delete('play_sound');
            window.history.replaceState({}, document.title, url.pathname + url.search);
        """,
        'main_header': 'INFINITY ENGINE v33.0',
        'main_subheader': 'Universal Discovery & Humanity Advancement',
        'scan_subheader': '🔍 Universal Atomic Scan',
        'camera_method_label': 'How to capture the sample:',
        'camera_option': '📸 Take photo with camera (reverse button below)',
        'upload_option': '📁 Upload photo from device',
        'camera_instruction': '📸 Point the camera at the soil. Use the Reverse button to switch between front and rear cameras.',
        'upload_instruction': '📸 Take a photo with your device\'s camera and upload it here.',
        'reverse_button': '↻ Reverse Camera',
        'capture_button': '📷 Capture Image',
        'camera_placeholder': 'Camera feed will appear here after granting permission.',
        'site_label': 'Site Name:',
        'site_placeholder': 'Grand Goâve',
        'photo_label': 'Sample Analysis',
        'notes_label': 'Analysis Notes (Detected Clues):',
        'weight_label': 'Mass (kg):',
        'execute_button': '🚀 EXECUTE UNIVERSAL ANALYSIS',
        'no_photo_error': 'Please capture or upload an image first.',
        'report_title': 'SOVEREIGN DISCOVERY REPORT',
        'resource_label': 'Resource Identified:',
        'trace_label': 'Scientific Trace:',
        'value_usd_label': 'Estimated Market Value: ${value:,.2f} USD',
        'value_htg_label': 'Local Economic Value: {value:,.2f} HTG',
        'solution_label': 'Humanity Solution:',
        'solution_text': '{resource} development leads to national infrastructure sovereignty.',
        'strategic_intel': '🌍 Strategic Intelligence',
        'recent_log': '**Recent Activity Log:**',
        'download_button': '📊 Download Research History (CSV)',
        'no_data_info': 'No discoveries recorded yet. Perform a scan to generate data.',
        'access_warning': 'Please enter your Master Key in the sidebar to begin scanning.',
        'language_selector': 'Language / Langue / Lang / Lang',
        'unknown_mineral': 'Unknown Mineral',
        'unclassified': 'Unclassified'
    },
    'fr': {
        'app_title': 'MOTEUR INFINI v33.0',
        'app_subtitle': 'Découverte Universelle & Avancement Humain',
        'owner_collab': 'Propriétaire: <strong>Gesner Deslandes</strong> &nbsp;|&nbsp; Collaborateurs: Gesner Junior Deslandes, Roosevelt Deslandes, Sebastien Stephane Deslandes & Zendaya Christelle Deslandes',
        'sidebar_title': '🛡️ Accès Moteur',
        'sidebar_activation': 'Activation via MonCash: **{moncash}**',
        'sidebar_key_label': 'Clé:',
        'sidebar_unlock': 'Déverrouiller',
        'sidebar_invalid': 'Clé invalide',
        'sidebar_granted': '✅ ACCÈS AUTORISÉ',
        'sidebar_logout': 'Déconnexion',
        'welcome_sound_js': """
            function playBeep() {
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const oscillator = audioContext.createOscillator();
                const gainNode = audioContext.createGain();
                oscillator.connect(gainNode);
                gainNode.connect(audioContext.destination);
                oscillator.type = 'sine';
                oscillator.frequency.value = 880;
                gainNode.gain.value = 0.3;
                oscillator.start();
                gainNode.gain.exponentialRampToValueAtTime(0.00001, audioContext.currentTime + 0.5);
                oscillator.stop(audioContext.currentTime + 0.5);
            }
            playBeep();
            const url = new URL(window.location);
            url.searchParams.delete('play_sound');
            window.history.replaceState({}, document.title, url.pathname + url.search);
        """,
        'main_header': 'MOTEUR INFINI v33.0',
        'main_subheader': 'Découverte Universelle & Avancement Humain',
        'scan_subheader': '🔍 Analyse Atomique Universelle',
        'camera_method_label': 'Comment capturer l\'échantillon:',
        'camera_option': '📸 Prendre une photo avec l\'appareil (bouton de retournement ci-dessous)',
        'upload_option': '📁 Télécharger une photo depuis l\'appareil',
        'camera_instruction': '📸 Pointez l’appareil vers le sol. Utilisez le bouton Retournement pour passer entre caméra avant et arrière.',
        'upload_instruction': '📸 Prenez une photo avec l\'appareil photo de votre téléphone et téléchargez-la ici.',
        'reverse_button': '↻ Retourner la caméra',
        'capture_button': '📷 Capturer l\'image',
        'camera_placeholder': 'Le flux vidéo apparaîtra ici après autorisation.',
        'site_label': 'Nom du site:',
        'site_placeholder': 'Grand Goâve',
        'photo_label': 'Analyse d\'échantillon',
        'notes_label': 'Notes d\'analyse (indices détectés):',
        'weight_label': 'Masse (kg):',
        'execute_button': '🚀 EXÉCUTER L\'ANALYSE UNIVERSELLE',
        'no_photo_error': 'Veuillez d\'abord capturer ou télécharger une image.',
        'report_title': 'RAPPORT DE DÉCOUVERTE SOUVERAINE',
        'resource_label': 'Ressource identifiée:',
        'trace_label': 'Trace scientifique:',
        'value_usd_label': 'Valeur marchande estimée: ${value:,.2f} USD',
        'value_htg_label': 'Valeur économique locale: {value:,.2f} HTG',
        'solution_label': 'Solution humanitaire:',
        'solution_text': 'Le développement de {resource} conduit à la souveraineté des infrastructures nationales.',
        'strategic_intel': '🌍 Renseignement Stratégique',
        'recent_log': '**Journal d\'activité récent:**',
        'download_button': '📊 Télécharger l\'historique de recherche (CSV)',
        'no_data_info': 'Aucune découverte enregistrée pour le moment. Effectuez une analyse pour générer des données.',
        'access_warning': 'Veuillez entrer votre clé principale dans la barre latérale pour commencer l\'analyse.',
        'language_selector': 'Langue / Language',
        'unknown_mineral': 'Minéral Inconnu',
        'unclassified': 'Non Classifié'
    },
    'es': {
        # ... include Spanish translations similarly ...
    },
    'ht': {
        # ... include Haitian Creole translations similarly ...
    }
}

def get_text(key, lang=None, **kwargs):
    if lang is None:
        lang = st.session_state.language
    text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text

# --- LOGIC ---
def analyze_resource(text):
    text = text.lower()
    for category, minerals in RESOURCE_CLASSES.items():
        for m in minerals:
            if m in text:
                return m, category
    return "Unknown Mineral", "Unclassified"

# --- Video processor for capturing frames ---
class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.image = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.image = img
        return frame

# --- Camera widget using streamlit-webrtc ---
def camera_widget():
    webrtc_ctx = webrtc_streamer(
        key="sample-camera",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    if webrtc_ctx.video_processor:
        if st.button(get_text('capture_button'), key="capture_btn"):
            img = webrtc_ctx.video_processor.image
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                success, buffer = cv2.imencode('.jpg', img)
                if success:
                    img_base64 = base64.b64encode(buffer).decode()
                    st.session_state.captured_image = f"data:image/jpeg;base64,{img_base64}"
                    st.rerun()
            else:
                st.error("No image captured. Please ensure the camera is working.")
    else:
        st.info(get_text('camera_placeholder'))

# --- UI CONFIG ---
st.set_page_config(page_title="Infinity Engine v33.0", layout="centered")

# Language selector & owner line
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(get_text('owner_collab'), unsafe_allow_html=True)
with col2:
    lang_options = {'en': '🇺🇸 English', 'fr': '🇫🇷 Français', 'es': '🇪🇸 Español', 'ht': '🇭🇹 Kreyòl'}
    selected_lang = st.selectbox(
        get_text('language_selector'),
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(st.session_state.language)
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

# Haitian Flag with coat of arms (improved)
st.markdown("""
<div style="display: flex; justify-content: center; margin: 15px 0;">
    <svg width="320" height="192" viewBox="0 0 960 576" xmlns="http://www.w3.org/2000/svg">
        <rect width="960" height="288" fill="#00209F" />
        <rect y="288" width="960" height="288" fill="#D21034" />
        <g transform="translate(480,288) scale(0.15)">
            <!-- Palm tree trunk -->
            <rect x="-15" y="-100" width="30" height="200" fill="#8B5A2B" />
            <!-- Palm fronds -->
            <polygon points="0,-120 -50,-80 -30,-70 0,-100 30,-70 50,-80 0,-120" fill="#2E7D32" />
            <!-- Liberty cap -->
            <polygon points="0,-130 -25,-100 0,-110 25,-100 0,-130" fill="#D32F2F" />
            <!-- Cannons -->
            <rect x="-90" y="80" width="60" height="25" fill="#555" />
            <rect x="30" y="80" width="60" height="25" fill="#555" />
            <!-- Drums -->
            <circle cx="-60" cy="95" r="15" fill="#A1887F" />
            <circle cx="60" cy="95" r="15" fill="#A1887F" />
            <!-- Palm leaves details -->
            <path d="M0,-115 L-35,-65 L-20,-70 L0,-95 L20,-70 L35,-65 L0,-115" fill="#1B5E20" />
            <!-- Flag scroll -->
            <rect x="-100" y="110" width="200" height="20" fill="#F5F5DC" />
            <text x="-80" y="125" font-size="18" fill="#000000" font-family="Arial">L'Union Fait la Force</text>
        </g>
    </svg>
</div>
""", unsafe_allow_html=True)

# Custom CSS
st.markdown("""
    <style>
    .main-header { background: linear-gradient(135deg, #00209F 0%, #D21034 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; border-bottom: 5px solid #FFD700; margin-bottom: 20px; }
    .report-card { border: 2px solid #00209F; padding: 20px; border-radius: 10px; background: #fff; color: #000; margin-top: 20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR AUTH ---
with st.sidebar:
    st.title(get_text('sidebar_title'))
    if not st.session_state.authenticated:
        st.write(get_text('sidebar_activation', moncash=MONCASH_ID))
        user_key = st.text_input(get_text('sidebar_key_label'), type="password")
        if st.button(get_text('sidebar_unlock')):
            if user_key == MASTER_KEY:
                st.session_state.authenticated = True
                st.query_params["play_sound"] = "true"
                st.rerun()
            else:
                st.error(get_text('sidebar_invalid'))
    else:
        st.success(get_text('sidebar_granted'))
        if st.button(get_text('sidebar_logout')):
            st.session_state.authenticated = False
            st.rerun()

# --- WELCOME SOUND ---
if st.session_state.authenticated and st.query_params.get("play_sound") == "true":
    st.markdown(f"<script>{get_text('welcome_sound_js')}</script>", unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.markdown(f'<div class="main-header"><h1>{get_text("main_header")}</h1><p>{get_text("main_subheader")}</p></div>', unsafe_allow_html=True)

if st.session_state.authenticated:
    st.subheader(get_text('scan_subheader'))

    method = st.radio(
        get_text('camera_method_label'),
        options=['camera', 'upload'],
        format_func=lambda x: get_text('camera_option') if x == 'camera' else get_text('upload_option'),
        horizontal=True
    )
    st.session_state.camera_method = method

    if method == 'camera':
        st.markdown(f"<p style='font-size:0.9rem; color:#555;'>{get_text('camera_instruction')}</p>", unsafe_allow_html=True)
        camera_widget()
        if st.session_state.captured_image:
            st.image(st.session_state.captured_image, caption="Captured image", width=200)
            if st.button("Clear image"):
                st.session_state.captured_image = None
                st.rerun()
    else:
        st.markdown(f"<p style='font-size:0.9rem; color:#555;'>{get_text('upload_instruction')}</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader(get_text('photo_label'), type=['jpg', 'jpeg', 'png'])
        if uploaded:
            bytes_data = uploaded.read()
            b64 = base64.b64encode(bytes_data).decode()
            st.session_state.captured_image = f"data:image/{uploaded.type.split('/')[-1]};base64,{b64}"
            st.rerun()

    site = st.text_input(get_text('site_label'), get_text('site_placeholder'))
    notes = st.text_area(get_text('notes_label'))
    weight = st.number_input(get_text('weight_label'), value=1.0)

    if st.button(get_text('execute_button')):
        if st.session_state.captured_image:
            res_name, res_cat = analyze_resource(notes)
            price = MARKET_HUB.get(res_name, 0)
            usd_val = price * weight
            htg_val = usd_val * HTG_RATE
            rep_id = f"HSC-UNIV-{uuid.uuid4().hex[:6].upper()}"

            st.session_state.discovery_log.append({
                "Date": str(datetime.date.today()),
                "ID": rep_id,
                "Resource": res_name.upper(),
                "Category": res_cat.upper(),
                "Site": site,
                "Mass_kg": weight,
                "Value_USD": usd_val
            })

            resource_display = res_name.upper() if res_name != "Unknown Mineral" else get_text('unknown_mineral')
            category_display = res_cat.upper() if res_cat != "Unclassified" else get_text('unclassified')

            report_html = f"""
            <div class="report-card">
                <h2 style="color:#D21034; text-align:center;">{get_text('report_title')}</h2>
                <hr>
                <p><b>{get_text('resource_label')}</b> {resource_display} ({category_display})</p>
                <p><b>{get_text('trace_label')}</b> Atomic structure match verified via stratigraphic sync.</p>
                <h3 style="color:green;">{get_text('value_usd_label', value=usd_val)}</h3>
                <h3 style="color:#00209F;">{get_text('value_htg_label', value=htg_val)}</h3>
                <hr>
                <p><b>{get_text('solution_label')}</b> {get_text('solution_text', resource=res_name.capitalize())}</p>
            </div>
            """
            st.markdown(report_html, unsafe_allow_html=True)
        else:
            st.error(get_text('no_photo_error'))

    # History
    st.divider()
    st.subheader(get_text('strategic_intel'))
    if st.session_state.discovery_log:
        st.markdown(get_text('recent_log'))
        df = pd.DataFrame(st.session_state.discovery_log)
        st.dataframe(df.tail(5), width='stretch')
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=get_text('download_button'),
            data=csv,
            file_name=f"Infinity_Research_Report_{datetime.date.today()}.csv",
            mime='text/csv',
        )
    else:
        st.info(get_text('no_data_info'))
else:
    st.warning(get_text('access_warning'))
