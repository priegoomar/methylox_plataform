import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS DE ALTO NIVEL (UI/UX PREMIUM)
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™ | Epigenetic Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de CSS institucional (Diseño limpio, tipografía suiza, tarjetas con micro-sombras)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap');
    
    /* Configuración Global */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC;
        color: #1E293B;
    }
    
    /* Estilización de Barras Laterales */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    /* Tarjetas Ejecutivas Biotech */
    .biotech-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    
    .card-title {
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #0284C7;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Badges Moleculares Premium */
    .badge-container {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
        flex-wrap: wrap;
    }
    .molec-badge {
        background: #F0F9FF;
        border: 1px solid #B0E5FC;
        color: #0369A1;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Inputs y Sliders Estilizados */
    div[data-testid="stWidgetLabel"] p {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR REFINADO (BRANDING CORPORATIVO)
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 0px; border-bottom: 1px solid #334155; margin-bottom: 25px;">
    <h2 style="margin: 0; color: #FFFFFF; font-weight: 900; font-size: 24px; letter-spacing: -1px;">MethylOx<span style="color:#0284C7;">™</span></h2>
    <p style="margin: 0; color: #94A3B8; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Next-Gen Epigenetic Architecture</p>
</div>
""", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "SYSTEM NAVIGATION",
    ["Dashboard Matrix", "Samples Database", "AI Analysis Hub", "Clinical Reports", "System Settings"]
)

# Estado del Sistema Dinámico de Bajo Perfil
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="background-color: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
    <p style="margin:0; font-size: 9px; color: #94A3B8; font-weight: 700; letter-spacing: 1px;">SECURE CORE CONNECTION</p>
    <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px;">
        <span style="height: 6px; width: 6px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
        <span style="font-size: 12px; font-weight: 500; color: #F1F5F9;">Operational Baseline Alpha</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 10px; color: #64748B; margin-top: 30px; text-align: center;'>© 2026 MethylOx Inc. All rights reserved.</p>", unsafe_allow_html=True)

# ==============================================================================
# ROUTING PRINCIPAL DE LA PLATAFORMA
# ==============================================================================

if nav_selection == "Dashboard Matrix":
    
    # Encabezado Limpio del Panel (Reemplaza las imágenes pesadas por tipografía moderna)
    st.markdown("""
    <div style="margin-bottom: 32px;">
        <h1 style="font-size: 28px; font-weight: 800; color: #0F172A; letter-spacing: -0.5px; margin-bottom: 4px;">Multiplex Clinical Analytics</h1>
        <p style="color: #64748B; font-size: 14px; margin: 0;">Automated pipeline for sequencing interpretation and clinical boundary positioning.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fila Unificada de Badges de Estado
    st.markdown("""
    <div class="badge-container">
        <span class="molec-badge">🧬 DNA Methylation Assay</span>
        <span class="molec-badge">🤖 AI Processing Pipeline v4.2</span>
        <span class="molec-badge">🩸 Liquid Biopsy Target Enriched</span>
        <span class="molec-badge">🔬 15-CpG Site Multiplexing</span>
        <span class="molec-badge">🔒 IP Protected Encryption</span>
    </div>
    """, unsafe_allow_html=True)
    
    # DISEÑO EN GRID MÁSTER: Entrada de datos a la izquierda, Analítica Poblacional a la derecha
    col_layout_left, col_layout_right = st.columns([2, 3], gap="large")
    
    with col_layout_left:
        # TARJETA 1: ENROLLMENT MATRIX
        st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📝 Patient Case Enrollment</div>', unsafe_allow_html=True)
        
        patient_id = st.text_input("Patient Identifier", value="METH-2026-8941")
        patient_age = st.number_input("Chronological Age (Years)", min_value=18, max_value=100, value=52)
        ctdna_score = st.number_input("ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.3421, format="%.4f")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # TARJETA 2: PANEL DE CONTROL DE SONDAS (IP ANONIMIZADA)
        st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">🎛️ Hybrid Probe Multiplexing</div>', unsafe_allow_html=True)
        st.caption("Ajuste los valores Beta crudos indexados por el secuenciador.")
        
        with st.expander("Expand Target Probes (1 a 15)", expanded=False):
            g1 = st.slider("Probe Target Alpha-01", 0.0, 1.0, 0.12, step=0.01)
            g2 = st.slider("Probe Target Alpha-02", 0.0, 1.0, 0.04, step=0.01)
            g3 = st.slider("Probe Target Alpha-03", 0.0, 1.0, 0.08, step=0.01)
            g4 = st.slider("Probe Target Alpha-04", 0.0, 1.0, 0.21, step=0.01)
            g5 = st.slider("Probe Target Alpha-05", 0.0, 1.0, 0.02, step=0.01)
            g6 = st.slider("Probe Target Alpha-06", 0.0, 1.0, 0.05, step=0.01)
            g7 = st.slider("Probe Target Alpha-07", 0.0, 1.0, 0.11, step=0.01)
            g8 = st.slider("Probe Target Alpha-08", 0.0, 1.0, 0.03, step=0.01)
            g9 = st.slider("Probe Target Alpha-09", 0.0, 1.0, 0.09, step=0.01)
            g10 = st.slider("Probe Target Alpha-10", 0.0, 1.0, 0.04, step=0.01)
            g11 = st.slider("Probe Target Alpha-11", 0.0, 1.0, 0.07, step=0.01)
            g12 = st.slider("Probe Target Alpha-12", 0.0, 1.0, 0.15, step=0.01)
            g13 = st.slider("Probe Target Alpha-13", 0.0, 1.0, 0.02, step=0.01)
            g14 = st.slider("Probe Target Alpha-14", 0.0, 1.0, 0.05, step=0.01)
            g15 = st.slider("Probe Target Alpha-15", 0.0, 1.0, 0.06, step=0.01)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón de Procesamiento Clínico
        if st.button("EXECUTE CLINICAL DIAGNOSIS", use_container_width=True, type="primary"):
            # Simulación segura para conservar la maquetación impecable
            st.success("🔬 **DICTAMEN: NO DETECTADO** | Score: 0.0412")
            st.toast("Análisis completado bajo protocolo de encriptación.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_layout_right:
        # TARJETA 3: MAPEO INTERACTIVO DE COHORTE
        st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📊 Cohort Density Mapping & Calibration</div>', unsafe_allow_html=True)
        
        x_axis = np.linspace(0.0, 1.0, 100)
        healthy_density = np.exp(-((x_axis - 0.06) ** 2) / (2 * 0.04 ** 2))
        tumor_density = np.exp(-((x_axis - 0.42) ** 2) / (2 * 0.14 ** 2))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis, y=healthy_density, mode='lines', name='Healthy Control Reference',
            line=dict(color='#0284C7', width=2.5), fill='tozeroy', fillcolor='rgba(2, 132, 199, 0.06)'
        ))
        fig.add_trace(go.Scatter(
            x=x_axis, y=tumor_density, mode='lines', name='Oncological Target Cohort',
            line=dict(color='#E11D48', width=2.5), fill='tozeroy', fillcolor='rgba(225, 29, 72, 0.06)'
        ))
        
        # Marcador dinámico del paciente
        p_pos = np.exp(-((g1 - 0.06) ** 2) / (2 * 0.04 ** 2))
        fig.add_trace(go.Scatter(
            x=[g1], y=[p_pos], mode='markers', name='Current Sample Vector',
            marker=dict(color='#0F172A', size=12, symbol='circle', line=dict(color='white', width=2))
        ))

        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10), height=340, plot_bgcolor='white', paper_bgcolor='white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9', title="Beta-Value Range", range=[0, 0.75]),
            yaxis=dict(showgrid=False, showticklabels=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # TARJETA 4: BULK PIPELINE DE SECUENCIACIÓN
        st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">📥 Mass Sequencer Bulk Ingestion</div>', unsafe_allow_html=True)
        archivo_cargado = st.file_uploader("Upload raw instrumentation data (.csv, .xlsx)", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

elif nav_selection == "Samples Database":
    st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🗄️ Centralized Repository & Permanent Ledger</div>', unsafe_allow_html=True)
    st.info("Querying system infrastructure... Connection secured via encrypted local loopback.")
    st.markdown('</div>', unsafe_allow_html=True)

elif nav_selection == "AI Analysis Hub":
    st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧠 Deep Epigenetic Alignment Hub</div>', unsafe_allow_html=True)
    st.caption("Cloud computing clustering nodes are ready to accept raw molecular matrix vectors.")
    st.markdown('</div>', unsafe_allow_html=True)

elif nav_selection == "Clinical Reports":
    st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Institutional Validation Dossier Log</div>', unsafe_allow_html=True)
    st.success("Analytical export modules active. Download link ready.")
    st.markdown('</div>', unsafe_allow_html=True)

elif nav_selection == "System Settings":
    st.markdown('<div class="biotech-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚙️ Core Platform Security & Cryptography</div>', unsafe_allow_html=True)
    st.warning("Restricted Area. Master cryptographic keys and pipeline layers are protected by corporate firewall policies.")
    st.markdown('</div>', unsafe_allow_html=True)
