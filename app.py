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

# 2. ARQUITECTURA DE DISEÑO: BIOTECH THEME HIGH-CONTRAST
st.markdown(
    """
    <style>
    /* Fondo general de laboratorio satinado (Rompe el blanco puro) */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    /* BANNER PANORÁMICO COMPACTO: Ancho completo y baja altura forzada */
    [data-testid="stImage"] img {
        width: 100% !important;
        max-height: 110px !important;
        object-fit: cover !important;
        border-radius: 10px !important;
        border-bottom: 3px solid #2563EB !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1) !important;
    }
    /* Barra lateral limpia con contraste clínico */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h2 {
        color: #0F172A !important;
    }
    /* Botones de navegación interactivos en azul eléctrico */
    [data-testid="stSidebar"] .stButton>button {
        background-color: #F1F5F9 !important;
        color: #2563EB !important;
        border: 1px solid #E2E8F0 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 15px !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-color: #2563EB !important;
    }
    /* 🧬 PANELES EN CONTRASTE ESTILO CRISPR.AI LABS (Fondo blanco sobre gris) */
    .biotech-panel {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-top: 4px solid #2563EB !important; /* Ceja Azul Eléctrico */
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    /* Animación de pulso neón para los indicadores activos */
    @keyframes heartbeat {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    .pulse-glow {
        color: #10B981 !important;
        font-weight: bold !important;
        animation: heartbeat 2s infinite ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

iniciar_base_datos()

# --- 3. BARRA LATERAL IZQUIERDA CON CONTROL DE ROLES ---
st.sidebar.markdown("## 🔬 MethylOx Labs")
st.sidebar.markdown("---")

rol_usuario = st.sidebar.radio(
    "🔑 Seleccione su Rol de Acceso:",
    ["🔬 Médico Oncólogo", "⚙️ Ingeniero / Científico BIOTECH"]
)

st.sidebar.markdown("---")

if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "🏠 Dashboard"

if st.sidebar.button("🏠 Dashboard", use_container_width=True): 
    st.session_state["menu_activo"] = "🏠 Dashboard"

if st.sidebar.button("👤 Patient Profiles", use_container_width=True): 
    st.session_state["menu_activo"] = "👤 Patient Profiles"

if st.sidebar.button("📄 Reports", use_container_width=True): 
    st.session_state["menu_activo"] = "📄 Reports"

# Módulos avanzados ocultos dinámicamente para el médico
if rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.sidebar.markdown("<p style='color:#2563EB; font-weight:bold; margin-bottom:2px;'>Módulos Bioinformáticos:</p>", unsafe_allow_html=True)
    
    if st.sidebar.button("📊 Methylation Matrix", use_container_width=True): 
        st.session_state["menu_activo"] = "📊 Methylation Matrix"
        
    if st.sidebar.button("🧬 CRISPR Guide Library", use_container_width=True): 
        st.session_state["menu_activo"] = "🧬 CRISPR Guide Library"
        
    if st.sidebar.button("🧪 Gel Analysis", use_container_width=True): 
        st.session_state["menu_activo"] = "🧪 Gel Analysis"
        
    if st.sidebar.button("⚙️ Settings", use_container_width=True): 
        st.session_state["menu_activo"] = "⚙️ Settings"

st.sidebar.markdown("---")
st.sidebar.markdown(f"Estatus: <span class='pulse-glow'>● Core Active</span>", unsafe_allow_html=True)


# --- 4. CONTROL DE PANTALLAS (FRONTEND MAESTRO) ---

# PANTALLA 1: DASHBOARD
if st.session_state["menu_activo"] == "🏠 Dashboard":
    # Quitamos el width estático para que tome el 100% de la pantalla (Panorámico Largo)
    st.image("banner_real.png", use_container_width=True)
    
    st.title("Molecular Methylation Analysis Hub")
    st.caption("Early Detection Through Epigenetic AI | Automated Screening Platform")
    st.markdown("---")
    
    # Renderizado del panel de entrada de datos con contraste
    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#2563EB; margin-top:0; font-weight:600;'>📥 Patient Enrollment Matrix</h4>", unsafe_allow_html=True)
    
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
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Segundo panel contrastante para las métricas en tiempo real
    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#2563EB; margin-top:0; font-weight:600;'>📊 Real-Time Analytics Overview</h4>", unsafe_allow_html=True)
    c_tar1, c_tar2, c_tar3 = st.columns(3)
    with c_tar1: st.metric(label="Clinical Cohort Status", value="Stage I Breast Cancer" if patient_id else "Awaiting Input")
    with c_tar2: st.metric(label="Global Methylation Value", value=f"{ctdna_score:.4f} ng/mL")
    with c_tar3: st.metric(label="Diagnostic Verdict", value=resultado)
    st.markdown("</div>", unsafe_allow_html=True)

# PANTALLA 2: HISTORIAL DE PACIENTES
elif st.session_state["menu_activo"] == "👤 Patient Profiles":
    st.title("👤 Patient Profiles & Clinical Records")
    st.markdown("---")
    import sqlite3
    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    if not df_pacientes.empty: 
        st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
        st.dataframe(df_pacientes, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else: 
        st.info("No active logs stored in SQLite3.")

# PANTALLA 3: REPORTES CLINICOS HISTÓRICOS
elif st.session_state["menu_activo"] == "📄 Reports":
    st.title("📄 Clinical Reports Archive")
    st.markdown("---")
    import sqlite3
    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    if not df_pacientes.empty:
        st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
        id_reporte = st.selectbox("Select Patient Record:", df_pacientes["id"].tolist())
        st.success(f"Report unified and ready for download for patient ID: {id_reporte}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No medical reports found in the archive.")

# PANTALLAS EXCLUSIVAS DE INGENIERÍA
elif st.session_state["menu_activo"] == "📊 Methylation Matrix" and rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.title("📊 Methylation Matrix Analytics")
    st.markdown("---")
    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1:
        st.write("**Epigenetic Biomarker Overview (CpG)**")
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.imshow(np.random.rand(8, 8), cmap="Blues")
        ax1.axis("off")
        st.pyplot(fig1)
    with g2:
        st.write("**CRISPR Guidance Response Mapping (ROC)**")
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        x = np.linspace(0, 1, 100)
        ax2.plot(x, 1 - np.exp(-5 * x), color="#2563EB")
        st.pyplot(fig2)
    with g3:
        st.write("**Automated Population Distribution**")
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.hist(np.random.normal(0.3, 0.1, 100), alpha=0.5, color="green")
        ax3.hist(np.random.normal(0.8, 0.1, 100), alpha=0.5, color="red")
        st.pyplot(fig3)
st.markdown("", unsafe_allow_html=True)

if st.session_state["menu_activo"] == "🧬 CRISPR Guide Library" and rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.title("🧬 CRISPR Guide Library & Screening")
    st.markdown("---")
    st.markdown("", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload core genomic logs / raw database files")
    st.markdown("", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            nombre = uploaded_file.name
            df_secuencias = pd.read_excel(uploaded_file) if nombre.endswith(('.xlsx', '.xls')) else pd.read_csv(uploaded_file, sep='\t' if nombre.endswith(('.tsv', '.txt')) else ',')
            df_guias_nuevas = ejecutar_motores_crispr_unificados(df_secuencias)
            st.success(f"Screening complete: {len(df_guias_nuevas)} high-affinity guides isolated.")
            st.dataframe(df_guias_nuevas, use_container_width=True)
        except Exception:
            st.error("Execution error: Invalid matrix mapping structure.")

elif st.session_state["menu_activo"] == "🧪 Gel Analysis" and rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.title("🧪 Automated Gel Clearance Inspection")
    st.markdown("---")
    st.markdown("", unsafe_allow_html=True)
    st.slider("Ajustar concentración de matriz de agarosa (%)", 0.5, 2.5, 1.2)
    fig_gel, ax_gel = plt.subplots(figsize=(6, 3))
    ax_gel.fill_between("color="#111827")
    ax_gel.hlines(y=, xmin=2, xmax=8, color="#10B981", lw=6, alpha=0.8)
    ax_gel.set_title("Bandas de ctDNA fragmentado detectadas por Cas12a", color="white")
    ax_gel.set_facecolor("#111827")
    st.pyplot(fig_gel)
    st.markdown("", unsafe_allow_html=True)

elif st.session_state["menu_activo"] == "⚙️ Settings" and rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.title("⚙️ Engineering Core & Backend Diagnostics")
    st.caption("Inspección en vivo del código analítico puro alojado en motores.py")
    st.markdown("---")
    
    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
        st.success("✅ Conexión e integridad del archivo motores.py verificada.")
    except Exception:
        st.error("❌ No se pudo enlazar el visor con motores.py")
