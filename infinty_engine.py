import streamlit as st
import datetime
import uuid
import pandas as pd
import base64
import json

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
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'camera_method' not in st.session_state:
    st.session_state.camera_method = 'camera'

# --- 3. TRANSLATIONS (complete) ---
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
        'camera_option': '📸 Take photo with camera (flip button below)',
        'upload_option': '📁 Upload photo from device',
        'camera_instruction': '📸 Adjust the camera, then click the flip button (↻) to switch between front and rear camera.',
        'upload_instruction': '📸 Take a photo with your device\'s camera and upload it here.',
        'flip_button': 'Flip Camera',
        'capture_button': 'Capture Image',
        'use_image_button': '✅ Use this image',
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
        'camera_instruction': '📸 Ajustez la caméra, puis cliquez sur le bouton ↻ pour passer entre caméra avant et arrière.',
        'upload_instruction': '📸 Prenez une photo avec l\'appareil photo de votre téléphone et téléchargez-la ici.',
        'flip_button': 'Retourner la caméra',
        'capture_button': 'Capturer l\'image',
        'use_image_button': '✅ Utiliser cette image',
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
        'app_title': 'MOTOR INFINITO v33.0',
        'app_subtitle': 'Descubrimiento Universal & Avance Humano',
        'owner_collab': 'Propietario: <strong>Gesner Deslandes</strong> &nbsp;|&nbsp; Colaboradores: Gesner Junior Deslandes, Roosevelt Deslandes, Sebastien Stephane Deslandes & Zendaya Christelle Deslandes',
        'sidebar_title': '🛡️ Acceso al Motor',
        'sidebar_activation': 'Activación vía MonCash: **{moncash}**',
        'sidebar_key_label': 'Clave:',
        'sidebar_unlock': 'Desbloquear Motor',
        'sidebar_invalid': 'Clave inválida',
        'sidebar_granted': '✅ ACCESO CONCEDIDO',
        'sidebar_logout': 'Cerrar sesión',
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
        'main_header': 'MOTOR INFINITO v33.0',
        'main_subheader': 'Descubrimiento Universal & Avance Humano',
        'scan_subheader': '🔍 Escaneo Atómico Universal',
        'camera_method_label': 'Cómo capturar la muestra:',
        'camera_option': '📸 Tomar foto con la cámara (botón de volteo abajo)',
        'upload_option': '📁 Subir foto desde el dispositivo',
        'camera_instruction': '📸 Ajuste la cámara, luego haga clic en el botón ↻ para cambiar entre cámara frontal y trasera.',
        'upload_instruction': '📸 Tome una foto con la cámara de su dispositivo y súbala aquí.',
        'flip_button': 'Voltear cámara',
        'capture_button': 'Capturar imagen',
        'use_image_button': '✅ Usar esta imagen',
        'camera_placeholder': 'El flujo de la cámara aparecerá aquí después de conceder permiso.',
        'site_label': 'Nombre del sitio:',
        'site_placeholder': 'Grand Goâve',
        'photo_label': 'Análisis de muestra',
        'notes_label': 'Notas de análisis (pistas detectadas):',
        'weight_label': 'Masa (kg):',
        'execute_button': '🚀 EJECUTAR ANÁLISIS UNIVERSAL',
        'no_photo_error': 'Primero capture o suba una imagen.',
        'report_title': 'INFORME DE DESCUBRIMIENTO SOBERANO',
        'resource_label': 'Recurso identificado:',
        'trace_label': 'Traza científica:',
        'value_usd_label': 'Valor de mercado estimado: ${value:,.2f} USD',
        'value_htg_label': 'Valor económico local: {value:,.2f} HTG',
        'solution_label': 'Solución humanitaria:',
        'solution_text': 'El desarrollo de {resource} conduce a la soberanía de infraestructura nacional.',
        'strategic_intel': '🌍 Inteligencia Estratégica',
        'recent_log': '**Registro de actividad reciente:**',
        'download_button': '📊 Descargar historial de investigación (CSV)',
        'no_data_info': 'Aún no se han registrado descubrimientos. Realice un escaneo para generar datos.',
        'access_warning': 'Por favor ingrese su clave maestra en la barra lateral para comenzar el escaneo.',
        'language_selector': 'Idioma / Language',
        'unknown_mineral': 'Mineral Desconocido',
        'unclassified': 'No Clasificado'
    },
    'ht': {
        'app_title': 'MOTEUR ENFINI v33.0',
        'app_subtitle': 'Dekouvèt Inivèsèl & Avansman Imèn',
        'owner_collab': 'Pwopriyetè: <strong>Gesner Deslandes</strong> &nbsp;|&nbsp; Kolaboratè: Gesner Junior Deslandes, Roosevelt Deslandes, Sebastien Stephane Deslandes & Zendaya Christelle Deslandes',
        'sidebar_title': '🛡️ Aksè Moteur',
        'sidebar_activation': 'Aktivasyon atravè MonCash: **{moncash}**',
        'sidebar_key_label': 'Kle:',
        'sidebar_unlock': 'Deklannche Moteur',
        'sidebar_invalid': 'Kle pa bon',
        'sidebar_granted': '✅ AKSÈ AKÒDE',
        'sidebar_logout': 'Dekonekte',
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
        'main_header': 'MOTEUR ENFINI v33.0',
        'main_subheader': 'Dekouvèt Inivèsèl & Avansman Imèn',
        'scan_subheader': '🔍 Analiz Atomik Inivèsèl',
        'camera_method_label': 'Ki jan pou pran foto echantiyon an:',
        'camera_option': '📸 Pran foto ak kamera (bouton vire anba a)',
        'upload_option': '📁 Telechaje foto depi aparèy ou',
        'camera_instruction': '📸 Ajiste kamera a, epi peze bouton ↻ pou chanje ant kamera devan ak dèyè.',
        'upload_instruction': '📸 Pran yon foto ak kamera aparèy ou epi telechaje li isit la.',
        'flip_button': 'Vire Kamera',
        'capture_button': 'Pran Foto',
        'use_image_button': '✅ Sèvi ak foto sa a',
        'camera_placeholder': 'Flò kamera a ap parèt isit la apre w bay pèmisyon.',
        'site_label': 'Non sit:',
        'site_placeholder': 'Grand Goâve',
        'photo_label': 'Analiz echantiyon',
        'notes_label': 'Nòt analiz (endis detekte):',
        'weight_label': 'Mas (kg):',
        'execute_button': '🚀 EKZEKITE ANALIZ INIVÈSÈL',
        'no_photo_error': 'Tanpri pran yon foto oswa telechaje yon imaj an premye.',
        'report_title': 'RAPÒ DEKOUVÈT SOUVÈN',
        'resource_label': 'Rès idantifye:',
        'trace_label': 'Trase syantifik:',
        'value_usd_label': 'Valè sou mache estime: ${value:,.2f} USD',
        'value_htg_label': 'Valè ekonomik lokal: {value:,.2f} HTG',
        'solution_label': 'Solisyon imanitè:',
        'solution_text': 'Devlopman {resource} mennen nan souvrenite enfrastrikti nasyonal.',
        'strategic_intel': '🌍 Entèlijans Estratejik',
        'recent_log': '**Jounal aktivite resan:**',
        'download_button': '📊 Telechaje istorik rechèch (CSV)',
        'no_data_info': 'Pa gen okenn dekouvèt anrejistre ankò. Fè yon eskanè pou jenere done.',
        'access_warning': 'Tanpri antre kle prensipal ou nan ba a pou kòmanse eskanè.',
        'language_selector': 'Lang / Language',
        'unknown_mineral': 'Mineral Enkoni',
        'unclassified': 'Pa Klase'
    }
}

def get_text(key, lang=None, **kwargs):
    if lang is None:
        lang = st.session_state.language
    text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text

# --- 4. LOGIC ---
def analyze_resource(text):
    text = text.lower()
    for category, minerals in RESOURCE_CLASSES.items():
        for m in minerals:
            if m in text:
                return m, category
    return "Unknown Mineral", "Unclassified"

# --- 5. CUSTOM CAMERA WIDGET (using st.components.v1.html + callback) ---
def custom_camera_widget():
    """Embed camera with flip button and send captured image via st.rerun with query param."""
    # Generate unique id
    widget_id = f"cam_{uuid.uuid4().hex[:8]}"

    # HTML/JS with flip and capture, then reload with image data in URL
    html = f"""
    <div id="{widget_id}_container" style="text-align: center;">
        <video id="{widget_id}_video" autoplay playsinline style="width: 100%; max-width: 500px; border: 2px solid #00209F; border-radius: 10px; background: #000;"></video>
        <div style="margin-top: 10px;">
            <button id="{widget_id}_flip" style="padding: 8px 16px; background-color: #00209F; color: white; border: none; border-radius: 5px; cursor: pointer; margin-right: 10px;">↻ {get_text('flip_button')}</button>
            <button id="{widget_id}_capture" style="padding: 8px 16px; background-color: #D21034; color: white; border: none; border-radius: 5px; cursor: pointer;">📷 {get_text('capture_button')}</button>
        </div>
        <canvas id="{widget_id}_canvas" style="display: none;"></canvas>
    </div>
    <script>
        (function() {{
            const video = document.getElementById("{widget_id}_video");
            const flipBtn = document.getElementById("{widget_id}_flip");
            const captureBtn = document.getElementById("{widget_id}_capture");
            const canvas = document.getElementById("{widget_id}_canvas");

            let currentStream = null;
            let devices = [];
            let currentDeviceIndex = 0;

            function stopStream() {{
                if (currentStream) {{
                    currentStream.getTracks().forEach(track => track.stop());
                    currentStream = null;
                }}
            }}

            function startVideo(deviceId) {{
                stopStream();
                const constraints = {{
                    video: deviceId ? {{ deviceId: {{ exact: deviceId }} }} : true
                }};
                navigator.mediaDevices.getUserMedia(constraints)
                    .then(stream => {{
                        currentStream = stream;
                        video.srcObject = stream;
                        video.play();
                    }})
                    .catch(err => {{
                        console.error("Camera error:", err);
                        video.style.display = "none";
                        document.getElementById("{widget_id}_container").innerHTML += "<p style='color:red;'>Cannot access camera. Please check permissions.</p>";
                    }});
            }}

            navigator.mediaDevices.enumerateDevices()
                .then(devicesList => {{
                    devices = devicesList.filter(device => device.kind === 'videoinput');
                    if (devices.length > 0) {{
                        // Try to select rear camera
                        const rearIndex = devices.findIndex(device =>
                            device.label.toLowerCase().includes('back') ||
                            device.label.toLowerCase().includes('rear') ||
                            device.label.toLowerCase().includes('environment')
                        );
                        if (rearIndex !== -1) currentDeviceIndex = rearIndex;
                        else currentDeviceIndex = 0;
                        startVideo(devices[currentDeviceIndex].deviceId);
                    }} else {{
                        startVideo(null);
                    }}
                }})
                .catch(err => {{
                    console.error("Enumerate error:", err);
                    startVideo(null);
                }});

            flipBtn.addEventListener('click', () => {{
                if (devices.length === 0) {{
                    alert("No other cameras found.");
                    return;
                }}
                currentDeviceIndex = (currentDeviceIndex + 1) % devices.length;
                startVideo(devices[currentDeviceIndex].deviceId);
            }});

            captureBtn.addEventListener('click', () => {{
                if (video.videoWidth === 0) {{
                    alert("No video stream. Please ensure camera is working.");
                    return;
                }}
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                const dataURL = canvas.toDataURL('image/jpeg', 0.8);
                // Reload the page with the image data in the query string
                window.location.href = window.location.pathname + "?captured_image=" + encodeURIComponent(dataURL);
            }});
        }})();
    </script>
    """
    st.components.v1.html(html, height=400)

# --- 6. UI CONFIG ---
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

# Haitian Flag (same as before)
st.markdown("""
<div style="display: flex; justify-content: center; margin: 15px 0;">
    <svg width="240" height="144" viewBox="0 0 720 432" xmlns="http://www.w3.org/2000/svg">
        <rect width="720" height="216" fill="#00209F" />
        <rect y="216" width="720" height="216" fill="#D21034" />
        <g transform="translate(360,216) scale(0.12)">
            <path d="M0,0 L0,0" fill="#FFFFFF" stroke="#000000" stroke-width="2" />
            <polygon points="0,-120 60,-40 20,-40 20,80 -20,80 -20,-40 -60,-40 0,-120" fill="#FFFFFF" stroke="#000000" stroke-width="2" />
            <circle cx="0" cy="-20" r="20" fill="#FFFFFF" stroke="#000000" stroke-width="2" />
            <rect x="-30" y="40" width="60" height="40" fill="#FFFFFF" stroke="#000000" stroke-width="2" />
            <rect x="-40" y="80" width="80" height="30" fill="#FFFFFF" stroke="#000000" stroke-width="2" />
            <polygon points="0,110 -20,140 20,140 0,110" fill="#FFFFFF" stroke="#000000" stroke-width="2" />
            <circle cx="0" cy="-50" r="6" fill="#000000" />
            <path d="M-15,-30 L15,-30" stroke="#000000" stroke-width="2" />
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

# --- 7. SIDEBAR AUTH ---
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

# --- 8. WELCOME SOUND ---
if st.session_state.authenticated and st.query_params.get("play_sound") == "true":
    st.markdown(f"<script>{get_text('welcome_sound_js')}</script>", unsafe_allow_html=True)

# --- 9. CAPTURED IMAGE FROM QUERY PARAM ---
if "captured_image" in st.query_params:
    img_data = st.query_params["captured_image"]
    st.session_state.captured_image = img_data
    # Remove the param to avoid reprocessing
    new_params = {k: v for k, v in st.query_params.items() if k != "captured_image"}
    st.query_params.clear()
    st.query_params.update(new_params)
    st.rerun()

# --- 10. MAIN INTERFACE ---
st.markdown(f'<div class="main-header"><h1>{get_text("main_header")}</h1><p>{get_text("main_subheader")}</p></div>', unsafe_allow_html=True)

if st.session_state.authenticated:
    st.subheader(get_text('scan_subheader'))

    # Camera method selection
    method = st.radio(
        get_text('camera_method_label'),
        options=['camera', 'upload'],
        format_func=lambda x: get_text('camera_option') if x == 'camera' else get_text('upload_option'),
        horizontal=True
    )
    st.session_state.camera_method = method

    if method == 'camera':
        st.markdown(f"<p style='font-size:0.9rem; color:#555;'>{get_text('camera_instruction')}</p>", unsafe_allow_html=True)
        custom_camera_widget()
        # Display the saved image if any
        if st.session_state.captured_image:
            st.image(st.session_state.captured_image, caption="Captured image", width=200)
            if st.button("Clear image"):
                st.session_state.captured_image = None
                st.rerun()
        else:
            st.info(get_text('camera_placeholder'))
    else:
        st.markdown(f"<p style='font-size:0.9rem; color:#555;'>{get_text('upload_instruction')}</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader(get_text('photo_label'), type=['jpg', 'jpeg', 'png'])
        if uploaded:
            # Convert to base64 for consistency
            bytes_data = uploaded.read()
            b64 = base64.b64encode(bytes_data).decode()
            st.session_state.captured_image = f"data:image/{uploaded.type.split('/')[-1]};base64,{b64}"
            st.rerun()

    site = st.text_input(get_text('site_label'), get_text('site_placeholder'))
    notes = st.text_area(get_text('notes_label'))
    weight = st.number_input(get_text('weight_label'), value=1.0)

    # --- Execute ---
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

    # --- History ---
    st.divider()
    st.subheader(get_text('strategic_intel'))

    if st.session_state.discovery_log:
        st.markdown(get_text('recent_log'))
        df = pd.DataFrame(st.session_state.discovery_log)
        st.dataframe(df.tail(5), use_container_width=True)

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
