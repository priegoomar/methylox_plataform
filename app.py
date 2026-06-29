import io
import os
import sqlite3  # <- AGREGADO PARA TU BASE DE DATOS
from datetime import datetime  # <- AGREGADO PARA LAS MARCAS DE TIEMPO
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN MAESTRA Y ESTILIZACIÓN DE LA PLATAFORMA
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar bases de datos históricas en memoria si no existen
if "historical_database" not in st.session_state:
    st.session_state["historical_database"] = pd.DataFrame(columns=['Patient ID', 'Age (Years)', 'ctDNA (ng/mL)', 'Clinical Status', 'Timestamp'])

# Inyección de CSS de Alta Fidelidad para los botones de la barra lateral
st.markdown("""
<style>
    /* 1. Fondo de la aplicación */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* 2. Reset de cabeceras y márgenes superiores */
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
    
    /* 3. BARRA LATERAL - FONDO OSCURO */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 2px solid #1E293B;
    }

    /* CONTENEDOR DE NUESTROS BOTONES CUSTOM ULTRA-VISIBLES */
    .custom-nav-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding: 0px 10px;
    }

    /* Sliders de la barra lateral */
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important;
        font-size: 12px !important;
    }

    /* 4. PROTECCIÓN DEL BANNER */
    button[title="View fullscreen"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stImage"] img {
        pointer-events: none !important;
        user-select: none !important;
        border-radius: 0px 0px 12px 12px !important;
    }

    /* 5. TARJETAS DE CONTENIDO PRINCIPAL */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
        margin-top: 15px !important;
        padding: 6px !important;
    }

    /* 6. BOTONES DE ACCIÓN */
    div.stButton > button:first-child {
        background-color: #0284C7 !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #0369A1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# GENERACIÓN DE BUFFER DE ARCHIVO COMPATIBLE (PDF EN MEMORIA)
# ==============================================================================
buffer_pdf = io.BytesIO()
buffer_pdf.write(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<<Type/Catalog/Pages 2 0 R>>>\nendobj\n2 0 obj\n<<<Type/Pages/Count 1/Kids[3 0 R]>>>\nendobj\n3 0 obj\n<<<Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>>\nendobj\n4 0 obj\n<not a legal valueLength 55>>\nstream\nBT\n/F1 12 Tf\n72 712 Td\n(MethylOx Institutional Analytical Dossier - Protected Content) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000015 00000 n\n0000000068 00000 n\n0000000120 00000 n\n0000000219 00000 n\ntrailer\n<<\n/Size 5/Root 1 0 R>>>\nstartxref\n326\n%%EOF")
pdf_data = buffer_pdf.getvalue()

# ==============================================================================
# BARRA LATERAL (BRANDING CORPORATIVO REFORZADO)
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 10px; border-bottom: 1px solid #1E293B; margin-bottom: 25px;">
    <h3 style="margin: 0; color: #FFFFFF !important; font-weight: 900; font-size: 22px; letter-spacing: -0.5px;">MethylOx™</h3>
    <p style="margin: 0; color: #38BDF8 !important; font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">Epigenetic AI Platform</p>
</div>
""", unsafe_allow_html=True)

if "nav_selection" not in st.session_state:
    st.session_state.nav_selection = "Dashboard Matrix"

st.sidebar.markdown('<div class="custom-nav-container">', unsafe_allow_html=True)

col_b1 = st.sidebar.button("📊 Dashboard Matrix", use_container_width=True)
col_b2 = st.sidebar.button("🗄️ Samples Database", use_container_width=True)
col_b3 = st.sidebar.button("🧠 AI Analysis Hub", use_container_width=True)
col_b4 = st.sidebar.button("📋 Clinical Reports", use_container_width=True)
col_b5 = st.sidebar.button("⚙️ System Settings", use_container_width=True)

if col_b1: st.session_state.nav_selection =
