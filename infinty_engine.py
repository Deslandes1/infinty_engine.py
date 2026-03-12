import streamlit as st
import datetime
import uuid
import json
from fpdf import FPDF # Nouvelle bibliothèque pour le PDF

# --- FONCTION DE GÉNÉRATION PDF ---
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # En-tête du Rapport
    pdf.set_fill_color(0, 32, 159) # Bleu Marine
    pdf.rect(0, 0, 210, 40, 'F')
    
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 20, "INFINITY ENGINE v33.0", ln=True, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "RAPPORT DE DÉCOUVERTE SOUVERAINE", ln=True, align='C')
    
    pdf.ln(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 14)
    
    # Contenu du Rapport
    pdf.cell(0, 10, f"ID du Rapport : {data['id']}", ln=True)
    pdf.cell(0, 10, f"Date de l'Analyse : {data['date']}", ln=True)
    pdf.cell(0, 10, f"Site de Prélèvement : {data['site']}", ln=True)
    pdf.ln(5)
    
    pdf.set_draw_color(210, 16, 52) # Rouge
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Ressource Identifiée : {data['res'].upper()}", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, f"Catégorie : {data['cat'].upper()}")
    pdf.multi_cell(0, 10, f"Masse Analysée : {data['weight']} kg")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 128, 0) # Vert pour la valeur
    pdf.cell(0, 10, f"Valeur Marchande Estimée : ${data['usd']:,.2f} USD", ln=True)
    pdf.set_text_color(0, 32, 159) # Bleu pour la monnaie locale
    pdf.cell(0, 10, f"Valeur Économique Locale : {data['htg']:,.2f} HTG", ln=True)
    
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, f"Note de Souveraineté : Le développement du {data['res']} est un pilier pour l'infrastructure nationale.")
    
    return pdf.output(dest='S') # Retourne le PDF sous forme de bytes

# --- (Insérez ici le reste de votre code précédent : MARKET_HUB, RESOURCE_CLASSES, etc.) ---

# Dans la section de l'interface (col1), après l'affichage du rapport HTML :
# Ajoutez ce bloc juste après 'st.markdown(f""" <div class="report-card"> ...'

# Préparation des données pour le PDF
report_data = {
    "id": rep_id,
    "date": str(datetime.date.today()),
    "site": site,
    "res": res_name,
    "cat": res_cat,
    "weight": weight,
    "usd": usd_val,
    "htg": htg_val
}

# Bouton de téléchargement PDF
pdf_bytes = generate_pdf(report_data)
st.download_button(
    label="📥 Télécharger le Rapport Officiel (PDF)",
    data=pdf_bytes,
    file_name=f"Rapport_{rep_id}.pdf",
    mime="application/pdf"
)
        


