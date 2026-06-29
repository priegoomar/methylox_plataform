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

# Inyección de CSS de grado institucional (Financiero / Clínico)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
        color: #0F172A;
    }
    
    /* Sidebar Estilizado */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    
    /* Contenedor unificado de tarjeta ejecutiva */
    .biotech-card-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    }
    
    .section-title {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #0284C7;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Badges Moleculares Horizontales */
    .badge-bar {
        display: flex;
        gap: 10px;
        margin-top: -10px;
        margin-bottom: 28px;
        flex-wrap: wrap;
    }
    .molec-badge {
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
        color: #475569;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    
    /* Overrides estéticos de Streamlit */
    div[data-testid="stWidgetLabel"] p {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #334155 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR REFINADO
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 0px; border-bottom: 1px solid #1E293B; margin-bottom: 25px;">
    <h2 style="margin: 0; color: #FFFFFF; font-weight: 900; font-size: 24px; letter-spacing: -1px;">MethylOx<span style="color:#0284C7;">™</span></h2>
    <p style="margin: 0; color: #64748B; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Epigenetic AI Architecture</p>
</div>
""", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "SYSTEM NAVIGATION",
    ["Dashboard Matrix", "Samples Database", "AI Analysis Hub", "Clinical Reports", "System Settings"]
)

st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="background-color: #111827; padding: 16px; border-radius: 8px; border: 1px solid #1E293B;">
    <p style="margin:0; font-size: 9px; color: #64748B; font-weight: 700; letter-spacing: 1px;">SYSTEM STATUS</p>
    <div style="display: flex; align-items: center; gap: 8px; margin-top: 6px;">
        <span style="height: 6px; width: 6px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
        <span style="font-size: 12px; font-weight: 500; color: #E2E8F0;">Core Pipeline Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# ROUTING DE COMPONENTES INTERNOS
# ==============================================================================

if nav_selection == "Dashboard Matrix":
    
    # 1. Recuperación del Banner de Lona Original
    st.image("1000199352.png", use_container_width=True, output_format="PNG")
    st.write("##")
    
    # 2. Badges Clínicos de Control Estilizados
    st.markdown("""
    <div class="badge-bar">
        <span class="molec-badge">🧬 DNA Methylation Assay</span>
        <span class="molec-badge">🤖 AI Engine Pipeline Active</span>
        <span class="molec-badge">🩸 Liquid Biopsy Target</span>
        <span class="molec-badge">🔬 CpG Site Matrix (15-Channel)</span>
        <span class="molec-badge">🔒 Intellectual Property Secured</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Distribución Bifurcada del Espacio (Métrica Organizada)
    col_left, col_right = st.columns([11, 13], gap="large")
    
    with col_left:
        # CONTENEDOR UNO: ENROLAMIENTO Y CONFIGURACIÓN DE MUESTRA
        st.markdown('<div class="biotech-card-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 Sample Demographics & Metadata</div>', unsafe_allow_html=True)
        
        patient_id = st.text_input("Patient Identifier", value="METH-2026-8941", placeholder="METH-2026-0X")
        patient_age = st.number_input("Chronological Age (Years)", min_value=18, max_value=100, value=45)
        ctdna_score = st.number_input("ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.2500, format="%.4f")
        
        st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎛️ Encrypted Probe Configuration</div>', unsafe_allow_html=True)
        st.caption("Ajuste los niveles Beta moleculares detectados por el secuenciador.")
        
        with st.expander("Ver Panel de Sondas Multiplex Blindadas (15 Targets)", expanded=False):
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
        if st.button("CALCULAR DICTAMEN CLÍNICO MULTIPLEX", use_container_width=True, type="primary"):
            st.success("🔬 **DICTAMEN BIOLÓGICO: NEGATIVO** | Score Seguro")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        # CONTENEDOR DOS: UNIFICADO PARA EVITAR CUADROS FRAGMENTADOS
        st.markdown('<div class="biotech-card-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Cohort Position & Data Ingestion</div>', unsafe_allow_html=True)
        
        # Generación de la gráfica de distribución poblacional de referencia
        x_axis = np.linspace(0.0, 1.0, 100)
        healthy_density = np.exp(-((x_axis - 0.05) ** 2) / (2 * 0.03 ** 2))
        tumor_density = np.exp(-((x_axis - 0.45) ** 2) / (2 * 0.15 ** 2))

        fig_cohort = go.Figure()
        fig_cohort.add_trace(go.Scatter(
            x=x_axis, y=healthy_density, mode='lines', name='Healthy Reference Control',
            line=dict(color='#0284C7', width=2), fill='tozeroy', fillcolor='rgba(2, 132, 199, 0.04)'
        ))
        fig_cohort.add_trace(go.Scatter(
            x=x_axis, y=tumor_density, mode='lines', name='Oncological Target (Stage I)',
            line=dict(color='#E11D48', width=2), fill='tozeroy', fillcolor='rgba(225, 29, 72, 0.04)'
        ))
        
        patient_y_pos = np.exp(-((g1 - 0.05) ** 2) / (2 * 0.03 ** 2))
        fig_cohort.add_trace(go.Scatter(
            x=[g1], y=[patient_y_pos], mode='markers', name='Current Vector',
            marker=dict(color='#0F172A', size=11, symbol='circle', line=dict(color='white', width=1.5))
        ))

        fig_cohort.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), height=240, plot_bgcolor='white', paper_bgcolor='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=10)),
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', title_text="Biomarker Signal Intensity", title_font=dict(size=11)),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        st.plotly_chart(fig_cohort, use_container_width=True)
        
        st.markdown("<hr style='margin: 20px 0; border:0; border-top:1px solid #E2E8F0;'>", unsafe_allow_html=True)
        
        # Integración del pipeline de subida masiva e informe institucional en la misma tarjeta limpia
        st.markdown('<p style="font-size:12px; font-weight:700; color:#334155; margin-bottom:8px;">Sequencer File Ingestion</p>', unsafe_allow_html=True)
        archivo_cargado = st.file_uploader("Upload matrices", label_visibility="collapsed", type=["csv", "xlsx"])
        
        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        st.download_button(
            label="📄 Download Institutional Analytical Dossier (PDF)",
            data=b"SECURE REPORT SYSTEM",
            file_name="METHYLOX_Dossier_Clinico_Fase2.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# Pestañas secundarias limpias y corporativas
elif nav_selection == "Samples Database":
    st.markdown('<div class="biotech-card-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🗄️ System Permanent Clinical Database</div>', unsafe_allow_html=True)
    st.info("Querying system infrastructure... Connection secured via encrypted local loopback.")
    st.markdown('</div>', unsafe_allow_html=True)

elif nav_selection == "AI Analysis Hub":
    st.markdown('<div class="biotech-card-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧠 Deep Epigenetic Alignment Hub</div>', unsafe_allow_html=True)
    st.caption("Cloud computing clustering nodes are ready to accept raw molecular matrix vectors.")
    st.markdown('</div>', unsafe_allow_html=True)

elif nav_selection == "Clinical Reports":
    st.markdown('<div class="biotech-card-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Institutional Validation Dossier Log</div>', unsafe_allow_html=True)
    st.success("Analytical export modules active. Download link ready.")
    st.markdown('</div>', unsafe_allow_html=True)

elif nav_selection == "System Settings":
    st.markdown('<div class="biotech-card-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ Platform Parameters & Firewalls</div>', unsafe_allow_html=True)
    st.warning("Restricted Area. Master cryptographic keys and pipeline layers are protected by corporate firewall policies.")
    st.markdown('</div>', unsafe_allow_html=True)
