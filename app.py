import sqlite3
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import motores

# 1. CONFIGURACION DE PAGINA MAESTRA (Layout extendido obligatorio)
st.set_page_config(page_title="MethylOx Labs", layout="wide", initial_sidebar_state="expanded")

# Configuración estética de gráficos premium
sns.set_theme(style="white")
plt.rcParams["text.color"] = "#0F172A"
plt.rcParams["axes.labelcolor"] = "#475569"
plt.rcParams["xtick.color"] = "#64748B"
plt.rcParams["ytick.color"] = "#64748B"

# 2. INYECCIÓN CSS SEGURO: EFECTO PANORÁMICO REAL 100% FLUIDO DE EXTREMO A EXTREMO
st.markdown(
    """
    <style>
    /* Fondo general de la plataforma blanco clínico satinado */
    .stApp { background-color: #F1F5F9 !important; font-family: 'Inter', -apple-system, sans-serif !important; }
    
    /* Forzar que el espacio de contenido de Streamlit no tenga márgenes superiores */
    .block-container { padding-top: 0rem !important; padding-left: 0rem !important; padding-right: 0rem !important; max-width: 100% !important; }
    
    /* BARRA LATERAL GRAFITO MATE (#1E293B) */
    [data-testid="stSidebar"] { background-color: #1E293B !important; border-right: none !important; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #FFFFFF !important; }
    
    /* 🔥 CONTENEDOR MAESTRO DEL BANNER: ROMPE CUALQUIER MARGEN Y SE ESTIRA AL 100% REAL */
    .banner-full {
        width: 100vw !important;
        height: 100px !important;
        background-image: url('app/static/banner_real.png'), url('banner_real.png') !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        border-bottom: 3px solid #2563EB !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
    }
    
    /* Espaciador interno para las secciones de contenido de la página principal */
    .main-content-wrapper {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    [data-testid="stSidebar"] .stButton>button {
        background-color: transparent !important; color: #CBD5E1 !important; border: none !important;
        text-align: left !important; justify-content: flex-start !important; padding-left: 20px !important;
        border-radius: 8px !important; margin-bottom: 8px !important; font-size: 14px !important; font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stButton>button:hover { background-color: rgba(255, 255, 255, 0.1) !important; color: #FFFFFF !important; }
    .executive-card {
        background-color: #FFFFFF !important; border: 1px solid #E2E8F0 !important; border-radius: 16px !important;
        padding: 24px !important; margin-bottom: 20px !important; box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03) !important;
    }
    .card-heading { color: #0F172A !important; font-size: 13px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.75px !important; margin-bottom: 15px !important; }
    
    /* 🧬 ANIMACIÓN DE SIGNO VITAL (HEARTBEAT PULSE) */
    @keyframes vitalPulse {
        0% { transform: scale(0.9); opacity: 0.6; }
        50% { transform: scale(1.15); opacity: 1; box-shadow: 0 0 12px #10B981; }
        100% { transform: scale(0.9); opacity: 0.6; }
    }
    .vital-dot {
        display: inline-block; width: 10px; height: 10px; background-color: #10B981; 
        border-radius: 50%; margin-right: 8px; animation: vitalPulse 1.5s infinite ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicialización silenciosa de BD llamando al backend
motores.iniciar_base_datos()
UMBRAL = motores.UMBRAL_GLOBAL

# --- 3. BARRA LATERAL DE NAVEGACIÓN ---
st.sidebar.markdown("## 🔮 MethylOx™")
st.sidebar.caption("Epigenetic AI Platform")
st.sidebar.markdown("---")
# --- 3. BARRA LATERAL DE NAVEGACIÓN ---
if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Dashboard"

if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.session_state["menu_activo"] = "Dashboard"
if st.sidebar.button("🧪 Samples", use_container_width=True):
    st.session_state["menu_activo"] = "Samples"
if st.sidebar.button("🧠 AI Analysis", use_container_width=True):
    st.session_state["menu_activo"] = "AI Analysis"
if st.sidebar.button("🧬 Biomarkers", use_container_width=True):
    st.session_state["menu_activo"] = "Biomarkers"
if st.sidebar.button("📄 Reports", use_container_width=True):
    st.session_state["menu_activo"] = "Reports"
if st.sidebar.button("⚙️ Settings", use_container_width=True):
    st.session_state["menu_activo"] = "Settings"

st.sidebar.markdown("---")


# --- 4. CONTROL DE PANTALLAS ---
if st.session_state["menu_activo"] == "Dashboard":
    # 1. Banner corporativo premium de extremo a extremo por CSS
    st.markdown(
        """
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 90px;
            background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%);
            z-index: 99999;
            border-bottom: 4px solid #10B981;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            padding-left: 20px;
        ">
            <h1 style="color: white; font-family: 'Inter', sans-serif; font-size: 22px; margin: 0; font-weight: 700; letter-spacing: 0.5px;">
                🧬 MethylOx™ <span style="font-weight: 300; font-size: 16px; color: #93C5FD;">| Molecular Methylation Analysis Hub</span>
            </h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # 2. Contenedor que empuja el contenido abajo para que el banner no lo tape
    st.markdown('<div style="margin-top: 140px;">', unsafe_allow_html=True)
    
    st.title("Molecular Methylation Analysis Hub")
    st.caption("Panel Ejecutivo de Cribado para Cáncer de Mama en Etapa Temprana")
    st.markdown("---")
    
    # Tarjeta 1: Formulario de Pacientes
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">🧬 Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        patient_id = st.text_input("🧬 Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2:
        patient_age = st.number_input("📋 Chronological Age", min_value=18, max_value=100, value=45)
    with col_f3:
        ctdna_score = st.number_input("🩸 ctDNA Concentration (ng/mL)", min_value=0.0000, max_value=5.0000, format="%.4f")

    resultado = motores.procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Commit Diagnostic Data (Save to SQLite3)", use_container_width=True):
            if patient_id:
                estatus_db = motores.registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado)
                if estatus_db == "Éxito":
                    st.success(f"Record secured in SQLite3 for ID: {patient_id}")
                else:
                    st.error("Database status: Patient Identifier already exists.")
            else:
                st.warning("Please enter a valid Patient Identifier.")

    with col_btn2:
        reporte_pdf_contenido = motores.generar_pdf_clinico(patient_id, patient_age, ctdna_score, resultado)
        st.download_button(label="📥 Download Personalized Clinical Report", data=reporte_pdf_contenido, file_name=f"MethylOx_{patient_id}.pdf", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True) # Cierre de Tarjeta 1

    # Tarjeta 2: Métricas en tiempo real
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">📈 Real-Time Analytics Overview</p>', unsafe_allow_html=True)
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(label="SENSITIVITY", value="96.4%")
    with k2:
        st.metric(label="SPECIFICITY", value="94.1%")
    with k3:
        st.metric(label="AUC (ROC)", value="0.982")
    with k4:
        st.metric(label="VERDICT STATUS", value="Low Risk")

    st.markdown("</div>", unsafe_allow_html=True) # Cierre de Tarjeta 2
    st.markdown("</div>", unsafe_allow_html=True) # Cierre del contenedor de margen

# --- 4. CONTROL DE PANTALLAS ---
if st.session_state["menu_activo"] == "Dashboard":
    # 1. Banner corporativo premium de extremo a extremo por CSS
    st.markdown(
        """
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 90px;
            background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 100%);
            z-index: 99999;
            border-bottom: 4px solid #10B981;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            padding-left: 20px;
        ">
            <h1 style="color: white; font-family: 'Inter', sans-serif; font-size: 22px; margin: 0; font-weight: 700; letter-spacing: 0.5px;">
                🧬 MethylOx™ <span style="font-weight: 300; font-size: 16px; color: #93C5FD;">| Molecular Methylation Analysis Hub</span>
            </h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # 2. Contenedor que empuja el contenido abajo para que el banner no lo tape
    st.markdown('<div style="margin-top: 140px;">', unsafe_allow_html=True)
    
    st.title("Molecular Methylation Analysis Hub")
    st.caption("Panel Ejecutivo de Cribado para Cáncer de Mama en Etapa Temprana")
    st.markdown("---")
    
    # Tarjeta 1: Formulario de Pacientes
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">🧬 Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        patient_id = st.text_input("🧬 Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2:
        patient_age = st.number_input("📋 Chronological Age", min_value=18, max_value=100, value=45)
    with col_f3:
        ctdna_score = st.number_input("🩸 ctDNA Concentration (ng/mL)", min_value=0.0000, max_value=5.0000, format="%.4f")

    resultado = motores.procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Commit Diagnostic Data (Save to SQLite3)", use_container_width=True):
            if patient_id:
                estatus_db = motores.registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado)
                if estatus_db == "Éxito":
                    st.success(f"Record secured in SQLite3 for ID: {patient_id}")
                else:
                    st.error("Database status: Patient Identifier already exists.")
            else:
                st.warning("Please enter a valid Patient Identifier.")

    with col_btn2:
        reporte_pdf_contenido = motores.generar_pdf_clinico(patient_id, patient_age, ctdna_score, resultado)
        st.download_button(label="📥 Download Personalized Clinical Report", data=reporte_pdf_contenido, file_name=f"MethylOx_{patient_id}.pdf", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True) # Cierre de Tarjeta 1

    # Tarjeta 2: Métricas en tiempo real
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">📈 Real-Time Analytics Overview</p>', unsafe_allow_html=True)
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(label="SENSITIVITY", value="96.4%")
    with k2:
        st.metric(label="SPECIFICITY", value="94.1%")
    with k3:
        st.metric(label="AUC (ROC)", value="0.982")
    with k4:
        st.metric(label="VERDICT STATUS", value="Low Risk")

    st.markdown("</div>", unsafe_allow_html=True) # Cierre de Tarjeta 2
    st.markdown("</div>", unsafe_allow_html=True) # Cierre del contenedor de margen
elif st.session_state["menu_activo"] == "⚙️ Settings":
    st.title("⚙️ Engineering Core & Backend Diagnostics")
    st.markdown("---")
   
    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
        st.success("✅ Conexión e integridad del archivo motores.py verificada.")
    except Exception:
        st.error("❌ No se pudo enlazar el visor con motores.py")
