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
# 2. INYECCIÓN CSS (Tu estilo + Ajuste de Banner)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    /* Tus clases originales del contenedor principal */
    .main-content-wrapper {
        padding: 10px;
    }
    
    .executive-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.03) !important;
    }

    .card-heading {
        color: #0F172A !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-top: 0px;
        margin-bottom: 20px;
        font-family: 'Inter', sans-serif;
    }

    /* RECORTE INTELIGENTE DE ALTURA PARA TU NUEVO BANNER */
    .banner-recortado img {
        height: 160px !important; /* Altura delgada ideal para laptops */
        object-fit: cover !important; /* Evita que las letras se aplasten */
        object-position: center 38% !important; /* Centra el texto MethylOx */
        border-radius: 12px !important;
    }
    
    /* Botón: Commit Data (Azul) */
    div.stButton > button {
        background-color: #2563EB !important;
        color: white !important;
        border: 1px solid #2563EB !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    
    /* Botón: Download Report (Rosa) */
    div.stDownloadButton > button {
        background-color: #EC4899 !important;
        color: white !important;
        border: 1px solid #EC4899 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100% !important;
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

st.sidebar.markdown("---")

# TU GRÁFICO DE PULSO ORIGINAL DE LA BARRA LATERAL
fig_pulse, ax_pulse = plt.subplots(figsize=(2.5, 0.4))
x_pulse = np.linspace(0, 10, 50)
y_pulse = np.sin(x_pulse * 2) * np.exp(-0.05 * x_pulse)
ax_pulse.plot(x_pulse, y_pulse, color="#10B981", lw=1.2)
ax_pulse.axis("off")
fig_pulse.patch.set_facecolor("none")
ax_pulse.set_facecolor("none")
st.sidebar.pyplot(fig_pulse)

st.sidebar.caption("© 2026 MethylOx™")

# ==========================================
# 4. CONTROL DE PANTALLAS (Tu bloque corregido)
# ==========================================
if st.session_state["menu_activo"] in ["Dashboard"]:
    
    # Abrimos tus envoltorios originales
    st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    
    # EL BANNER NUEVO CON MÁXIMA CALIDAD Y ALTURA REDUCIDA
    with st.container():
        st.markdown('<div class="banner-recortado">', unsafe_allow_html=True)
        st.image("1000199352.png", use_container_width=True, output_format="PNG")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True) # Cierre seguro de la tarjeta del banner
    
    # ENTRADA DE DATOS DEL PACIENTE (Nueva tarjeta limpia)
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
    
    col_inputs = st.columns(3)
    with col_inputs[0]:
        patient_id = st.text_input("Patient Identifier", placeholder="e.g., MOX-2026-X9")
    with col_inputs[1]:
        chronological_age = st.number_input("Chronological Age (Years)", min_value=1, max_value=120, value=54)
    with col_inputs[2]:
        ctdna_concentration = st.number_input("ctDNA Concentration (pg/mL)", min_value=0.0, max_value=100.0, value=2.4, step=0.1)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fila de Botones del Formulario
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        commit_data = st.button("Commit Data to Database")
    with col_btn2:
        try:
            pdf_bytes = motores.generar_pdf_clinico(patient_id, chronological_age, ctdna_concentration)
        except:
            pdf_bytes = b"PDF Fallback"
            
        download_report = st.download_button(
            label="Download Report (PDF)",
            data=pdf_bytes,
            file_name=f"MethylOx_Report_{patient_id if patient_id else 'Draft'}.pdf",
            mime="application/pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True) # Cierre de tarjeta de datos

    # Lógica del Backend (SQLite)
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

    # PANEL DE GRÁFICOS AVANZADOS
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p class="card-heading">Advanced Epigenetic Analytics</p>', unsafe_allow_html=True)
    
    sns.set_theme(style="white")
    fig, ax = plt.subplots(1, 2, figsize=(14, 4.2), facecolor="#FFFFFF")
    
    np.random.seed(42)
    edades_base = np.linspace(20, 80, 50)
    ctdna_base = 0.05 * edades_base + np.random.normal(0, 0.5, 50)
    ctdna_base = np.clip(ctdna_base, 0.1, None)

    # Gráfico 1: Tendencia Cohorte
    sns.regplot(x=edades_base, y=ctdna_base, ax=ax[0], color="#2563EB", 
                scatter_kws={'alpha':0.3, 's':50, 'color':'#64748B'}, 
                line_kws={'color':'#2563EB', 'linewidth':2, 'label':'Cohort Trend'})
    if patient_id:
        ax[0].scatter(chronological_age, ctdna_concentration, color="#EC4899", s=220, marker="*", edgecolors="black", zorder=5, label=f"Patient: {patient_id}")
    ax[0].set_title("ctDNA Concentration vs. Age Distribution", fontsize=10, fontweight='bold', color='#0F172A')
    ax[0].legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=8)
    ax[0].spines['top'].set_visible(False)
    ax[0].spines['right'].set_visible(False)

    # Gráfico 2: Densidad de Riesgo
    sns.kdeplot(ctdna_base, ax=ax[1], fill=True, color="#2563EB", alpha=0.08, linewidth=2)
    ax[1].axvline(x=1.5, color="#10B981", linestyle=":", linewidth=1.5, label="Normal Threshold (<1.5)")
    ax[1].axvline(x=3.5, color="#F59E0B", linestyle=":", linewidth=1.5, label="Borderline Zone (1.5-3.5)")
    ax[1].axvline(x=ctdna_concentration, color="#EC4899", linestyle="-", linewidth=2, label="Current Patient Level")
    ax[1].set_title("Biopsy Risk Interval Distribution", fontsize=10, fontweight='bold', color='#0F172A')
    ax[1].legend(frameon=True, facecolor='#F8FAFC', edgecolor='none', fontsize=8)
    ax[1].spines['top'].set_visible(False)
    ax[1].spines['right'].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    
    st.markdown('</div>', unsafe_allow_html=True) # Cierre tarjeta gráficos
    st.markdown('</div>', unsafe_allow_html=True) # Cierre main-content-wrapper

# OTRAS SECCIONES
elif st.session_state["menu_activo"] == "Samples":
    st.title("🔬 Epigenetic Samples Inventory")
    st.markdown('<div class="executive-card"><h3>Active Repositories</h3><p>Connecting to <code>methyl_clinic.db</code>...</p></div>', unsafe_allow_html=True)

elif st.session_state["menu_activo"] == "Settings":
    st.title("⚙️ System Configuration")
    st.markdown('<div class="executive-card"><h3>Configuration Parameters</h3><p>Engine version: <code>MethylOx AI Regressor v2.6</code></p></div>', unsafe_allow_html=True)
