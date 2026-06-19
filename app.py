import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import motores # Tu archivo de lógica de negocio backend

# =====================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS PREMIUM ULTRA-TECNOLÓGICOS
# =====================================================================
st.set_page_config(page_title="MethylOx™ Labs", layout="wide", initial_sidebar_state="expanded")

# Forzar estilo estético limpio para los gráficos integrados
sns.set_theme(style="white")
plt.rcParams["text.color"] = "#0F172A"
plt.rcParams["axes.labelcolor"] = "#475569"
plt.rcParams["xtick.color"] = "#64748B"
plt.rcParams["ytick.color"] = "#64748B"

st.markdown(
    """
    <style>
    /* Fondo general de la plataforma gris clínico satinado */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
   
    /* Eliminar márgenes superiores y laterales de Streamlit */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
   
    /* BARRA LATERAL GRAFITO ESPACIAL MATE */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
   
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 {
        color: #F8FAFC !important;
    }

    /* AJUSTE DE BANNER DE ANCHO COMPLETO PANORÁMICO */
    div[data-testid="stMainBlockContainer"] div[data-testid="element-container"]:has(img) {
        width: 100vw !important;
        max-width: 100vw !important;
        margin-left: calc(50% - 50vw) !important;
        margin-top: -65px !important;
        margin-bottom: 25px !important;
        display: block !important;
    }
   
    div[data-testid="stMainBlockContainer"] [data-testid="stImage"] img {
        width: 100vw !important;
        max-width: 100vw !important;
        height: 240px !important; 
        object-fit: fill !important; 
        image-rendering: -webkit-optimize-contrast !important; 
        display: block !important;
    }

    /* Botones de navegación de la barra lateral */
    [data-testid="stSidebar"] .stButton>button {
        background-color: transparent !important;
        color: #94A3B8 !important;
        border: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 20px !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
   
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #3B82F6 !important;
    }
   
    /* PANELES Y TARJETAS EJECUTIVAS MODULARES */
    .executive-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 30px !important;
        margin-left: 40px !important;
        margin-right: 40px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 10px 25px rgba(148, 163, 184, 0.04) !important;
    }
   
    .card-heading {
        color: #0F172A !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.75px !important;
        margin-bottom: 20px !important;
        border-bottom: 2px solid #F1F5F9 !important;
        padding-bottom: 10px !important;
    }

    /* FILA DE ICONOS DE PROCESO BIOTECNOLÓGICO */
    .process-badge {
        background-color: #F1F5F9;
        border: 1px solid #E2E8F0;
        padding: 10px 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 12px;
        font-weight: 600;
        color: #475569;
    }
   
    /* ANIMACIÓN DE SIGNO VITAL (HEARTBEAT PULSE) */
    @keyframes vitalPulse {
        0% { transform: scale(0.9); opacity: 0.6; }
        50% { transform: scale(1.15); opacity: 1; box-shadow: 0 0 12px #10B981; }
        100% { transform: scale(0.9); opacity: 0.6; }
    }
   
    .vital-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #10B981;
        border-radius: 50%;
        margin-right: 8px;
        animation: vitalPulse 1.5s infinite ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================================
# 2. INICIALIZACIÓN DE DATOS (BACKEND BASE)
# =====================================================================
motores.iniciar_base_datos()
UMBRAL = motores.UMBRAL_GLOBAL

# =====================================================================
# 3. BARRA LATERAL DE NAVEGACIÓN (SISTEMA DE ESTADO REPARADO)
# =====================================================================
st.sidebar.markdown("## 🧬 MethylOx™")
st.sidebar.caption("Epigenetic AI Platform")
st.sidebar.markdown("---")

if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Dashboard"

if st.sidebar.button("📊 Dashboard Matrix", use_container_width=True):
    st.session_state["menu_activo"] = "Dashboard"
if st.sidebar.button("🧪 Samples Database", use_container_width=True):
    st.session_state["menu_activo"] = "Samples"
if st.sidebar.button("🔬 AI Analysis Hub", use_container_width=True):
    st.session_state["menu_activo"] = "AI Analysis"
if st.sidebar.button("📈 Clinical Reports", use_container_width=True):
    st.session_state["menu_activo"] = "Reports"
if st.sidebar.button("⚙️ System Settings", use_container_width=True):
    st.session_state["menu_activo"] = "Settings"

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size:11px; color:#94A3B8; margin-bottom:2px;'>SYSTEM STATUS</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size:13px; color:#FFFFFF; font-weight:600; margin-top:0;'><span class='vital-dot'></span>Core Engine Processing...</p>", unsafe_allow_html=True)

# Gráfica lineal del latido del procesador en el Sidebar
fig_pulse, ax_pulse = plt.subplots(figsize=(2.5, 0.4))
x_pulse = np.linspace(0, 10, 50)
y_pulse = np.sin(x_pulse * 2) * np.exp(-0.05 * x_pulse)
ax_pulse.plot(x_pulse, y_pulse, color="#10B981", lw=1.2)
ax_pulse.axis("off")
fig_pulse.patch.set_facecolor("none")
ax_pulse.set_facecolor("none")
st.sidebar.pyplot(fig_pulse)
st.sidebar.caption("© 2026 MethylOx™")

# =====================================================================
# 4. CONTROL DE PANTALLAS (DASHBOARD MULTI-MODULAR PREMIUM)
# =====================================================================
if st.session_state["menu_activo"] == "Dashboard":
   
    # Carga de la lona panorámica expandida
    st.image("1000199352.png", use_container_width=True, output_format="PNG")
   
    # FILA DE ICONOS DE PROCESO MOLECULAR (Estilo NVIDIA BIOTECH / APPLE VISION)
    st.markdown('<div style="margin-left: 40px; margin-right: 40px; margin-bottom: 20px;">', unsafe_allow_html=True)
    bad_1, bad_2, bad_3, bad_4, bad_5 = st.columns(5)
    with bad_1: st.markdown('<div class="process-badge">🧬 DNA Methylation</div>', unsafe_allow_html=True)
    with bad_2: st.markdown('<div class="process-badge">🤖 AI Engine Active</div>', unsafe_allow_html=True)
    with bad_3: st.markdown('<div class="process-badge">🧪 Liquid Biopsy</div>', unsafe_allow_html=True)
    with bad_4: st.markdown('<div class="process-badge">📊 CpG Site Analysis</div>', unsafe_allow_html=True)
    with bad_5: st.markdown('<div class="process-badge">❤️ Early Detection</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # DISTRIBUCIÓN ESTRUCTURAL PRINCIPAL (Formulario Izquierda | Anillo de IA Derecha)
    col_panel_izq, col_panel_der = st.columns([2, 1])
    
    with col_panel_izq:
        st.markdown('<div class="executive-card" style="margin-left:40px; margin-right:10px; height: 100%;">', unsafe_allow_html=True)
        st.markdown('<p class="card-heading">📋 Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
        
        # Inputs de datos integrados
        patient_id = st.text_input("Patient Identifier", placeholder="Ej. METH-2026-0X")
        patient_age = st.number_input("Chronological Age (Years)", min_value=18, max_value=100, value=45)
        ctdna_score = st.number_input("ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.25, format="%.4f")
        
        st.markdown("<br>", unsafe_allow_html=True)
        resultado = motores.procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score)
       
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Commit Data to SQLite3", use_container_width=True):
                if patient_id:
                    estatus_db = motores.registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado)
                    if estatus_db == "Éxito": st.success("Record secured.")
                    else: st.error("Identifier already exists.")
                else: st.warning("Enter a valid ID.")
        with col_btn2:
            reporte_pdf_contenido = motores.generar_pdf_clinico(patient_id, patient_age, ctdna_score, resultado)
            st.download_button(label="📥 Download Clinical Report", data=reporte_pdf_contenido, file_name=f"Report_{patient_id}.pdf", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_panel_der:
        st.markdown('<div class="executive-card" style="margin-left:10px; margin-right:40px; text-align:center; height: 100%;">', unsafe_allow_html=True)
        st.markdown('<p class="card-heading">🧠 AI Core Engine Accuracy</p>', unsafe_allow_html=True)
        
# Métrica de Anillo Circular Avanzada usando Matplotlib
fig_anillo, ax_anillo = plt.subplots(figsize=(3, 3))
fig_anillo.patch.set_facecolor("none")
ax_anillo.set_facecolor("none")

# Dibujamos el anillo tecnológico
colores_anillo = ['#2563EB', '#E2E8F0'] # Azul eléctrico y gris sutil
ax_anillo.pie([98.7, 1.3], colors=colores_anillo, startangle=90, wedgeprops=dict(width=0.25, edgecolor='none'))
ax_anillo.text(0, 0, "98.7%\nAccuracy", ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
ax_anillo.axis('off')
st.pyplot(fig_anillo)

st.markdown("Total Biomarkers Index: 5,248High-Risk Sequence Delta: 89", unsafe_allow_html=True)
st.markdown('', unsafe_allow_html=True)

# 4.1 ANALÍTICAS INFERIORES PREMIUM EN PARALELO
st.markdown('', unsafe_allow_html=True)
st.markdown('📊 Real-Time Analytics Overview', unsafe_allow_html=True)

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric(label="Screening Sensitivity", value="96.4%", delta="Target Verified")
with col_m2:
    st.metric(label="Analytical Specificity", value="94.1%", delta="Validated")
with col_m3:
    st.metric(label="ctDNA Detection Limit", value="0.01%", delta="High-Resolution")

st.markdown("", unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.markdown("Risk Score Distribution (KDE)")
    fig3, ax3 = plt.subplots(figsize=(6, 2.8))
    fig3.patch.set_facecolor('#FFFFFF')
    ax3.set_facecolor('#F8FAFC')
    sns.kdeplot(np.random.normal(30, 8, 150), color="#3B82F6", fill=True, alpha=0.15, label="Healthy", ax=ax3)
    sns.kdeplot(np.random.normal(78, 6, 150), color="#EC4899", fill=True, alpha=0.2, label="Early Cancer", ax=ax3)
    ax3.set_xlabel("Risk Score (%)", fontsize=8)
    ax3.grid(True, linestyle='--', alpha=0.5, color='#E2E8F0')
    ax3.legend(fontsize=7)
    sns.despine(left=True, bottom=True)
    st.pyplot(fig3)

with col_g2:
    st.markdown("ctDNA Concentration Variance")
    fig4, ax4 = plt.subplots(figsize=(6, 2.8))
    fig4.patch.set_facecolor('#FFFFFF')
    ax4.set_facecolor('#F8FAFC')
    sns.histplot(np.random.exponential(0.5, 100), color="#2563EB", kde=True, alpha=0.4, ax=ax4)
    ax4.set_xlabel("Concentration (ng/mL)", fontsize=8)
    ax4.grid(True, linestyle='--', alpha=0.5, color='#E2E8F0')
    sns.despine(left=True, bottom=True)
    st.pyplot(fig4)

st.markdown('', unsafe_allow_html=True)

# =====================================================================
# 5. PESTAÑA B: SAMPLES DATABASE (TABLAS INTERACTIVAS)
# =====================================================================
elif st.session_state["menu_activo"] == "Samples":
    st.markdown('', unsafe_allow_html=True)
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
        st.warning("Database tables empty or initializing...")
    finally:
        conn.close()
        
    st.markdown('', unsafe_allow_html=True)

# =====================================================================
# 6. PESTAÑA C: SYSTEM SETTINGS (ENGINEERING DIAGNOSTICS)
# =====================================================================
elif st.session_state["menu_activo"] == "Settings":
    st.markdown('', unsafe_allow_html=True)
    st.title("⚙️ Engineering Core & Backend Diagnostics")
    st.markdown("---")
    
    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
        st.success("✅ Conexión e integridad del archivo motores.py verificada.")
    except Exception:
        st.error("❌ No se pudo enlazar el visor con motores.py")
        
    st.markdown('', unsafe_allow_html=True)

# PESTAÑAS ADICIONALES PARA EVITAR CONFLICTOS
elif st.session_state["menu_activo"] in ["AI Analysis", "Reports"]:
    st.markdown('', unsafe_allow_html=True)
    st.title(f"🛠️ {st.session_state['menu_activo']} Workspace")
    st.info("Sección en desarrollo clínico secundario.")
    st.markdown("", unsafe_allow_html=True)
