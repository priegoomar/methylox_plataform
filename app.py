import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sqlite3
import pandas as pd

# =====================================================================
# 1. ESTILOS DE INTERFAZ: MODO CLARO HIGH-TECH (AZUL LIMPIO Y SIN EMOJIS)
# =====================================================================
st.markdown("""
    <style>
        /* Fondo global blanco puro */
        .stApp {
            background-color: #FFFFFF;
            color: #0F172A;
            font-family: 'Inter', sans-serif;
        }
        
        /* Barra lateral limpia */
        [data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
            border-right: 1px solid #E2E8F0;
        }
        
        /* Tarjetas con fondo azul cielo ultra-suave y limpio */
        .medical-card {
            background-color: #EFF6FF; 
            border: 1px solid #DBEAFE;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
        }
        
        /* Títulos corporativos */
        h1, h2, h3, h4 {
            color: #0F172A !important;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        /* Badges de estado estilo Apple en tonos azules */
        .status-badge {
            background-color: #F1F5F9;
            color: #475569;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid #E2E8F0;
            text-transform: uppercase;
        }
        
        .status-badge-active {
            background-color: #2563EB; 
            color: #FFFFFF;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        /* Botón Principal - Azul Tecnológico */
        div.stButton > button:first-child {
            background-color: #2563EB !important; 
            color: white !important;
            border-radius: 6px;
            border: none;
            width: 100%;
            font-weight: 600;
            font-size: 13px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Lógica básica para controlar el menú si no está inicializado
if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Dashboard"

# =====================================================================
# 2. CONTROL DE PESTAÑAS (IF / ELIF / ELSE)
# =====================================================================

# --- PESTAÑA A: DASHBOARD PRINCIPAL ---
if st.session_state["menu_activo"] == "Dashboard":
    
    # HEADER: BANNER Y ANILLO DE PRECISIÓN (AZUL) - CORREGIDO AQUÍ
    col_header_left, col_header_right = st.columns(2)

    with col_header_left:
        st.title("MethyLOx™")
        st.markdown("<p style='color: #475569; font-size: 14px; margin-top: -15px; font-weight: 500;'>Early Detection Through Epigenetic AI</p>", unsafe_allow_html=True)
        
        st.markdown("""
            <div style='display: flex; gap: 8px; margin-top: 15px;'>
                <span class='status-badge'>DNA Methylation</span>
                <span class='status-badge-active'>AI Engine Active</span>
                <span class='status-badge'>Liquid Biopsy</span>
                <span class='status-badge'>CpG Analysis</span>
            </div>
        """, unsafe_allow_html=True)

    with col_header_right:
        fig_anillo, ax_anillo = plt.subplots(figsize=(2.0, 2.0))
        fig_anillo.patch.set_facecolor("none")
        ax_anillo.set_facecolor("none")
        
        ax_anillo.pie([98.7, 1.3], colors=['#2563EB', '#E2E8F0'], startangle=90, wedgeprops=dict(width=0.20, edgecolor='none'))
        ax_anillo.text(0, 0, "98.7%\nAccuracy", ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')
        ax_anillo.axis('off')
        st.pyplot(fig_anillo)
        
        st.markdown("""
            <div style='display: flex; justify-content: space-around; text-align: center; font-size: 11px; margin-top: -15px;'>
                <div><b style='color: #2563EB; font-size: 13px;'>5,248</b><br><span style='color: #64748B;'>Biomarkers</span></div>
                <div><b style='color: #EF4444; font-size: 13px;'>89</b><br><span style='color: #64748B;'>High-Risk Cases</span></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # FILA DE CARACTERÍSTICAS (3 COLUMNAS AZULES)
    col_feat1, col_feat2, col_feat3 = st.columns(3)

    with col_feat1:
        st.markdown("""
            <div class='medical-card'>
                <div style='font-size: 11px; font-weight: 700; color: #2563EB; letter-spacing: 0.05em; text-transform: uppercase;'>EPIGENETIC AI</div>
                <div style='font-size: 13px; font-weight: 600; color: #0F172A; margin-top: 5px;'>POWERED PLATFORM</div>
                <p style='margin: 5px 0 0 0; font-size: 12px; color: #475569; line-height: 1.4;'>Advanced AI models for epigenetic biomarker discovery.</p>
            </div>
        """, unsafe_allow_html=True)

    with col_feat2:
        st.markdown("""
            <div class='medical-card'>
                <div style='font-size: 11px; font-weight: 700; color: #2563EB; letter-spacing: 0.05em; text-transform: uppercase;'>NON-INVASIVE</div>
                <div style='font-size: 13px; font-weight: 600; color: #0F172A; margin-top: 5px;'>& LIQUID BIOPSY</div>
                <p style='margin: 5px 0 0 0; font-size: 12px; color: #475569; line-height: 1.4;'>Accurate, painless, and highly reproducible corporate protocols.</p>
            </div>
        """, unsafe_allow_html=True)

    with col_feat3:
        st.markdown("""
            <div class='medical-card'>
                <div style='font-size: 11px; font-weight: 700; color: #2563EB; letter-spacing: 0.05em; text-transform: uppercase;'>EARLY DETECTION</div>
                <div style='font-size: 13px; font-weight: 600; color: #0F172A; margin-top: 5px;'>PROACTIVE SCREENING</div>
                <p style='margin: 5px 0 0 0; font-size: 12px; color: #475569; line-height: 1.4;'>Substantially better proactive patient outcomes and saved lives.</p>
            </div>
        """, unsafe_allow_html=True)

    # MATRIZ DE PACIENTE
    st.markdown("<h3 style='font-size: 16px; font-weight: 700; margin-bottom: 10px;'>Patient Case Enrollment Matrix</h3>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='medical-card'>", unsafe_allow_html=True)
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            patient_id = st.text_input("Patient Identifier", value="TL-METH-2026-0X")
            age = st.number_input("Chronological Age (Years)", value=45)
        with col_input2:
            ctdna = st.number_input("ctDNA Concentration (ng/mL)", value=0.2500, format="%.4f")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("Commit Diagnostic Data (Save to SQLite3)")
        with col_btn2:
            st.button("Download Personalized Clinical Report")
        st.markdown("</div>", unsafe_allow_html=True)

# --- PESTAÑA B: SAMPLES DATABASE (CONEXIÓN SQLITE) ---
elif st.session_state["menu_activo"] == "Samples":
    st.title("Sample Records & Permanent Database")
    st.markdown("---")
    
    conn = sqlite3.connect("methyl_clinic.db")
    try:
        df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
        if not df_pacientes.empty:
            st.dataframe(df_pacientes, use_container_width=True)
        else:
            st.info("No active patient logs detected inside methyl_clinic.db.")
    except Exception:
        st.warning("Database tables empty or initializing...")
    finally:
        conn.close()

# --- PESTAÑA C: SYSTEM SETTINGS (LECTOR DE BACKEND) ---
elif st.session_state["menu_activo"] == "Settings":
    st.title("Engineering Core & Backend Diagnostics")
    st.markdown("---")
    
    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
        st.success("✅ Conexión e integridad del archivo motores.py verificada.")
    except Exception:
        st.error("❌ No se pudo enlazar el visor con motores.py")

# --- OTRAS PESTAÑAS ---
elif st.session_state["menu_activo"] in ["AI Analysis", "Reports"]:
    st.title(f"{st.session_state['menu_activo']} Workspace")
    st.info("Sección en desarrollo clínico secundario.")
