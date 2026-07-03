import io
import os
import sqlite3
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from fpdf import FPDF

# ==============================================================================
# 📊 CONFIGURACIÓN GENERAL E IDENTIDAD VISUAL EXECUTIVE DE ALTA GAMA
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™ | Epigenetic AI Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #F8FAFC !important; font-family: sans-serif !important; }
    [data-testid="stSidebar"] { background-color: #0B0F19 !important; }
    .executive-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 30px !important;
        margin-top: 20px !important;
    }
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #0284C7, #00B4D8) !important;
        color: white !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

if "historical_database" not in st.session_state:
    st.session_state["historical_database"] = pd.DataFrame(columns=['Timestamp', 'Patient ID', 'Age (Years)', 'ctDNA (ng/mL)', 'Clinical Status'])

# ==============================================================================
# BARRA LATERAL
# ==============================================================================
access_key = st.sidebar.text_input("Llave de Acceso", type="password")

if access_key == "METHYLOX-ROOT-2026":
    nav_selection = st.sidebar.radio("Navegación", ["Dashboard Matrix", "Samples Database"])
    token_hospital = "ROOT-INTERNAL"
else:
    nav_selection = "Lock"
    token_hospital = None

# ==============================================================================
# DASHBOARD
# ==============================================================================
if nav_selection == "Dashboard Matrix":
    col_izquierda, col_derecha = st.columns([1, 1], gap="large")
    
    with col_izquierda:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown('<h3>📝 Patient Case Enrollment</h3>', unsafe_allow_html=True)
        patient_id = st.text_input("Patient Identifier")
        patient_age = st.number_input("Age", 18, 100, 45)
        ctdna_score = st.number_input("ctDNA (ng/mL)", 0.0, 5.0, 0.25)
        if st.button("🚀 Analyze"):
            st.success("Análisis procesado")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_derecha:
        # Aquí eliminamos el 'with st.container(border=True)' que causaba el recuadro 
        # y mantenemos el contenido directamente alineado bajo el 'with'
        st.markdown('<p style="font-size: 15px; font-weight:700; color:#0F172A;">📊 Cohort Density Mapping</p>', unsafe_allow_html=True)
        
        x_axis = np.linspace(0.0, 1.0, 100)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_axis, y=np.exp(-((x_axis - 0.45) ** 2) / 0.05), fill='tozeroy'))
        fig.update_layout(height=260, margin=dict(l=0, r=0, t=10, b=10), plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

        st.write("---")
        st.markdown('<p style="font-size: 13px; font-weight:700;">📥 Data Ingestion</p>', unsafe_allow_html=True)
        st.file_uploader("Upload sequencer", type=["csv", "xlsx"], label_visibility="collapsed")
        
elif nav_selection == "Lock":
    st.warning("🔒 Acceso Restringido: Ingrese credenciales.")
