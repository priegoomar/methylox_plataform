import io
import os
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN MAESTRA Y BLINDAJE DE CONTRASTE RADICAL
# ==============================================================================
st.set_page_config(
    page_title="MethylOx™",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de CSS Forzado - Contraste Absoluto
st.markdown("""
<style>
    /* 1. Fondo de la aplicación */
    .stApp {
        background-color: #F8FAFC !important;
    }

    /* 2. Reset de cabeceras y márgenes superiores */
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
    
    /* 3. BARRA LATERAL - FONDO OSCURO */
    [data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 2px solid #1E293B;
    }
    
    /* Remover título nativo invisible y ajustar espacio del menú */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 12px !important; /* Espacio generoso entre bloques */
        padding: 0px 10px !important;
    }
    
    /* DISEÑO DE BOTÓN SÓLIDO INACTIVO (MÁXIMA VISIBILIDAD) */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background-color: #1E293B !important; /* Bloque gris claro visible sobre fondo negro */
        border: 1px solid #475569 !important; /* Borde claro definido */
        border-radius: 8px !important;
        padding: 14px 18px !important;
        margin: 0px !important;
        width: 100% !important;
        cursor: pointer !important;
        display: block !important;
        transition: all 0.15s ease-in-out;
    }
    
    /* Eliminar el círculo de selección de raíz */
    [data-testid="stSidebar"] [data-testid="stRadio"] label div:first-child {
        display: none !important;
    }
    
    /* SELECTOR PROFUNDO: Fuerza a cualquier texto interno inactivo a ser BLANCO PURO */
    [data-testid="stSidebar"] [data-testid="stRadio"] label * {
        color: #FFFFFF !important; 
        font-weight: 700 !important;
        font-size: 14px !important;
        text-decoration: none !important;
    }
    
    /* EFECTO HOVER (Al pasar el cursor por encima) */
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background-color: #334155 !important;
        border-color: #38BDF8 !important;
    }
    
    /* BOTÓN SELECCIONADO / ACTIVO (ILUMINACIÓN RADICAL) */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[data-checked="true"] label {
        background-color: #0284C7 !important; /* Fondo azul rey brillante */
        border-color: #38BDF8 !important;
        box-shadow: 0px 4px 12px rgba(2, 132, 199, 0.4) !important;
    }
    
    /* SELECTOR PROFUNDO ACTIVO: Fuerza al texto seleccionado a mantener brillo e idoneidad */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[data-checked="true"] label * {
        color: #FFFFFF !important; /* Texto blanco puro sobre el fondo azul brillante */
        font-weight: 800 !important;
    }
    
    /* Sliders de la barra lateral */
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {
        color: #94A3B8 !important;
        font-size: 12px !important;
    }

    /* 4. PROTECCIÓN DEL BANNER */
    button[title="View fullscreen"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stImage"] img {
        pointer-events: none !important;
        user-select: none !important;
        border-radius: 0px 0px 12px 12px !important;
    }

    /* 5. TARJETAS DE CONTENIDO PRINCIPAL */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
        margin-top: 15px !important;
        padding: 6px !important;
    }

    /* 6. BOTONES DE ACCIÓN */
    div.stButton > button:first-child {
        background-color: #0284C7 !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #0369A1 !important;
    }

    /* Estilo secundario */
    .executive-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-top: 15px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# GENERACIÓN DE BUFFER DE ARCHIVO COMPATIBLE (PDF EN MEMORIA)
# ==============================================================================
buffer_pdf = io.BytesIO()
buffer_pdf.write(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n1 0 obj\n< Badger Catalog >\nendobj\n2 0 obj\n<</Type/Pages/Count 1/Kids[3 0 R]>>\nendobj\n3 0 obj\n<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 55>>\nstream\nBT\n/F1 12 Tf\n72 712 Td\n(MethylOx Institutional Analytical Dossier - Protected Content) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000015 00000 n\n0000000068 00000 n\n0000000120 00000 n\n0000000219 00000 n\ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n326\n%%EOF")
pdf_data = buffer_pdf.getvalue()

# ==============================================================================
# BARRA LATERAL (BRANDING CORPORATIVO REFORZADO)
# ==============================================================================
st.sidebar.markdown("""
<div style="padding: 10px 10px; border-bottom: 1px solid #1E293B; margin-bottom: 25px;">
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
    st.sidebar.markdown('<p style="font-size:11px; font-weight:700; color:#64748B !important; letter-spacing:1px; text-transform:uppercase; margin-bottom:10px; padding-left:10px;">Monitor de Canales Activos</p>', unsafe_allow_html=True)
    slider_ch1 = st.sidebar.slider("Canal Ómico CH-01", 0.0, 1.0, 0.45)
    slider_ch2 = st.sidebar.slider("Canal Ómico CH-02", 0.0, 1.0, 0.62)
    slider_ch3 = st.sidebar.slider("Canal Ómico CH-03", 0.0, 1.0, 0.18)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding: 5px 10px;">
    <p style="margin: 0; font-size: 10px; font-weight: 700; color: #64748B !important; text-transform: uppercase; letter-spacing: 1px;">SYSTEM STATUS</p>
    <div style="display: flex; align-items: center; gap: 8px; margin-top: 6px;">
        <span style="height: 7px; width: 7px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
        <span style="font-size: 12px; font-weight: 600; color: #E2E8F0 !important;">Core Engine Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# CONTENIDO PRINCIPAL
# ==============================================================================
st.image("1000199352.png", use_container_width=True, output_format="PNG")

if nav_selection == "Dashboard Matrix":
    col_izquierda, col_derecha = st.columns([12, 12], gap="large")
    
    with col_izquierda:
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
            if st.button("Calcular Dictamen Clínico Multiplex", use_container_width=True):
                st.info("Procesando matriz molecular de manera encriptada y segura...")

    with col_derecha:
        with st.container(border=True):
            st.markdown('<p style="font-size: 15px; font-weight:700; color:#0F172A; text-transform:uppercase; letter-spacing:0.5px; margin-top:5px; margin-bottom:15px;">📊 Cohort Density Mapping & Patient Positioning</p>', unsafe_allow_html=True)
            
            x_axis = np.linspace(0.0, 1.0, 100)
            healthy_density = np.exp(-((x_axis - 0.05) ** 2) / (2 * 0.03 ** 2))
            tumor_density = np.exp(-((x_axis - 0.45) ** 2) / (2 * 0.15 ** 2))

            fig_cohort = go.Figure()
            fig_cohort.add_trace(go.Scatter(
                x=x_axis, y=healthy_density, mode='lines', name='Healthy Control',
                line=dict(color='#0284C7', width=2.5), fill='tozeroy', fillcolor='rgba(2, 132, 199, 0.02)'
            ))
            fig_cohort.add_trace(go.Scatter(
                x=x_axis, y=tumor_density, mode='lines', name='Oncological Cohort',
                line=dict(color='#F43F5E', width=2.5), fill='tozeroy', fillcolor='rgba(244, 63, 94, 0.02)'
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

# --- REPOSITORIO DE PESTAÑAS SECUNDARIAS ---
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
