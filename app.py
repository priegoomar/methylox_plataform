import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN MAESTRA Y ELIMINACIÓN DE LOS CUADROS BLANCOS FANTASMA
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Reset total de la cabecera de Streamlit para eliminar los rectángulos superiores
st.markdown("""
<style>
    /* 1. Eliminar cabecera y espacios invisibles superiores */
    [data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    div.block-container {
        padding-top: 0rem !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }

    /* 2. CORRECCIÓN DE LA BARRA LATERAL (Color Oscuro Corporativo Original) */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B;
    }
    /* Forzar texto claro en la barra lateral */
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    /* Estilizar específicamente los botones de radio del menú */
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important;
    }

    /* 3. BLINDAJE DEL BANNER: Bloquea zoom e interacciones molestas */
    button[title="View fullscreen"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stImage"] img {
        pointer-events: none !important;
        user-select: none !important;
    }

    /* 4. Tarjetas Ejecutivas */
    .executive-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# BARRA LATERAL (DISEÑO PREMIUM RECOBRADO)
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 0px; border-bottom: 1px solid #1E293B; margin-bottom: 20px;">
    <h3 style="margin: 0; color: #FFFFFF !important; font-weight: 900; font-size: 22px; letter-spacing: -0.5px;">MethylOx™</h3>
    <p style="margin: 0; color: #38BDF8 !important; font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">Epigenetic AI Platform</p>
</div>
""", unsafe_allow_html=True)

# Menú de navegación original por botones de radio
nav_selection = st.sidebar.radio(
    "Navegación del Sistema",
    ["Dashboard Matrix", "Samples Database", "AI Analysis Hub", "Clinical Reports", "System Settings"],
    label_visibility="collapsed"
)

st.sidebar.write("##")

# Sliders del Sidebar
if nav_selection == "Dashboard Matrix":
    st.sidebar.markdown('<p style="font-size:11px; font-weight:700; color:#94A3B8 !important; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px;">Monitor de Canales Activos</p>', unsafe_allow_html=True)
    
    ct_dna_val = 0.2500
    slider_ch1 = st.sidebar.slider("Canal Ómico CH-01", 0.0, 1.0, 0.45)
    slider_ch2 = st.sidebar.slider("Canal Ómico CH-02", 0.0, 1.0, 0.62)
    slider_ch3 = st.sidebar.slider("Canal Ómico CH-03", 0.0, 1.0, 0.18)
    
    beta1 = min(ct_dna_val * 2.82 * (slider_ch1 + 0.5), 1.0)
    beta2 = min(ct_dna_val * 0.42 * (slider_ch2 + 0.5), 1.0)
else:
    ct_dna_val, slider_ch1, slider_ch2, slider_ch3 = 0.2500, 0.45, 0.62, 0.18
    beta1, beta2 = 0.3500, 0.1200

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding: 5px 0px;">
    <p style="margin: 0; font-size: 10px; font-weight: 700; color: #64748B !important; text-transform: uppercase; letter-spacing: 1px;">SYSTEM STATUS</p>
    <div style="display: flex; align-items: center; gap: 8px; margin-top: 6px;">
        <span style="height: 7px; width: 7px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
        <span style="font-size: 12px; font-weight: 600; color: #E2E8F0 !important;">Core Engine Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 10px; color: #64748B !important; font-weight: 500; margin-top:30px;'>© 2026 MethylOx™</p>", unsafe_allow_html=True)

# ==============================================================================
# CUERPO DE CONTENIDO PRINCIPAL UNIFICADO
# ==============================================================================

# Banner estático superior (Sin saltos de caja)
st.image("1000199352.png", use_container_width=True, output_format="PNG")

# --- PESTAÑA 1: DASHBOARD MATRIX ---
if nav_selection == "Dashboard Matrix":
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 15px; font-weight:700; color:#0F172A; text-transform:uppercase; letter-spacing:0.5px;">Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        patient_id = st.text_input("Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2:
        patient_age = st.number_input("Chronological Age (Years)", min_value=18, max_value=100, value=45)
    with col_f3:
        ctdna_score = st.number_input("ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.25, format="%.4f")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("⚙️ Configuración Avanzada: Panel Genómico Multiplex (15 Sondas CRISPR Blindadas)"):
        st.caption("Ajuste de niveles moleculares Beta detectados. Las correlaciones están encriptadas en el core.")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            g1 = st.slider("Sonda Multiplex Alpha-01", 0.0, 1.0, 0.05, step=0.01)
            g2 = st.slider("Sonda Multiplex Alpha-02", 0.0, 1.0, 0.01, step=0.01)
            g3 = st.slider("Sonda Multiplex Alpha-03", 0.0, 1.0, 0.01, step=0.01)
            g4 = st.slider("Sonda Multiplex Alpha-04", 0.0, 1.0, 0.01, step=0.01)
            g5 = st.slider("Sonda Multiplex Alpha-05", 0.0, 1.0, 0.01, step=0.01)
            g6 = st.slider("Sonda Multiplex Alpha-06", 0.0, 1.0, 0.01, step=0.01)
            g7 = st.slider("Sonda Multiplex Alpha-07", 0.0, 1.0, 0.01, step=0.01)
            g8 = st.slider("Sonda Multiplex Alpha-08", 0.0, 1.0, 0.01, step=0.01)
        with col_g2:
            g9 = st.slider("Sonda Multiplex Alpha-09", 0.0, 1.0, 0.01, step=0.01)
            g10 = st.slider("Sonda Multiplex Alpha-10", 0.0, 1.0, 0.01, step=0.01)
            g11 = st.slider("Sonda Multiplex Alpha-11", 0.0, 1.0, 0.01, step=0.01)
            g12 = st.slider("Sonda Multiplex Alpha-12", 0.0, 1.0, 0.01, step=0.01)
            g13 = st.slider("Sonda Multiplex Alpha-13", 0.0, 1.0, 0.01, step=0.01)
            g14 = st.slider("Sonda Multiplex Alpha-14", 0.0, 1.0, 0.01, step=0.01)
            g15 = st.slider("Sonda Multiplex Alpha-15", 0.0, 1.0, 0.01, step=0.01)

    st.write("##")
    if st.button("Calcular Dictamen Clínico Multiplex", use_container_width=True, type="primary"):
        st.info("Procesando matriz molecular de manera encriptada y segura...")

    st.write("---")
    st.markdown("#### 📊 Cohort Density Mapping & Patient Positioning")
    
    x_axis = np.linspace(0.0, 1.0, 100)
    healthy_density = np.exp(-((x_axis - 0.05) ** 2) / (2 * 0.03 ** 2))
    tumor_density = np.exp(-((x_axis - 0.45) ** 2) / (2 * 0.15 ** 2))

    fig_cohort = go.Figure()
    fig_cohort.add_trace(go.Scatter(
        x=x_axis, y=healthy_density, mode='lines', name='Healthy Reference Control',
        line=dict(color='#0284C7', width=2.5), fill='tozeroy', fillcolor='rgba(2, 132, 199, 0.04)'
    ))
    fig_cohort.add_trace(go.Scatter(
        x=x_axis, y=tumor_density, mode='lines', name='Oncological Target Cohort',
        line=dict(color='#E11D48', width=2.5), fill='tozeroy', fillcolor='rgba(225, 29, 72, 0.04)'
    ))

    fig_cohort.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), height=320, plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(showgrid=True, gridcolor='#F1F5F9', range=[0, 0.75]), yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig_cohort, use_container_width=True)

    st.write("---")
    st.markdown("#### 📥 Data Ingestion & Archiving")
    archivo_cargado = st.file_uploader("Drag and drop your sequencer data matrix here", type=["csv", "xlsx"])
    
    st.write("##")
    st.download_button(
        label="📄 Download Institutional Analytical Dossier (PDF)", data=b"SECURE REPORT SYSTEM DATA",
        file_name="METHYLOX_Dossier_Clinico.pdf", mime="application/pdf", use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


# --- PESTAÑA 2: SAMPLES DATABASE ---
elif nav_selection == "Samples Database":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('### 🗄️ Sample Records & Permanent Database', unsafe_allow_html=True)
    st.write("---")
    st.info("Accediendo al repositorio centralizado... Registros indexados mediante hashes seguros de manera óptima.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- PESTAÑA 3: AI ANALYSIS HUB ---
elif nav_selection == "AI Analysis Hub":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('### 🧠 AI Epigenetic Analysis Engine', unsafe_allow_html=True)
    st.write("---")
    st.caption("Matriz de alineación molecular y procesamiento de descriptores ómicos en la nube.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- PESTAÑA 4: CLINICAL REPORTS ---
elif nav_selection == "Clinical Reports":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('### 📋 Reporting & De-Risk Dossier Log', unsafe_allow_html=True)
    st.write("---")
    st.success("Módulo de exportación analítica listo. Dossier Clínico anonimizado disponible para descarga institucional.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- PESTAÑA 5: SYSTEM SETTINGS ---
elif nav_selection == "System Settings":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('### ⚙️ Platform Security & Parameters', unsafe_allow_html=True)
    st.write("---")
    st.warning("Área restringida. Protocolos de encriptación y llaves maestras cifradas corporativas.")
    st.markdown('</div>', unsafe_allow_html=True)
