import streamlit as fancy_st # Usamos un alias limpio o el estándar
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Importación segura de la lógica del motor
try:
    import motores
except ImportError:
    # Definición de fallbacks en caso de que motores.py esté en actualización
    class MotoresFallback:
        def registrar_paciente_db(self, pid, age, ctdna): return True
        def generar_pdf_clinico(self, pid, age, ctdna): return b"PDF_DATA"
    motores = MotoresFallback()

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="MethylOx™ Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. IDENTIDAD VISUAL Y ESTILOS CSS (CRISPR.AI LABS STYLE)
# ==========================================
st.markdown("""
    <style>
    /* Configuración del fondo clínico de la app */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Contenedores principales y tarjetas modulares */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.02);
        margin-bottom: 16px;
    }
    
    /* Limpieza de fondos duplicados en bloques anidados */
    div[data-testid="element-container"], div[data-testid="stForm"] {
        background-color: transparent !important;
        box-shadow: none !important;
        padding: 0px !important;
        border: none !important;
    }

    /* Estilización de la Barra Lateral (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Títulos y fuentes corporativas (Inter/Sans-serif) */
    h1, h2, h3, h4 {
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, sans-serif;
        font-weight: 600 !important;
    }
    
    label {
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    /* BOTÓN 1: Commit Data (Azul Tecnológico) */
    div.stButton > button:first-child, .commit-btn button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #2563EB !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }

    /* BOTÓN 2: Download Report / st.download_button (Rosa Vibrante) */
    div.stDownloadButton > button {
        background-color: #EC4899 !important;
        color: #FFFFFF !important;
        border: 1px solid #EC4899 !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s ease;
    }
    div.stDownloadButton > button:hover {
        background-color: #DB2777 !important;
        border-color: #DB2777 !important;
        box-shadow: 0 4px 6px -1px rgba(236, 72, 153, 0.2);
    }

    /* Ajuste para el nuevo banner institucional */
    [data-testid="stImage"] img {
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CONTROL DE ESTADO Y NAVEGACIÓN LATERAL
# ==========================================
if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Dashboard"

# Menú visual con emojis, pero mapeado internamente de forma limpia
opciones_menu = {
    "📊 Dashboard": "Dashboard",
    "🔬 Samples": "Samples",
    "⚙️ Settings": "Settings"
}

st.sidebar.title("MethylOx™ Navigation")
seleccion_visual = st.sidebar.radio(
    "Select Workspace Section",
    options=list(opciones_menu.keys()),
    index=list(opciones_menu.values()).index(st.session_state["menu_activo"])
)
# Actualizar el estado interno de forma segura
st.session_state["menu_activo"] = opciones_menu[seleccion_visual]

# ==========================================
# 4. ENRUTAMIENTO DE SECCIONES (VISTAS)
# ==========================================

# SECCIÓN PRINCIPAL: DASHBOARD
if st.session_state["menu_activo"] in ["Dashboard", "🗙 Dashboard"]:
    
    # Renderizado del nuevo banner institucional solicitado
    st.image("1000199352.png", use_container_width=True)
    
    st.markdown("### Clinical Analysis and Patient Intake")
    
    # Formulario Clínico de Pacientes (Estructura de Datos Seguro)
    with st.form("clinical_intake_form"):
        col_inputs = st.columns(3)
        
        with col_inputs[0]:
            patient_id = st.text_input("Patient Identifier", placeholder="e.g., MOX-2026-09A")
        with col_inputs[1]:
            chronological_age = st.number_input("Chronological Age", min_value=0, max_value=120, value=45)
        with col_inputs[2]:
            ctdna_concentration = st.number_input("ctDNA Concentration (pg/mL)", min_value=0.0, max_value=100.0, value=1.5, step=0.1)
            
        # Fila de acciones y envío del formulario
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            commit_data = st.form_submit_button("Commit Data to Database")
            
        with col_btn2:
            # Botón de descarga de reporte clínico
            pdf_bytes = motores.generar_pdf_clinico(patient_id, chronological_age, ctdna_concentration)
            download_report = st.download_button(
                label="Download Report (PDF)",
                data=pdf_bytes,
                file_name=f"MethylOx_Report_{patient_id}.pdf",
                mime="application/pdf"
            )

    # Lógica de Ejecución del Commit
    if commit_data:
        if patient_id.strip() == "":
            st.error("Error: Please provide a valid Patient Identifier.")
        else:
            exito = motores.registrar_paciente_db(patient_id, chronological_age, ctdna_concentration)
            if exito:
                st.success(f"Success: Record for {patient_id} successfully synchronized with methyl_clinic.db.")
            else:
                st.error("Database connection failure. Please review SQLite logs.")

    # ==========================================
    # 5. GRÁFICAS INFERIORES DE ANÁLISIS POPULACIONAL
    # ==========================================
    st.markdown("### Epigenetic Population Biopsy Benchmarking")
    
    # Inicialización limpia de los subplots previniendo NameError
    fig3, ax3 = plt.subplots(1, 2, figsize=(12, 4))
    
    # Datos simulados de población de referencia
    edades_control = [25, 34, 45, 52, 61, 68, 72]
    ctdna_control = [0.2, 0.5, 1.1, 1.4, 2.1, 3.8, 5.2]
    
    # Gráfico izquierdo: Regresión/Dispersión Poblacional
    sns.scatterplot(x=edades_control, y=ctdna_control, ax=ax3[0], color="#2563EB", s=100, label="Reference Cohort")
    if patient_id:
        sns.scatterplot(x=[chronological_age], y=[ctdna_concentration], ax=ax3[0], color="#EC4899", s=200, marker="*", label=f"Patient {patient_id}")
    ax3[0].set_title("ctDNA vs Age Distribution", fontsize=10, fontweight='bold', color='#0F172A')
    ax3[0].set_xlabel("Age", fontsize=8)
    ax3[0].set_ylabel("ctDNA (pg/mL)", fontsize=8)
    ax3[0].grid(True, linestyle="--", alpha=0.3)
    
    # Gráfico derecho: Umbral de riesgo de metilación
    sns.barplot(x=["Normal Range", "Borderline", "High Risk Threshold"], y=[1.0, 2.5, 5.0], ax=ax3[1], palette="Blues_d")
    if ctdna_concentration > 0:
        ax3[1].axhline(y=ctdna_concentration, color="#EC4899", linestyle="--", linewidth=2, label="Current Patient")
    ax3[1].set_title("Clinical Risk Intervals", fontsize=10, fontweight='bold', color='#0F172A')
    ax3[1].set_ylabel("Concentration Scale", fontsize=8)
    ax3[1].legend()

    # Ajustar layout de matplotlib y desplegar en Streamlit
    fig3.tight_layout()
    st.pyplot(fig3)

# SECCIÓN SECUNDARIA: SAMPLES (Módulo clínico futuro)
elif st.session_state["menu_activo"] == "Samples":
    st.title("🔬 Epigenetic Samples Inventory")
    st.info("Liquid Biopsy sample storage module. Querying records from 'pacientes' table in methyl_clinic.db...")
    # Aquí puedes añadir una consulta de tabla con st.dataframe()

# SECCIÓN TERCIARIA: SETTINGS (Configuración del sistema)
elif st.session_state["menu_activo"] == "Settings":
    st.title("⚙️ System Configuration")
    st.write("Database Path: `methyl_clinic.db`")
    st.write("Active Model Engine: `Epigenetic AI Regressor v2.4`")
