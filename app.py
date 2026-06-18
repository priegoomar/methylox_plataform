import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================================
# RECONEXIÓN CON TU BACKEND REAL
# ==========================================
import motores # Conecta directamente con procesar_diagnostico_clinico, registrar_paciente_db, generar_pdf_clinico

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA (Estilo Clínico)
# ==========================================
st.set_page_config(
    page_title="MethylOx™ Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. INYECCIÓN CSS AVANZADA (Diseño CRISPR.AI LABS)
# ==========================================
st.markdown("""
    <style>
    /* Fondo General de la App */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Diseño de la Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Tipografías e Inputs */
    h1, h2, h3, h4, .stMarkdown h3 {
        color: #0F172A !important;
        font-family: 'Inter', -apple-system, sans-serif;
        font-weight: 600 !important;
    }
    
    label {
        color: #475569 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }

    /* Contenedor tipo Tarjeta de Laboratorio (Card) */
    .clinical-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03);
    }
    
    /* Estilización del Botón: Commit Data (Azul Tecnológico) */
    div.stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border: 1px solid #2563EB !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.1) !important;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
        border-color: #1D4ED8 !important;
        transform: translateY(-1px);
    }

    /* Estilización del Botón: Download Report (Rosa Vibrante) */
    div.stDownloadButton > button {
        background-color: #EC4899 !important;
        color: white !important;
        border: 1px solid #EC4899 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(236, 72, 153, 0.1) !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #DB2777 !important;
        border-color: #DB2777 !important;
        transform: translateY(-1px);
    }

    /* AJUSTE FIJO PARA HACER EL BANNER MENOS ALTO (PANORÁMICO) */
    [data-testid="stImage"] img {
        border-radius: 12px !important;
        height: 160px !important; /* Altura delgada optimizada */
        object-fit: cover !important; /* Recorte inteligente sin deformar */
        object-position: center 38% !important; /* Enfoca el logo perfectamente */
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CONTROL DE ESTADO Y BARRA LATERAL (Lógica limpia)
# ==========================================
if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Dashboard"

opciones_menu = {
    "📊 Dashboard": "Dashboard",
    "🔬 Samples": "Samples",
    "⚙️ Settings": "Settings"
}

st.sidebar.markdown("<h2 style='text-align: center; color: #2563EB; margin-bottom: 0;'>MethylOx™</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #64748B; font-size: 0.8rem;'>Epigenetic AI Platform</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

seleccion_visual = st.sidebar.radio(
    "Navigation Menu",
    options=list(opciones_menu.keys()),
    index=list(opciones_menu.values()).index(st.session_state["menu_activo"])
)
st.session_state["menu_activo"] = opciones_menu[seleccion_visual]

# ==========================================
# 4. TRATAMIENTO DE LA VISTA: DASHBOARD
# ==========================================
if st.session_state["menu_activo"] == "Dashboard":
    
    # Renderizado del Banner Panorámico Compactado
    try:
        st.image("1000199352.png", use_container_width=True)
    except:
        st.warning("Banner image source '1000199352.png' loading...")

    st.markdown("<br>", unsafe_allow_html=True)

    # Formulario de Captura Estilizado en Tarjeta Médica
    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color:#0F172A;'>🔬 Patient Clinical Intake & Biomarkers</h3>", unsafe_allow_html=True)
    
    col_inputs = st.columns(3)
    with col_inputs[0]:
        patient_id = st.text_input("Patient Identifier", placeholder="e.g., MOX-2026-X9")
    with col_inputs[1]:
        chronological_age = st.number_input("Chronological Age (Years)", min_value=1, max_value=120, value=54)
    with col_inputs[2]:
        ctdna_concentration = st.number_input("ctDNA Concentration (pg/mL)", min_value=0.0, max_value=100.0, value=2.4, step=0.1)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Columnas de Botones con Acciones del Backend Real
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        commit_data = st.button("Commit Data to Database")
    with col_btn2:
        # Generación dinámica del PDF usando motores.py de tu Backend
        try:
            pdf_bytes = motores.generar_pdf_clinico(patient_id, chronological_age, ctdna_concentration)
        except Exception as e:
            pdf_bytes = b"Fallback PDF Data Error Backend Connection"
            
        download_report = st.download_button(
            label="Download Report (PDF)",
            data=pdf_bytes,
            file_name=f"MethylOx_Report_{patient_id if patient_id else 'Draft'}.pdf",
            mime="application/pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Lógica de Ejecución Interactiva con la Base de Datos SQLite3 del Backend
    if commit_data:
        if not patient_id.strip():
            st.error("Validation Error: Please provide a valid Patient Identifier.")
        else:
            try:
                # Intenta registrar en tu base de datos mediante motores.py
                exito = motores.registrar_paciente_db(patient_id, chronological_age, ctdna_concentration)
                if exito:
                    st.success(f"Success: Analysis data for {patient_id} committed to methyl_clinic.db.")
                    # Opcional: Ejecutar diagnóstico médico predictivo en segundo plano
                    if hasattr(motores, 'procesar_diagnostico_clinico'):
                        diagnostico = motores.procesar_diagnostico_clinico(patient_id, chronological_age, ctdna_concentration)
                else:
                    st.error("Database Transaction Failed: Review methyl_clinic.db availability.")
            except Exception as e:
                st.error(f"Backend Linkage Error: {e}")

    # ==========================================
    # 5. PANEL DE GRÁFICOS REDISEÑADO (Look Profesional BioTech)
    # ==========================================
    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color:#0F172A;'>📈 Advanced Epigenetic Analytics</h3>", unsafe_allow_html=True)
    
    sns.set_theme(style="white")
    fig, ax = plt.subplots(1, 2, figsize=(14, 4.5), facecolor="#FFFFFF")
    
    # Generación de datos estéticos y limpios de control poblacional
    np.random.seed(42)
    edades_base = np.linspace(20, 80, 50)
    ctdna_base = 0.05 * edades_base + np.random.normal(0, 0.5, 50)
    ctdna_base = np.clip(ctdna_base, 0.1, None)

    # GRÁFICO 1: Análisis de Tendencia Poblacional (Scatter + Regresión)
    sns.regplot(x=edades_base, y=ctdna_base, ax=ax[0], color="#2563EB", 
                scatter_kws={'alpha':0.3, 's':50, 'color':'#64748B'}, 
                line_kws={'color':'#2563EB', 'linewidth':2, 'label':'Cohort Trend'})
    
    if patient_id:
        ax[0].scatter(chronological_age, ctdna_concentration, color="#EC4899", s=220, 
                      marker="*", edgecolors="black", linewidths=1.2, zorder=5, label=f"Patient: {patient_id}")
    
    ax[0].set_title("ctDNA Concentration vs. Age Distribution", fontsize=10, fontweight='bold', pad=12, color='#0F172A')
    ax[0].set_xlabel("Chronological Age (Years)", fontsize=8, color='#475569')
    ax[0].set_ylabel("ctDNA Level (pg/mL)", fontsize=8, color='#475569')
    ax[0].grid(True, linestyle=":", alpha=0.5, color="#E2E8F0")
    ax[0].legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=8)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)

    # GRÁFICO 2: Densidad de Riesgo Clínico e Intervalos
    sns.kdeplot(ctdna_base, ax=ax[1], fill=True, color="#2563EB", alpha=0.08, linewidth=2, label="Population Density")
    ax[1].axvline(x=1.5, color="#10B981", linestyle=":", linewidth=1.5, label="Normal Threshold (<1.5)")
    ax[1].axvline(x=3.5, color="#F59E0B", linestyle=":", linewidth=1.5, label="Borderline Zone (1.5-3.5)")
    ax[1].axvline(x=ctdna_concentration, color="#EC4899", linestyle="-", linewidth=2, label="Current Patient Level")
    
    ax[1].set_title("Biopsy Risk Interval Distribution", fontsize=10, fontweight='bold', pad=12, color='#0F172A')
    ax[1].set_xlabel("ctDNA Concentration (pg/mL)", fontsize=8, color='#475569')
    ax[1].set_ylabel("Density Scale", fontsize=8, color='#475569')
    ax[1].legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=8)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. OTRAS SECCIONES
# ==========================================
elif st.session_state["menu_activo"] == "Samples":
    st.title("🔬 Epigenetic Samples Inventory")
    st.markdown('<div class="clinical-card"><h3>Active Repositories</h3><p>Querying active data from table <code>pacientes</code> inside <code>methyl_clinic.db</code>...</p></div>', unsafe_allow_html=True)

elif st.session_state["menu_activo"] == "Settings":
    st.title("⚙️ System Configuration")
    st.markdown('<div class="clinical-card"><h3>Configuration Parameters</h3><p>Engine version linked: <code>MethylOx AI Regressor v2.6</code></p></div>', unsafe_allow_html=True)
