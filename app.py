import io
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN MAESTRA Y ELIMINACIÓN DE LOS CUADROS BLANCOS FANTASMA
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Remoción absoluta de los tres niveles de headers y contenedores de columnas
st.markdown("""
<style>
    /* 1. Eliminar por completo la cabecera nativa y el espacio muerto superior */
    [data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    div.block-container {
        padding-top: 0rem !important;
    }
    
    /* 2. ASESINO DE LOS DOS RECUADROS BLANCOS EN COLUMNAS */
    [data-testid="stColumn"] {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    
    /* 3. BARRA LATERAL (Color Oscuro Corporativo Original) */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important;
    }
    
    /* 4. BLINDAJE DEL BANNER */
    button[title="View fullscreen"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stImage"] img {
        pointer-events: none !important;
        user-select: none !important;
    }

    /* 5. Tarjetas Ejecutivas */
    .executive-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-top: 0px; 
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# GENERACIÓN DE BUFFER DE ARCHIVO COMPATIBLE (PDF COMPILADO EN MEMORIA)
# ==============================================================================
buffer_pdf = io.BytesIO()
buffer_pdf.write(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Count 1/Kids[3 0 R]>>\nendobj\n3 0 obj\n<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 55>>\nstream\nBT\n/F1 12 Tf\n72 712 Td\n(MethylOx Institutional Analytical Dossier - Protected Content) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000015 00000 n\n0000000068 00000 n\n0000000120 00000 n\n0000000219 00000 n\ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n326\n%%EOF")
pdf_data = buffer_pdf.getvalue()

# ==============================================================================
# BARRA LATERAL (DISEÑO PREMIUM ORIGINAL CORREGIDO)
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 0px; border-bottom: 1px solid #1E293B; margin-bottom: 20px;">
    <h3 style="margin: 0; color: #FFFFFF !important; font-weight: 900; font-size: 22px; letter-spacing: -0.5px;">MethylOx™</h3>
    <p style="margin: 0; color: #38BDF8 !important; font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">Epigenetic AI Platform</p>
</div>
""", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "Navegación del Sistema",
    ["Dashboard Matrix", "Samples Database", "AI Analysis Hub", "Clinical Reports", "System Settings"],
    label_visibility="collapsed"
)

st.sidebar.write("##")

# Corregido el cierre lógico de las condicionales internas del Sidebar
if nav_selection == "Dashboard Matrix":
    st.sidebar.markdown('<p style="font-size:11px; font-weight:700; color:#94A3B8 !important; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px;">Monitor de Canales Activos</p>', unsafe_allow_html=True)
    slider_ch1 = st.sidebar.slider("Canal Ómico CH-01", 0.0, 1.0, 0.45)
    slider_ch2 = st.sidebar.slider("Canal Ómico CH-02", 0.0, 1.0, 0.62)
    slider_ch3 = st.sidebar.slider("Canal Ómico CH-03", 0.0, 1.0, 0.18)

st.sidebar.markdown("
