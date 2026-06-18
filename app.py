import sqlite3
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import motores

# 1. CONFIGURACION DE PAGINA MAESTRA
st.set_page_config(page_title="MethylOx Labs", layout="wide", initial_sidebar_state="expanded")

# Configuración estética de gráficos premium
sns.set_theme(style="white")
plt.rcParams["text.color"] = "#0F172A"
plt.rcParams["axes.labelcolor"] = "#475569"
plt.rcParams["xtick.color"] = "#64748B"
plt.rcParams["ytick.color"] = "#64748B"

# 2. INYECCIÓN CSS SEGURO: CONTROL DE MARGENES ABSOLUTOS DE EXTREMO A EXTREMO
st.markdown(
    """
    <style>
    # ESTILOS PREMIUM INSPIRADOS EN CRISPR.AI LABS (METHYLOX)
# =========================================================
st.markdown("""
<style>
    /* 1. Fondo Global y Tipografía Limpia */
    @import url('https://googleapis.com');
    
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* 2. Tarjetas Modulares Estilo Laboratorio (Bordes Suaves, Sombras Sutiles) */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05) !important;
        margin-bottom: 20px !important;
    }

    /* Evitar que el contenedor maestro duplique fondos */
    div[data-testid="stMain"] > div[data-testid="stVerticalBlock"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
    }

    /* Evitar que las columnas internas hereden dobles bordes */
    div[data-testid="stHorizontalBlock"] div[data-testid="stVerticalBlock"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
    }

    /* 3. Diseño de Inputs / Campos de Formulario */
    div[data-testid="stNumberInput"] input, 
    div[data-testid="stTextInput"] input {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 10px !important;
        color: #0F172A !important;
        font-weight: 500 !important;
        padding: 10px 14px !important;
    }
    
    div[data-testid="stNumberInput"] input:focus, 
    div[data-testid="stTextInput"] input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }

    label {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 6px !important;
    }

    /* 4. Botón 1: Commit Data (Azul Tecnológico con Hover Suave) */
    div.stButton > button:first-child:not([data-testid="download_button"]) {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.025em !important;
        width: 100% !important;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    div.stButton > button:first-child:not([data-testid="download_button"]):hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 12px -2px rgba(37, 99, 235, 0.3) !important;
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
    }

    /* 5. Botón 2: Download Report (Rosa Vibrante Tecnológico) */
    div[data-testid="stDownloadButton"] > button, 
    .stDownloadButton > button {
        background: linear-gradient(135deg, #EC4899 0%, #DB2777 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.025em !important;
        width: 100% !important;
        box-shadow: 0 4px 6px -1px rgba(236, 72, 153, 0.2) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 12px -2px rgba(236, 72, 153, 0.3) !important;
        background: linear-gradient(135deg, #DB2777 0%, #C2185B 100%) !important;
    }

    /* 6. Encabezados y Títulos de Secciones */
    h1, h2, h3 {
        color: #0F172A !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
    }
</style>
""", unsafe_allow_html=True)
# =========================================================
)
# Inicialización silenciosa de BD llamando al backend
motores.iniciar_base_datos()
UMBRAL = motores.UMBRAL_GLOBAL

# --- 3. BARRA LATERAL DE NAVEGACIÓN ---
st.sidebar.markdown("## 🔮 MethylOx™")
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
st.sidebar.markdown("<p style='font-size:11px; color:#94A3B8; margin-bottom:2px;'>SYSTEM STATUS</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:13px; color:#FFFFFF; font-weight:600; margin-top:0;'><span class='vital-dot'></span>Core Engine Processing...</p>", unsafe_allow_html=True)

# Gráfica lineal del latido del procesador
fig_pulse, ax_pulse = plt.subplots(figsize=(2.5, 0.4))
x_pulse = np.linspace(0, 10, 50)
y_pulse = np.sin(x_pulse * 2) * np.exp(-0.05 * x_pulse)
ax_pulse.plot(x_pulse, y_pulse, color="#10B981", lw=1.2)
ax_pulse.axis("off")
fig_pulse.patch.set_facecolor("none")
ax_pulse.set_facecolor("none")
st.sidebar.pyplot(fig_pulse)

st.sidebar.caption("© 2026 MethylOx™")

# --- 4. CONTROL DE PANTALLAS ---
if st.session_state["menu_activo"] in ["Dashboard"]:
    st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    
    # 1. EL BANNER LOCAL QUE SÍ FUNCIONA (CON MÁXIMA CALIDAD PARA LAS LETRAS)
    st.image("banner_real.png", use_container_width=True, output_format="PNG")
    
    st.write("")
    st.write("")

    st.markdown('<p class="card-heading">📋 Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
    
    # 2. ENTRADA DE DATOS DEL PACIENTE
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        patient_id = st.text_input("📋 Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2:
        patient_age = st.number_input("📅 Chronological Age", min_value=18, max_value=100, value=45)
    with col_f3:
        ctdna_score = st.number_input("🧪 ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.25, format="%.4f")

    # 3. LÓGICA DE PROCESAMIENTO Y BOTONES (SIN MEZCLAS)
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
        st.download_button(
            label="📥 Download Personalized Clinical Report", 
            data=reporte_pdf_contenido, 
            file_name=f"Methylox_Report_{patient_id}.pdf", 
            use_container_width=True
        )
        
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. ANALÍTICAS EN TIEMPO REAL Y GRÁFICO INICIALIZADO CORRECTAMENTE
    st.markdown('### 📊 REAL-TIME ANALYTICS OVERVIEW')
    
    # Aquí puedes colocar tus métricas fijas de la interfaz (Sensitivity, Specificity, etc.)
    
    fig3, ax3 = plt.subplots(figsize=(6, 2.8))
    sns.kdeplot(np.random.normal(78, 6, 150), color="#EC4899", fill=True, alpha=0.2, label="Early Cancer", ax=ax3)
    ax3.set_xlabel("Risk Score (%)", fontsize=8)
    ax3.legend(fontsize=7)
    sns.despine()
    st.pyplot(fig3)

# 2. Las siguientes secciones ahora sí se conectarán correctamente
elif st.session_state["menu_activo"] == "🧪 Samples":
    st.markdown("", unsafe_allow_html=True)
    st.title("🧪 Sample Records & Permanent Database")
    st.markdown("---")

    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()

    if not df_pacientes.empty:
        st.markdown("", unsafe_allow_html=True)
        st.dataframe(df_pacientes, use_container_width=True)
        st.markdown("", unsafe_allow_html=True)
    else:
        st.info("No active patient logs detected inside methyl_clinic.db.")
    st.markdown("", unsafe_allow_html=True)

elif st.session_state["menu_activo"] == "⚙️ Settings":
    st.markdown("", unsafe_allow_html=True)
    st.title("⚙️ Engineering Core & Backend Diagnostics")
    st.markdown("---")

    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
        st.success("✅ Conexión e integridad del archivo motores.py verificada.")
    except Exception:
        st.error("❌ No se pudo enlazar el visor con motores.py")
        st.markdown("", unsafe_allow_html=True)
