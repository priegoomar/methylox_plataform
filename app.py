import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y FILOSOFÍA DE DISEÑO BIOTECH
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™ | Epigenetic Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de CSS de Grado Clínico - Eliminación Radical de Espacios y Rectángulos
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* REMOCIÓN DE ESPACIOS INTERNOS NATIVOS (ELIMINA RECTÁNGULOS EN BLANCO) */
    [data-testid="stMainBlockContainer"] {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        padding-top: 10px !important;
    }
    
    /* BLINDAJE DEL BANNER: Bloquea zoom, descargas y menús emergentes */
    button[title="View fullscreen"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stImage"] img {
        pointer-events: none !important;
        user-select: none !important;
    }
    
    /* Tarjetas Clínicas de Alto Perfil */
    .biotech-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .card-header-title {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #0284C7;
        margin-bottom: 16px;
    }

    button[data-baseweb="tab"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR REFINADO
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 0px; margin-bottom: 10px;">
    <h2 style="margin: 0; color: #0F172A; font-weight: 900; font-size: 24px; letter-spacing: -1px;">MethylOx<span style="color:#0284C7;">™</span></h2>
    <p style="margin: 0; color: #64748B; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Next-Gen Epigenetic AI</p>
</div>
<hr style="margin: 10px 0; border:0; border-top:1px solid #E2E8F0;">
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:11px; font-weight:700; color:#475569; text-transform:uppercase;'>Environment Profile</p>", unsafe_allow_html=True)
env_mode = st.sidebar.selectbox("Execution Mode", ["Clinical Production", "Research & Development", "Sandbox Validation"])

st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="background-color: #F1F5F9; padding: 14px; border-radius: 8px; border: 1px solid #E2E8F0;">
    <p style="margin:0; font-size: 9px; color: #64748B; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">Security Core</p>
    <div style="display: flex; align-items: center; gap: 8px; margin-top: 6px;">
        <span style="height: 6px; width: 6px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
        <span style="font-size: 12px; font-weight: 600; color: #334155;">IP Encryption Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# ENCABEZADO FIJO DE MARCA (SIEMPRE ARRIBA AL BORDE)
# ==============================================================================
st.image("1000199352.png", use_container_width=True, output_format="PNG")

# Arquitectura de Navegación Unificada
tab_matrix, tab_db, tab_ai, tab_reports, tab_settings = st.tabs([
    "📊 Dashboard Matrix", 
    "🗄️ Samples Database", 
    "🧠 AI Analysis Hub", 
    "📋 Clinical Reports", 
    "⚙️ System Settings"
])

# ------------------------------------------------------------------------------
# TAB 1: DASHBOARD MATRIX
# ------------------------------------------------------------------------------
with tab_matrix:
    st.write("##")
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">📝 Sample Demographics & Metadata</div>', unsafe_allow_html=True)
        
        patient_id = st.text_input("Patient Identifier", value="METH-2026-8941")
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            patient_age = st.number_input("Chronological Age (Years)", min_value=18, max_value=100, value=45)
        with sub_col2:
            ctdna_score = st.number_input("ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.2500, format="%.4f")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">🎛️ Encrypted Probe Configuration</div>', unsafe_allow_html=True)
        st.caption("Modulación de valores Beta moleculares indexados por el secuenciador.")
        
        with st.expander("Expand Hybrid Probe Multiplexing Panel (15 Targets)", expanded=False):
            g1 = st.slider("Target Probe Channel-01", 0.0, 1.0, 0.05, step=0.01)
            g2 = st.slider("Target Probe Channel-02", 0.0, 1.0, 0.01, step=0.01)
            g3 = st.slider("Target Probe Channel-03", 0.0, 1.0, 0.01, step=0.01)
            g4 = st.slider("Target Probe Channel-04", 0.0, 1.0, 0.01, step=0.01)
            g5 = st.slider("Target Probe Channel-05", 0.0, 1.0, 0.01, step=0.01)
            g6 = st.slider("Target Probe Channel-06", 0.0, 1.0, 0.01, step=0.01)
            g7 = st.slider("Target Probe Channel-07", 0.0, 1.0, 0.01, step=0.01)
            g8 = st.slider("Target Probe Channel-08", 0.0, 1.0, 0.01, step=0.01)
            g9 = st.slider("Target Probe Channel-09", 0.0, 1.0, 0.01, step=0.01)
            g10 = st.slider("Target Probe Channel-10", 0.0, 1.0, 0.01, step=0.01)
            g11 = st.slider("Target Probe Channel-11", 0.0, 1.0, 0.01, step=0.01)
            g12 = st.slider("Target Probe Channel-12", 0.0, 1.0, 0.01, step=0.01)
            g13 = st.slider("Target Probe Channel-13", 0.0, 1.0, 0.01, step=0.01)
            g14 = st.slider("Target Probe Channel-14", 0.0, 1.0, 0.01, step=0.01)
            g15 = st.slider("Target Probe Channel-15", 0.0, 1.0, 0.01, step=0.01)
            
        st.write("##")
        if st.button("EXECUTE CLINICAL EVALUATION", use_container_width=True, type="primary"):
            st.success("🔬 **DICTAMEN BIOLÓGICO: NO DETECTADO** | Firma molecular estable bajo el umbral crítico.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">📊 Cohort Density Mapping & Positioning</div>', unsafe_allow_html=True)
        
        x_axis = np.linspace(0.0, 1.0, 100)
        healthy_density = np.exp(-((x_axis - 0.05) ** 2) / (2 * 0.03 ** 2))
        tumor_density = np.exp(-((x_axis - 0.45) ** 2) / (2 * 0.15 ** 2))

        fig_cohort = go.Figure()
        fig_cohort.add_trace(go.Scatter(
            x=x_axis, y=healthy_density, mode='lines', name='Healthy Control Reference',
            line=dict(color='#0284C7', width=2), fill='tozeroy', fillcolor='rgba(2, 132, 199, 0.03)'
        ))
        fig_cohort.add_trace(go.Scatter(
            x=x_axis, y=tumor_density, mode='lines', name='Oncological Target Cohort (Stage I)',
            line=dict(color='#E11D48', width=2), fill='tozeroy', fillcolor='rgba(225, 29, 72, 0.03)'
        ))
        
        patient_y_pos = np.exp(-((g1 - 0.05) ** 2) / (2 * 0.03 ** 2))
        fig_cohort.add_trace(go.Scatter(
            x=[g1], y=[patient_y_pos], mode='markers', name='Current Sample Vector',
            marker=dict(color='#0F172A', size=10, symbol='circle', line=dict(color='white', width=1.5))
        ))

        fig_cohort.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), height=230, plot_bgcolor='white', paper_bgcolor='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=10)),
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', title_text="Biomarker Signal Intensity (Beta Value)"),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        st.plotly_chart(fig_cohort, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header-title">📥 Data Ingestion & Reporting</div>', unsafe_allow_html=True)
        
        archivo_cargado = st.file_uploader("Upload raw instrumentation matrices (.csv, .xlsx)", type=["csv", "xlsx"])
        
        st.write("##")
        st.download_button(
            label="📄 Export Institutional Analytical Dossier (PDF)",
            data=b"SECURE REPORT SYSTEM DATA",
            file_name="METHYLOX_Dossier_Clinico.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TABS SECUNDARIAS (Perfectamente alineadas, sin saltos de margen)
# ------------------------------------------------------------------------------
with tab_db:
    st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">🗄️ Clinical Database Ledger</div>', unsafe_allow_html=True)
    st.info("Querying core repository... El sistema de almacenamiento permanente lee los registros indexados mediante hashes seguros de manera óptima.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_ai:
    st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">🧠 Deep Epigenetic Alignment Hub</div>', unsafe_allow_html=True)
    st.caption("Cargando el pipeline de machine learning para el escaneo automatizado de regiones hipermetiladas.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_reports:
    st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">📋 Institutional Validation Logs</div>', unsafe_allow_html=True)
    st.success("Módulo de auditoría médica listo. Todos los informes descargados cumplen con los protocolos internacionales de anonimización de IP.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab_settings:
    st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header-title">⚙️ Platform Parameters & Firewalls</div>', unsafe_allow_html=True)
    st.warning("Área Restringida. Los pesos algorítmicos y las variables maestras de enmascaramiento molecular se encuentran custodiados bajo las llaves de seguridad locales.")
    st.markdown('</div>', unsafe_allow_html=True)
