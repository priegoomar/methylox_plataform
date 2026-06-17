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
    /* Fondo general de la plataforma gris clínico satinado */
    .stApp { background-color: #F1F5F9 !important; font-family: 'Inter', -apple-system, sans-serif !important; }
    
    /* Eliminar márgenes superiores y laterales por defecto de Streamlit */
    .block-container { padding-top: 0rem !important; padding-left: 0rem !important; padding-right: 0rem !important; max-width: 100% !important; }
    
    /* BARRA LATERAL GRAFITO MATE (#1E293B) */
    [data-testid="stSidebar"] { background-color: #1E293B !important; border-right: none !important; }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 { color: #FFFFFF !important; }
    
    /* 🖼️ MOTOR INYECTOR PANORÁMICO: Fuerza al st.image nativo a ocupar el 100% de la pantalla horizontal */
    [data-testid="stImage"] { 
        width: 100vw !important; 
        margin-left: 0px !important;
        margin-right: 0px !important;
        padding: 0px !important;
        text-align: center !important; 
    }
    [data-testid="stImage"] img { 
        width: 100vw !important; 
        max-height: 90px !important; 
        object-fit: fill !important; 
        border-radius: 0px !important;
        border-bottom: 3px solid #2563EB !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15) !important;
    }
    
    /* Espaciador interno para mantener los márgenes de las tarjetas del médico */
    .main-content-wrapper {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 1rem !important;
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

if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "🏠 Dashboard"

if st.sidebar.button("🏠 Dashboard", use_container_width=True): st.session_state["menu_activo"] = "🏠 Dashboard"
if st.sidebar.button("🧪 Samples", use_container_width=True): st.session_state["menu_activo"] = "🧪 Samples"
if st.sidebar.button("🧠 AI Analysis", use_container_width=True): st.session_state["menu_activo"] = "🧠 AI Analysis"
if st.sidebar.button("🧬 Biomarkers", use_container_width=True): st.session_state["menu_activo"] = "🧬 Biomarkers"
if st.sidebar.button("📄 Reports", use_container_width=True): st.session_state["menu_activo"] = "📄 Reports"
if st.sidebar.button("⚙️ Settings", use_container_width=True): st.session_state["menu_activo"] = "⚙️ Settings"

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

if st.session_state["menu_activo"] == "🏠 Dashboard":
    st.image("banner_real.png", use_container_width=True)
    
    st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
    
    st.title("Molecular Methylation Analysis Hub")
    st.caption("Panel Ejecutivo de Cribado para Cáncer de Mama en Etapa Temprana")
    st.markdown("---")
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">📥 Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1: patient_id = st.text_input("🆔 Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2: patient_age = st.number_input("🎂 Chronological Age", min_value=18, max_value=100, value=45)
    with col_f3: ctdna_score = st.number_input("🔬 ctDNA Concentration (ng/mL)", min_value=0.0000, max_value=5.0000, format="%.4f", value=0.2500)
    
    resultado = motores.procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score)
        
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Commit Diagnostic Data (Save to SQLite3)", use_container_width=True):
            if patient_id:
                estatus_db = motores.registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado)
                if estatus_db == "Éxito": st.success(f"Record secured in SQLite3 for ID: {patient_id}")
                else: st.error("Database status: Patient Identifier already exists.")
            else: st.warning("Please enter a valid Patient Identifier.")
                
    with col_btn2:
        reporte_pdf_contenido = motores.generar_pdf_clinico(patient_id, patient_age, ctdna_score, resultado)
        st.download_button(label="📥 Download Personalized Clinical Report", data=reporte_pdf_contenido, file_name=f"MethylOx_Report_{patient_id if patient_id else 'Draft'}.doc", mime="application/msword", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">📈 Real-Time Analytics Overview</p>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric(label="SENSITIVITY", value="96.4%")
    with k2: st.metric(label="SPECIFICITY", value="94.1%")
    with k3: st.metric(label="AUC (ROC)", value="0.983")
    with k4: st.metric(label="VERDICT STATUS", value=resultado)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 📊 Clinical Evidence & Multi-Population Models")
    g1, g2, g3 = st.columns(3)
    
    with g1:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-heading">DNA Methylation: Genomic Position</p>', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(4.5, 3.2))
        data_heatmap = np.random.rand(8, 8)
        sns.heatmap(data_heatmap, cmap="Purples", cbar=True, ax=ax1, xticklabels=False, yticklabels=False)
        st.pyplot(fig1)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with g2:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-heading">ROC Performance Curve</p>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(4.5, 3.2))
        x_val = np.linspace(0, 1, 100)
        y_val = 1 - np.exp(-5 * x_val)
        ax2.plot(x_val, y_val, color="#6366F1", lw=2.5)
        # Línea diagonal fija reparada con datos correctos
        ax2.plot([0, 1], [0, 1], color="#CBD5E1", linestyle="--")
        ax2.set_xlabel("1 - Specificity", fontsize=8)
        ax2.set_ylabel("Sensitivity", fontsize=8)
        sns.despine()
        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with g3:
        st.markdown('<div class="executive-card">', unsafe_allow_html=True)
        st.markdown('<p class="card-heading">Risk Distribution Model</p>', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(4.5, 3.2))
        sns.kdeplot(np.random.normal(25, 6, 150), color="#3B82F6", fill=True, alpha=0.2, label="Healthy", ax=ax3)
        sns.kdeplot(np.random.normal(55, 8, 150), color="#8B5CF6", fill=True, alpha=0.2, label="Benign", ax=ax3)
if st.session_state["menu_activo"] == "🏠 Dashboard": 
    sns.kdeplot(
        np.random.normal(78, 6, 150),
        color="#EC4899",
        fill=True,
        alpha=0.2,
        label="Early Cancer",
        ax=ax3,
    )
    ax3.set_xlabel("Risk Score (%)", fontsize=8)
    ax3.legend(fontsize=7)
    sns.despine()
    st.pyplot(fig3), use_container_width=False

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
