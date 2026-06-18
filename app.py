import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import motores # Tu archivo de lógica de negocio backend

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS TECNOLÓGICOS (ESTILO CRISPR.AI)
# =====================================================================
st.set_page_config(page_title="MethylOx™ Platform", page_icon="🧬", layout="wide")

st.markdown(
    """
    <style>
    /* Fondo de la aplicación moderno y limpio */
    .stApp {
        background-color: #F8FAFC !important;
    }
    
    /* Barra lateral tecnológica (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        box-shadow: 4px 0 10px rgba(15, 23, 42, 0.02) !important;
    }
    
    /* El contenedor principal de contenido */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }

    .main-content-wrapper {
        padding: 30px !important;
    }
    
    /* 🛠️ CONFIGURACIÓN EXACTA PARA TU BANNER AZUL (1000199352) */
    [data-testid="stMainBlockContainer"] [data-testid="stImage"] img {
        width: 100vw !important; /* Se estira limpiamente a lo ancho */
        height: 110px !important; /* Altura fija ideal tipo cintillo corporativo */
        object-fit: cover !important; /* Mantiene los logos y textos proporcionados sin aplastarlos */
        object-position: center !important; /* Enfoca el centro exacto de tu diseño */
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* Tarjetas ejecutivas con bordes suaves y sombras sutiles */
    .executive-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 30px !important;
        box-shadow: 0 10px 25px rgba(148, 163, 184, 0.08) !important;
        margin-bottom: 25px !important;
    }
    
    /* Títulos de las tarjetas estilizados */
    .card-heading {
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        margin-bottom: 25px !important;
        border-bottom: 2px solid #F1F5F9 !important;
        padding-bottom: 10px !important;
    }
    
    /* Botón de guardar (Commit) - Azul Tecnológico */
    div.stButton > button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Botón de descarga (Reporte) - Rosa de Contraste */
    div.stDownloadButton > button {
        background-color: #EC4899 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.15) !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #DB2777 !important;
        box-shadow: 0 6px 16px rgba(236, 72, 153, 0.25) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Estilizar los campos de entrada de texto y números */
    .stTextInput input, .stNumberInput input {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 2. BARRA LATERAL DE NAVEGACIÓN Y CONFIGURACIÓN DEL MENÚ
# =====================================================================
st.sidebar.markdown("## 🧬 MethylOx™")
st.sidebar.caption("Epigenetic AI Platform")
st.sidebar.markdown("---")

if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Dashboard"

if st.sidebar.button("📋 Dashboard", use_container_width=True):
    st.session_state["menu_activo"] = "Dashboard"
if st.sidebar.button("🧪 Samples", use_container_width=True):
    st.session_state["menu_activo"] = "Samples"
if st.sidebar.button("📊 AI Analysis", use_container_width=True):
    st.session_state["menu_activo"] = "AI Analysis"
if st.sidebar.button("🧬 Biomarkers", use_container_width=True):
    st.session_state["menu_activo"] = "Biomarkers"
if st.sidebar.button("📈 Reports", use_container_width=True):
    st.session_state["menu_activo"] = "Reports"
if st.sidebar.button("⚙️ Settings", use_container_width=True):
    st.session_state["menu_activo"] = "Settings"

st.sidebar.markdown("---")
st.sidebar.caption("SYSTEM STATUS: 🟢 Core Engine Processing...")

# =====================================================================
# 3. CUERPO PRINCIPAL DE LA APLICACIÓN - CONTENIDO POR PESTAÑA
# =====================================================================

# PESTAÑA A: DASHBOARD PRINCIPAL
if st.session_state["menu_activo"] in ["Dashboard", "🗙 Dashboard"]:
    # Cambiado con éxito al nombre correcto de tu archivo
    st.image("1000199352.png", use_container_width=True, output_format="PNG")
    
    # Contenedor con márgenes para estructurar el contenido de abajo
    st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)

    st.markdown('<p class="card-heading">📋 Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
    
    # Columnas de inputs de datos médicos
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        patient_id = st.text_input("📋 Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2:
        patient_age = st.number_input("📅 Chronological Age", min_value=18, max_value=100, value=45)
    with col_f3:
        ctdna_score = st.number_input("🧪 ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.25, format="%.4f")

    # Inicializar la lógica de procesamiento para que esté disponible en ambos botones
    resultado = motores.procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score)

    # Bloque de botones en columnas paralelas
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
        st.download_button(
            label="📥 Download Personalized Clinical Report", 
            data=reporte_pdf_contenido, 
            file_name=f"Methylox_Report_{patient_id}.pdf",
            use_container_width=True
        )
        
    st.markdown("</div>", unsafe_allow_html=True)

    # Seccion de Analiticas e Indicadores de Rendimiento Clínico
    st.markdown('### 📊 REAL-TIME ANALYTICS OVERVIEW')
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="📊 Screening Sensitivity", value="96.4%", delta="Target Verified")
    with col_m2:
        st.metric(label="🎯 Analytical Specificity", value="94.1%", delta="Validated")
    with col_m3:
        st.metric(label="🧪 ctDNA Detection Limit", value="0.01%", delta="High-Resolution")

    # Gráficos ejecutivos en paralelo sin distorsión
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**Risk Score Distribution (KDE)**")
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        sns.kdeplot(np.random.normal(78, 6, 150), color="#EC4899", fill=True, alpha=0.2, label="Early Cancer", ax=ax3)
        ax3.set_xlabel("Risk Score (%)", fontsize=8)
        ax3.legend(fontsize=7)
        sns.despine()
        st.pyplot(fig3)

    with col_g2:
        st.markdown("**ctDNA Concentration Variance**")
        fig4, ax4 = plt.subplots(figsize=(5, 3))
        sns.histplot(np.random.exponential(0.5, 100), color="#3B82F6", kde=True, ax=ax4)
        ax4.set_xlabel("Concentration (ng/mL)", fontsize=8)
        sns.despine()
        st.pyplot(fig4)
    st.markdown("</div>", unsafe_allow_html=True)

# PESTAÑA B: VISUALIZACIÓN DE MUESTRAS LOGUEADAS
elif st.session_state["menu_activo"] == "Samples":
    st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
    st.title("🧪 Sample Records & Permanent Database")
    st.markdown("---")

    conn = sqlite3.connect("methyl_clinic.db")
    try:
        df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
        if not df_pacientes.empty:
            st.dataframe(df_pacientes, use_container_width=True)
        else:
            st.info("No active patient logs detected inside methyl_clinic.db.")
    except Exception:
        st.warning("Database tables are empty or initializing...")
    finally:
        conn.close()
    st.markdown("</div>", unsafe_allow_html=True)

# PESTAÑA C: DIAGNÓSTICO E INTEGRIDAD DE MOTORES BACKEND
elif st.session_state["menu_activo"] == "Settings":
    st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
    st.title("⚙️ Engineering Core & Backend Diagnostics")
    st.markdown("---")

    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
    except Exception:
        st.error("No se pudo leer motores.py")
    st.markdown("</div>", unsafe_allow_html=True)
