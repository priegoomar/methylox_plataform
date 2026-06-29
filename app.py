import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN GLOBAL Y ELIMINACIÓN DE LOS RECTÁNGULOS BLANCOS SUPERIORES
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Este bloque CSS elimina el contenedor transparente de arriba que causa los rectángulos
st.markdown("""
<style>
    /* Eliminar el header nativo de Streamlit que genera el espacio en blanco */
    [data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    /* Forzar a que el contenedor principal empiece pegado arriba */
    [data-testid="stMainBlockContainer"] {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
    }
    /* Bloquear zoom e interacción de pantalla completa en el banner */
    button[title="View fullscreen"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stImage"] img {
        pointer-events: none !important;
        user-select: none !important;
    }
    /* Mantener las tarjetas limpias originales */
    .executive-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 20px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización del estado de la sesión
if "menu_active" not in st.session_state:
    st.session_state["menu_active"] = "Dashboard"

# ==============================================================================
#  MÓDULO INTERFAZ LATERAL (TU DISEÑO ORIGINAL EXACTO)
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 0px;">
    <h3 style="margin: 0; color: #0F172A; font-weight: 900; font-size: 20px; letter-spacing: -0.5px;">MethylOx™</h3>
    <p style="margin: 0; color: #64748B; font-size: 11px; font-weight: 500; letter-spacing: 0.5px; text-transform: uppercase;">Epigenetic AI Platform</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.write("##")

# Menú de navegación original por botones de radio
nav_selection = st.sidebar.radio(
    "Navegación del Sistema",
    ["Dashboard Matrix", "Samples Database", "AI Analysis Hub", "Clinical Reports", "System Settings"],
    label_visibility="collapsed"
)

st.sidebar.write("##")

# Sliders globales de referencia (Completamente anonimizados en Sidebar)
if nav_selection == "Dashboard Matrix":
    st.sidebar.markdown('<p style="font-size:11px; font-weight:700; color:#0F172A; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px;">Monitor de Canales Activos</p>', unsafe_allow_html=True)
    
    ct_dna_val = 0.2500
    slider_ch1 = st.sidebar.slider("Canal Ómico CH-01", 0.0, 1.0, 0.45)
    slider_ch2 = st.sidebar.slider("Canal Ómico CH-02", 0.0, 1.0, 0.62)
    slider_ch3 = st.sidebar.slider("Canal Ómico CH-03", 0.0, 1.0, 0.18)
    
    beta1 = min(ct_dna_val * 2.82 * (slider_ch1 + 0.5), 1.0)
    beta2 = min(ct_dna_val * 0.42 * (slider_ch2 + 0.5), 1.0)
else:
    ct_dna_val, slider_ch1, slider_ch2, slider_ch3 = 0.2500, 0.45, 0.62, 0.18
    beta1, beta2 = 0.3500, 0.1200

# Indicador de estado animado original
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding: 5px 0px;">
    <p style="margin: 0; font-size: 10px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 1px;">SYSTEM STATUS</p>
    <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px;">
        <span style="height: 8px; width: 8px; background-color: #0D9488; border-radius: 50%; display: inline-block;"></span>
        <span style="font-size: 12px; font-weight: 600; color: #0F172A;">Core Engine Processing...</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="margin-top: 10px; margin-bottom: 20px; opacity: 0.85;">
    <svg viewBox="0 0 100 20" width="100%" height="25" xmlns="http://www.w3.org/2000/svg">
        <path d="M0,10 Q10,0 20,10 T40,10 T60,10 T80,10 T100,10" fill="none" stroke="#0096C7" stroke-width="2">
            <animate attributeName="d" dur="3s" repeatCount="indefinite"
                values="M0,10 Q10,0 20,10 T40,10 T60,10 T80,10 T100,10;
                        M0,10 Q10,20 20,10 T40,10 T60,0 T80,10 T100,10;
                        M0,10 Q10,0 20,10 T40,10 T60,10 T80,10 T100,10" />
        </path>
    </svg>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 10px; color: #94A3B8; font-weight: 500;'>© 2026 MethylOx™</p>", unsafe_allow_html=True)

# ==============================================================================
#  ENRUTAMIENTO PRINCIPAL DE LA INTERFAZ
# ==============================================================================

# El banner se queda fijo arriba de todo el contenido, sin importar la pestaña seleccionada
st.image("1000199352.png", use_container_width=True, output_format="PNG")

# --- PESTAÑA 1: DASHBOARD MATRIX ---
if nav_selection == "Dashboard Matrix":
    
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 16px; font-weight:700; color:#0F172A;">Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        patient_id = st.text_input("Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2:
        patient_age = st.number_input("Chronological Age (Years)", min_value=18, max_value=100, value=45)
    with col_f3:
        ctdna_score = st.number_input("ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.25, format="%.4f")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CONFIGURACIÓN AVANZADA - TOTALMENTE ANONIMIZADA (IP PROTEGIDA)
    st.write("---")
    with st.expander(" Configuración Avanzada: Panel Genómico Multiplex (15 Sondas CRISPR Blindadas)"):
        st.caption("Ajuste de niveles moleculares Beta detectados. Las correlaciones de peso y mapeo genético están encriptadas en el core.")
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

    if st.button(" Calcular Dictamen Clínico Multiplex", use_container_width=True):
        st.info("Procesando matriz molecular de manera encriptada y segura...")

    # GRÁFICO DE POBLACIÓN ORIGINAL
    st.write("---")
    st.markdown("###  Cohort Density Mapping & Patient Positioning")
    
    x_axis = np.linspace(0.0, 1.0, 100)
    healthy_density = np.exp(-((x_axis - 0.05) ** 2) / (2 * 0.03 ** 2))
    tumor_density = np.exp(-((x_axis - 0.45) ** 2) / (2 * 0.15 ** 2))

    fig_cohort = go.Figure()
    fig_cohort.add_trace(go.Scatter(
        x=x_axis, y=healthy_density, mode='lines', name='Healthy Reference Control (TCGA)',
        line=dict(color='#2ecc71', width=3), fill='tozeroy', fillcolor='rgba(46, 204, 113, 0.15)'
    ))
    fig_cohort.add_trace(go.Scatter(
        x=x_axis, y=tumor_density, mode='lines', name='Oncological Target Cohort (Stage I)',
        line=dict(color='#3498db', width=3), fill='tozeroy', fillcolor='rgba(52, 152, 219, 0.15)'
    ))

    fig_cohort.update_layout(
        xaxis_title="Biomarker Methylation Intensity (Beta Value)",
        yaxis_title="Population Density Vector", margin=dict(l=20, r=20, t=20, b=20), height=380,
        plot_bgcolor='white', paper_bgcolor='white', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor='#f1f1f1', range=[0, 0.8]), yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig_cohort, use_container_width=True)

    # DOCUMENT DOWNLOAD ORIGINAL
    st.write("---")
    st.markdown("###  Institutional Document Download")
    st.download_button(
        label=" Download METHYLOX Corporate Dossier (PDF)", data=b"METHYLOX SIGNATURE PROTECTED SYSTEM",
        file_name="METHYLOX_Dossier_Clinico_Fase2.pdf", mime="application/pdf", use_container_width=True
    )

    st.write("##")
    archivo_cargado = st.file_uploader("Drag and drop your sequencer data matrix here", type=["csv", "xlsx"])
    st.markdown('</div>', unsafe_allow_html=True)


# --- PESTAÑA 2: SAMPLES DATABASE ---
elif nav_selection == "Samples Database":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('### 🗄️ Sample Records & Permanent Database', unsafe_allow_html=True)
    st.write("---")
    st.info("Accediendo al repositorio centralizado... Registros indexados mediante hashes seguros.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- PESTAÑA 3: AI ANALYSIS HUB ---
elif nav_selection == "AI Analysis Hub":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('### 🧠 AI EPIGENETIC ANALYSIS ENGINE', unsafe_allow_html=True)
    st.write("---")
    st.caption("Matriz de alineación molecular y procesamiento de descriptores ómicos en la nube.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- PESTAÑA 4: CLINICAL REPORTS ---
elif nav_selection == "Clinical Reports":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('### 📋 REPORTING & DE-RISK DOSSIER LOG', unsafe_allow_html=True)
    st.write("---")
    st.success("Módulo de exportación analítica listo. Dossier Clínico anonimizado disponible para descarga institucional.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- PESTAÑA 5: SYSTEM SETTINGS ---
elif nav_selection == "System Settings":
    st.markdown('<div class="executive-card">', unsafe_allow_html=True)
    st.markdown('### ⚙️ PLATFORM SECURITY & PARAMETERS', unsafe_allow_html=True)
    st.write("---")
    st.warning("Área restringida. Protocolos de encriptación y llaves maestras cifradas.")
    st.markdown('</div>', unsafe_allow_html=True)
