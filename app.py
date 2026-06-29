import io
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN MAESTRA Y ELIMINACIÓN DE ESPACIOS MUERTOS
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos globales para la barra lateral y fuentes
st.markdown("""
<style>
    /* 1. Eliminar por completo la cabecera nativa y el espacio muerto superior */
    [data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    div.block-container {
        padding-top: 0rem !important;
    }
    
    /* 2. BARRA LATERAL (Color Oscuro Corporativo Original) */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] * {
        color: #F1F5F9 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important;
    }
    
    /* 3. BLINDAJE DEL BANNER */
    button[title="View fullscreen"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stImage"] img {
        pointer-events: none !important;
        user-select: none !important;
    }

    /* 4. Estilo para las Tarjetas de las Pestañas Secundarias */
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
# GENERACIÓN DE BUFFER DE ARCHIVO COMPATIBLE (PDF EN MEMORIA)
# ==============================================================================
buffer_pdf = io.BytesIO()
buffer_pdf.write(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Count 1/Kids[3 0 R]>>\nendobj\n3 0 obj\n<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 55>>\nstream\nBT\n/F1 12 Tf\n72 712 Td\n(MethylOx Institutional Analytical Dossier - Protected Content) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000015 00000 n\n0000000068 00000 n\n0000000120 00000 n\n0000000219 00000 n\ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n326\n%%EOF")
pdf_data = buffer_pdf.getvalue()

# ==============================================================================
# BARRA LATERAL (DISEÑO PREMIUM ORIGINAL)
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 0px; border-bottom: 1px solid #1E293B; margin-bottom: 20px;">
    <h3 style="margin: 0; color: #FFFFFF !important; font-weight: 900; font-size: 22px; letter-spacing: -0.5px;">MethylOx™</h3>
    <p style="margin: 0; color: #38BDF8 !important; font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase;">Epigenetic AI Platform</p>
</div>
""", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "Navegación del Sistema",
    ["Dashboard Matrix", "Samples Database", "AI Analysis Hub", "Clinical Reports", "System Settings"],
    label_visibility="collapsed"
)

st.sidebar.write("##")

if nav_selection == "Dashboard Matrix":
    st.sidebar.markdown('<p style="font-size:11px; font-weight:700; color:#94A3B8 !important; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px;">Monitor de Canales Activos</p>', unsafe_allow_html=True)
    slider_ch1 = st.sidebar.slider("Canal Ómico CH-01", 0.0, 1.0, 0.45)
    slider_ch2 = st.sidebar.slider("Canal Ómico CH-02", 0.0, 1.0, 0.62)
    slider_ch3 = st.sidebar.slider("Canal Ómico CH-03", 0.0, 1.0, 0.18)

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

# ==============================================================================
# CUERPO DE CONTENIDO PRINCIPAL
# ==============================================================================

# Banner estático superior
st.image("1000199352.png", use_container_width=True, output_format="PNG")

# --- CONTROL DE LOGICA DE PESTAÑAS ---
if nav_selection == "Dashboard Matrix":
    
    col_izquierda, col_derecha = st.columns([12, 12], gap="large")
    
    # ---- COLUMNA IZQUIERDA: CONTENEDOR NATIVO SEGURO ----
    with col_izquierda:
        # st.container(border=True) crea la tarjeta perfecta sin bugs visuales
        with st.container(border=True):
            st.markdown('<p style="font-size: 15px; font-weight:700; color:#0F172A; text-transform:uppercase; letter-spacing:0.5px; margin-top:5px; margin-bottom:15px;">📝 Patient Case Enrollment Matrix</p>', unsafe_allow_html=True)
            
            patient_id = st.text_input("Patient Identifier", placeholder="Ej. METH-2026-0X")
            patient_age = st.number_input("Chronological Age (Years)", min_value=18, max_value=100, value=45)
            ctdna_score = st.number_input("ctDNA Concentration (ng/mL)", min_value=0.0, max_value=5.0, value=0.25, format="%.4f")
            
            st.write("---")
            
            with st.expander("⚙️ Configuración Avanzada: Panel Genómico Multiplex (15 Sondas CRISPR)"):
                st.caption("Ajuste de niveles moleculares Beta detectados.")
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    g1 = st.slider("Sonda Multiplex Alpha-01", 0.0, 1.0, 0.05, step=0.01)
                    g2 = st.slider("Sonda Multiplex Alpha-02", 0.0, 1.0, 0.01, step=0.01)
                    g3 = st.slider("Sonda Multiplex Alpha-03", 0.0, 1.0, 0.01, step=0.01)
                with col_g2:
                    g4 = st.slider("Sonda Multiplex Alpha-04", 0.0, 1.0, 0.01, step=0.01)
                    g5 = st.slider("Sonda Multiplex Alpha-05", 0.0, 1.0, 0.01, step=0.01)
                    g6 = st.slider("Sonda Multiplex Alpha-06", 0.0, 1.0, 0.01, step=0.01)

            st.write("##")
            if st.button("Calcular Dictamen Clínico Multiplex", use_container_width=True, type="primary"):
                st.info("Procesando matriz molecular de manera encriptada y segura...")

    # ---- COLUMNA DERECHA: CONTENEDOR NATIVO SEGURO ----
    with col_derecha:
        with st.container(border=True):
            st.markdown('<p style="font-size: 15px; font-weight:700; color:#0F172A; text-transform:uppercase; letter-spacing:0.5px; margin-top:5px; margin-bottom:15px;">📊 Cohort Density Mapping & Patient Positioning</p>', unsafe_allow_html=True)
            
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
                margin=dict(l=10, r=10, t=10, b=10), height=260, plot_bgcolor='white', paper_bgcolor='white',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
                xaxis=dict(showgrid=True, gridcolor='#F1F5F9', range=[0, 0.75]), yaxis=dict(showgrid=False, showticklabels=False)
            )
            st.plotly_chart(fig_cohort, use_container_width=True)

            st.write("---")
            st.markdown('<p style="font-size: 13px; font-weight:700; color:#0F172A; margin-bottom:5px;">📥 Data Ingestion & Archiving</p>', unsafe_allow_html=True)
            archivo_cargado = st.file_uploader("Upload sequencer", type=["csv", "xlsx"], label_visibility="collapsed")
            
            st.write("##")
            st.download_button(
                label="📄 Download Institutional Analytical Dossier (PDF)",
                data=pdf_data,
                file_name="METHYLOX_Dossier_Clinico.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# --- PESTAÑAS SECUNDARIAS (HTML LIMPIO Y AISLADO) ---
elif nav_selection == "Samples Database":
    st.markdown("""
    <div class="executive-card">
        <h3 style="margin:0; color:#0F172A; font-size:20px;">🗄️ Sample Records & Permanent Database</h3>
        <hr style="border:0; border-top:1px solid #E2E8F0; margin:15px 0;">
        <p style="margin:0; color:#64748B; font-size:14px;">Accediendo de forma limpia y directa al repositorio indexado...</p>
    </div>
    """, unsafe_allow_html=True)

elif nav_selection == "AI Analysis Hub":
    st.markdown("""
    <div class="executive-card">
        <h3 style="margin:0; color:#0F172A; font-size:20px;">🧠 AI Epigenetic Analysis Engine</h3>
        <hr style="border:0; border-top:1px solid #E2E8F0; margin:15px 0;">
        <p style="margin:0; color:#64748B; font-size:14px;">Matriz analítica lista para procesamiento ómico.</p>
    </div>
    """, unsafe_allow_html=True)

elif nav_selection == "Clinical Reports":
    st.markdown("""
    <div class="executive-card">
        <h3 style="margin:0; color:#0F172A; font-size:20px;">📋 Reporting & De-Risk Dossier Log</h3>
        <hr style="border:0; border-top:1px solid #E2E8F0; margin:15px 0;">
        <p style="margin:0; color:#64748B; font-size:14px;">Dossier Clínico anonimizado disponible para descarga institucional.</p>
    </div>
    """, unsafe_allow_html=True)

elif nav_selection == "System Settings":
    st.markdown("""
    <div class="executive-card">
        <h3 style="margin:0; color:#0F172A; font-size:20px;">⚙️ Platform Security & Parameters</h3>
        <hr style="border:0; border-top:1px solid #E2E8F0; margin:15px 0;">
        <p style="margin:0; color:#64748B; font-size:14px;">Área de seguridad restringida y encriptación de credenciales.</p>
    </div>
    """, unsafe_allow_html=True)
