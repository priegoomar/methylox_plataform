# app.py - FRONTEND PRESET: THEME BIOTECH CLEANROOM
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importación de la capa analítica pura
from motores import (
    iniciar_base_datos,
    procesar_diagnostico_clinico,
    registrar_paciente_db,
    ejecutar_motores_crispr_unificados,
    UMBRAL_GLOBAL
)

# 1. CONFIGURACION DE PAGINA MAESTRA
st.set_page_config(
    page_title="MethylOx Labs",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INYECCIÓN CSS: TEMÁTICA PRESET PREMIUM (Blanco & Azul Eléctrico)
st.markdown(
    """
    <style>
    /* Fondo maestro blanco y tipografía de laboratorio */
    .stApp {
        background-color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    /* Barra lateral limpia color blanco/gris clínico */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    /* Estilización de textos en la barra lateral */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h2 {
        color: #0F172A !important;
    }
    /* Botones de navegación integrados estilo menú clínico */
    [data-testid="stSidebar"] .stButton>button {
        background-color: #FFFFFF !important;
        color: #2563EB !important;
        border: 1px solid #E2E8F0 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 15px !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    }
    /* Efecto hover interactivo */
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-color: #2563EB !important;
    }
    /* Tarjetas modulares de datos tipo dashboard de la imagen */
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #F1F5F9;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicialización silenciosa de SQLite3
iniciar_base_datos()

# --- 3. BARRA LATERAL IZQUIERDA DE NAVEGACIÓN ---
st.sidebar.markdown("## 🔬 MethylOx Labs")
st.sidebar.markdown("`CLINICAL PLATFORM v4.0`")
st.sidebar.markdown("---")

if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "🏠 Dashboard"

if st.sidebar.button("🏠 Dashboard", use_container_width=True): st.session_state["menu_activo"] = "🏠 Dashboard"
if st.sidebar.button("👤 Patient Profiles", use_container_width=True): st.session_state["menu_activo"] = "👤 Patient Profiles"
if st.sidebar.button("📊 Methylation Matrix", use_container_width=True): st.session_state["menu_activo"] = "📊 Methylation Matrix"
if st.sidebar.button("🧬 CRISPR Guide Library", use_container_width=True): st.session_state["menu_activo"] = "🧬 CRISPR Guide Library"
if st.sidebar.button("🧪 Gel Analysis", use_container_width=True): st.session_state["menu_activo"] = "🧪 Gel Analysis"
if st.sidebar.button("📄 Reports", use_container_width=True): st.session_state["menu_activo"] = "📄 Reports"
if st.sidebar.button("⚙️ Settings", use_container_width=True): st.session_state["menu_activo"] = "⚙️ Settings"
st.sidebar.markdown("---")
if st.sidebar.button("🟢 Platform Status\n● Active Connection", use_container_width=True):
    st.sidebar.toast("Enlace de datos en línea.")

# --- 4. CONTROL DE PANTALLAS (FRONTEND LIMPIO) ---

if st.session_state["menu_activo"] == "🏠 Dashboard":
    st.image("banner_real.png", width=420)
    st.title("Molecular Methylation Analysis Hub")
    st.caption("Early Detection Through Epigenetic AI | Automated Screening Platform")
    st.markdown("---")
    
    st.markdown("#### 📥 Patient Enrollment Matrix")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1: patient_id = st.text_input("🆔 Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2: patient_age = st.number_input("🎂 Chronological Age", min_value=18, max_value=100, value=45)
    with col_f3: ctdna_score = st.number_input("🔬 ctDNA Concentration (ng/mL)", min_value=0.0000, max_value=5.0000, format="%.4f", value=0.2500)
    
    resultado = procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score)
        
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Commit Diagnostic Data", use_container_width=True):
            if patient_id:
                estatus_db = registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado)
                if estatus_db == "Éxito": st.success(f"Record verified for ID: {patient_id}")
                else: st.error("Database conflict: ID already exists.")
            else: st.warning("Invalid credentials.")
                
    with col_btn2:
        reporte_txt = f"METHYLOX CLINICAL EXCERPT\nID: {patient_id}\nAge: {patient_age}\nScore: {ctdna_score:.4f}\nVerdict: {resultado}"
        st.download_button("📥 Export Prognostic Report (.TXT)", data=reporte_txt, file_name=f"Report_{patient_id}.txt", use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📊 Real-Time Analytics Overview")
    c_tar1, c_tar2, c_tar3 = st.columns(3)
    with c_tar1: st.metric(label="Clinical Cohort Status", value="Stage I Breast Cancer" if patient_id else "Awaiting Input")
    with c_tar2: st.metric(label="Global Methylation Value", value=f"{ctdna_score:.4f} ng/mL")
    with c_tar3: st.metric(label="Diagnostic Verdict", value=resultado)

elif st.session_state["menu_activo"] == "👤 Patient Profiles":
    st.title("👤 Patient Profiles & Clinical Records")
    st.markdown("---")
    import sqlite3
    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    if not df_pacientes.empty: st.dataframe(df_pacientes, use_container_width=True)
    else: st.info("No active logs stored in SQLite3.")

elif st.session_state["menu_activo"] == "🧬 CRISPR Guide Library":
    st.title("🧬 CRISPR Guide Library & Screening")
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload core genomic logs / raw database files")
    if uploaded_file is not None:
        try:
            nombre = uploaded_file.name
            df_secuencias = pd.read_excel(uploaded_file) if nombre.endswith(('.xlsx', '.xls')) else pd.read_csv(uploaded_file, sep='\t' if nombre.endswith(('.tsv', '.txt')) else ',')
            df_guias_nuevas = ejecutar_motores_crispr_unificados(df_secuencias)
            st.success(f"Screening complete: {len(df_guias_nuevas)} high-affinity guides isolated.")
            st.dataframe(df_guias_nuevas, use_container_width=True)
        except Exception:
            st.error("Execution error: Invalid matrix mapping structure.")
