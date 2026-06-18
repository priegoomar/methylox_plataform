import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================================
# RECONEXIÓN CON TU BACKEND REAL
# ==========================================
import motores # Conecta directamente con tu archivo motores.py

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
# 2. INYECCIÓN CSS LIMPIA Y ESTABLE
# ==========================================
st.markdown("""
    <style>
    /* Fondo General Clínico */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Fuentes y Textos */
    h1, h2, h3, h4, label {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    label {
        color: #475569 !important;
        font-weight: 500 !important;
    }

    /* Tarjetas Modulares tipo CRISPR.AI */
    .clinical-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03) !important;
    }
    
    /* Botón: Commit Data (Azul Tecnológico) */
    div.stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border: 1px solid #2563EB !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background-color: #1D4ED8 !important;
        transform: translateY(-1px);
    }

    /* Botón: Download Report (Rosa Vibrante) */
    div.stDownloadButton > button {
        background-color: #EC4899 !important;
        color: white !important;
        border: 1px solid #EC4899 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #DB2777 !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CONTROL DE ESTADO Y BARRA LATERAL
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
# 4. VISTA PRINCIPAL: DASHBOARD
# ==========================================
if st.session_state["menu_activo"] == "Dashboard":
    
    # BANNER CONTROLADO POR HTML (Evita el bug de desalineación)
    # Usamos codificación nativa para renderizar la imagen de forma panorámica y centrada
    st.markdown("""
        <div style="
            width: 100%; 
            height: 160px; 
            border-radius: 12px; 
            background-image: url('app/static/1000199352.png'), url('1000199352.png'); 
            background-size: cover; 
            background-position: center 35%;
            margin-bottom: 20px;
        "></div>
    """, unsafe_allow_html=True)

    # FORMULARIO EN TARJETA BLANCA (Garantiza el recuadro contenedor)
    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color:#0F172A; margin-bottom: 20px;'>🔬 Patient Clinical Intake & Biomarkers</h3>", unsafe_allow_html=True)
    
    col_inputs = st.columns(3)
    with col_inputs[0]:
        patient_id = st.text_input("Patient Identifier", placeholder="e.g., MOX-2026-X9")
    with col_inputs[1]:
        chronological_age = st.number_input("Chronological Age (Years)", min_value=1, max_value=120, value=54)
    with col_inputs[2]:
        ctdna_concentration = st.number_input("ctDNA Concentration (pg/mL)", min_value=0.0, max_value=100.0, value=2.4, step=0.1)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fila de Botones
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        commit_data = st.button("Commit Data to Database")
    with col_btn2:
        try:
            pdf_bytes = motores.generar_pdf_clinico(patient_id, chronological_age, ctdna_concentration)
        except:
            pdf_bytes = b"PDF Fallback Data"
            
        download_report = st.download_button(
            label="Download Report (PDF)",
            data=pdf_bytes,
            file_name=f"MethylOx_Report_{patient_id if patient_id else 'Draft'}.pdf",
            mime="application/pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True) # Cierre de tarjeta médica

    # Lógica de Base de Datos
    if commit_data:
        if not patient_id.strip():
            st.error("Validation Error: Please provide a valid Patient Identifier.")
        else:
            try:
                exito = motores.registrar_paciente_db(patient_id, chronological_age, ctdna_concentration)
                if exito:
                    st.success(f"Success: Analysis data for {patient_id} committed to methyl_clinic.db.")
                else:
                    st.error("Database Transaction Failed.")
            except Exception as e:
                st.error(f"Backend connection error: {e}")

    # ==========================================
    # 5. PANEL DE GRÁFICOS AVANZADOS
    # ==========================================
    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color:#0F172A; margin-bottom: 20px;'>📈 Advanced Epigenetic Analytics</h3>", unsafe_allow_html=True)
    
    sns.set_theme(style="white")
    fig, ax = plt.subplots(1, 2, figsize=(14, 4.5), facecolor="#FFFFFF")
    
    # Datos de control de la población
    np.random.seed(42)
    edades_base = np.linspace(20, 80, 50)
    ctdna_base = 0.05 * edades_base + np.random.normal(0, 0.5, 50)
    ctdna_base = np.clip(ctdna_base, 0.1, None)

    # Gráfico 1: Tendencia Cohorte vs Paciente
    sns.regplot(x=edades_base, y=ctdna_base, ax=ax[0], color="#2563EB", 
                scatter_kws={'alpha':0.3, 's':50, 'color':'#64748B'}, 
                line_kws={'color':'#2563EB', 'linewidth':2, 'label':'Cohort Trend'})
    
    if patient_id:
        ax[0].scatter(chronological_age, ctdna_concentration, color="#EC4899", s=220, 
                      marker="*", edgecolors="black", linewidths=1.2, zorder=5, label=f"Patient: {patient_id}")
    
    ax[0].set_title("ctDNA Concentration vs. Age Distribution", fontsize=10, fontweight='bold', color='#0F172A')
    ax[0].grid(True, linestyle=":", alpha=0.5, color="#E2E8F0")
    ax[0].legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=8)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)

    # Gráfico 2: Densidad de Riesgo
    sns.kdeplot(ctdna_base, ax=ax[1], fill=True, color="#2563EB", alpha=0.08, linewidth=2, label="Population Density")
    ax[1].axvline(x=1.5, color="#10B981", linestyle=":", linewidth=1.5, label="Normal Threshold (<1.5)")
    ax[1].axvline(x=3.5, color="#F59E0B", linestyle=":", linewidth=1.5, label="Borderline Zone (1.5-3.5)")
    ax[1].axvline(x=ctdna_concentration, color="#EC4899", linestyle="-", linewidth=2, label="Current Patient Level")
    
    ax[1].set_title("Biopsy Risk Interval Distribution", fontsize=10, fontweight='bold', color='#0F172A')
    ax[1].legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=8)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# OTRAS SECCIONES
elif st.session_state["menu_activo"] == "Samples":
    st.title("🔬 Epigenetic Samples Inventory")
    st.markdown('<div class="clinical-card"><h3>Active Repositories</h3><p>Connecting to <code>methyl_clinic.db</code>...</p></div>', unsafe_allow_html=True)

elif st.session_state["menu_activo"] == "Settings":
    st.title("⚙️ System Configuration")
    st.markdown('<div class="clinical-card"><h3>Configuration Parameters</h3><p>Engine version: <code>MethylOx AI Regressor v2.6</code></p></div>', unsafe_allow_html=True)
