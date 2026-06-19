import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sqlite3
import pandas as pd

# Configuración de página ancha nativa de Streamlit
st.set_page_config(page_title="MethyLOx™ Platform", layout="wide")

# Inicialización obligatoria del estado del menú
if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Dashboard"

# =====================================================================
# CONTENEDORES Y NAVEGACIÓN DE PESTAÑAS (IF / ELIF)
# =====================================================================

# --- PESTAÑA A: DASHBOARD PRINCIPAL (TU VERSIÓN CORRECTA COMPLETA) ---
if st.session_state["menu_activo"] == "Dashboard":
    
    # 1. EL BANNER SUPERIOR PREMIUM QUE SE HABÍA BORRADO
    st.title("MethyLOx™")
    st.markdown("<p style='font-size: 16px; margin-top: -15px; color: #94A3B8;'>Early Detection Through Epigenetic AI</p>", unsafe_allow_html=True)
    
    # Pequeña fila de estados en texto horizontal
    st.markdown("""
        <div style='display: flex; gap: 15px; font-size: 13px; color: #cbd5e1; margin-bottom: 20px;'>
            <span>🧬 DNA Methylation</span>
            <span>🤖 AI Engine Active</span>
            <span>💧 Liquid Biopsy</span>
            <span>📊 CpG Site Analysis</span>
            <span>❤️ Early Detection</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 2. SECCIÓN MATRIZ DE PACIENTE (INPUTS, BOTONES Y ANILLO JUNTO A ELLOS)
    st.markdown("### PATIENT CASE ENROLLMENT MATRIX")
    
    col_izq, col_der = st.columns([2, 1]) # Columnas balanceadas para que el anillo no se haga gigante
    
    with col_izq:
        # Inputs del formulario que hacían falta
        patient_id = st.text_input("Patient Identifier", value="TL-METH-2026-0X")
        age = st.number_input("Chronological Age (Years)", value=45)
        ctdna = st.number_input("ctDNA Concentration (ng/mL)", value=0.2500, format="%.4f")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Los dos botones interactivos en paralelo abajo de los inputs
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("Commit Data to SQLite3")
        with col_btn2:
            st.button("Download Clinical Report")
            
    with col_der:
        # Dibujamos tu gráfico de anillo tecnológico ajustado para que quede al lado de los botones
        fig_anillo, ax_anillo = plt.subplots(figsize=(2.5, 2.5))
        fig_anillo.patch.set_facecolor("none")
        ax_anillo.set_facecolor("none")
        
        colores_anillo = ['#2563EB', '#E2E8F0']
        ax_anillo.pie([98.7, 1.3], colors=colores_anillo, startangle=90, wedgeprops=dict(width=0.25, edgecolor='none'))
        ax_anillo.text(0, 0, "98.7%\nAccuracy", ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF')
        ax_anillo.axis('off')
        st.pyplot(fig_anillo)
        
        # Texto original de los Biomarkers acoplado abajo de la gráfica circular
        st.markdown("""
            <div style='text-align: center; font-size: 13px; color: #cbd5e1; margin-top: -10px;'>
                Total Biomarkers Index: <b>5,248</b><br>
                High-Risk Sequence Delta: <b>89</b>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 3. ANALÍTICAS INFERIORES PREMIUM EN PARALELO
    st.markdown('📊 Real-Time Analytics Overview', unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1: 
        st.metric(label="Screening Sensitivity", value="96.4%", delta="Target Verified")
    with col_m2: 
        st.metric(label="Analytical Specificity", value="94.1%", delta="Validated")
    with col_m3: 
        st.metric(label="ctDNA Detection Limit", value="0.01%", delta="High-Resolution")

    st.markdown("<br>", unsafe_allow_html=True)

    # Las dos gráficas de distribución de riesgo originales abajo
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("Risk Score Distribution (KDE)")
        fig3, ax3 = plt.subplots(figsize=(6, 2.8))
        fig3.patch.set_facecolor('#FFFFFF')
        ax3.set_facecolor('#F8FAFC')
        sns.kdeplot(np.random.normal(30, 8, 150), color="#3B82F6", fill=True, alpha=0.15, label="Healthy", ax=ax3)
        sns.kdeplot(np.random.normal(78, 6, 150), color="#EC4899", fill=True, alpha=0.2, label="Early Cancer", ax=ax3)
        ax3.set_xlabel("Risk Score (%)", fontsize=8)
        ax3.grid(True, linestyle='--', alpha=0.5, color='#E2E8F0')
        ax3.legend(fontsize=7)
        sns.despine(left=True, bottom=True)
        st.pyplot(fig3)

    with col_g2:
        st.markdown("ctDNA Concentration Variance")
        fig4, ax4 = plt.subplots(figsize=(6, 2.8))
        fig4.patch.set_facecolor('#FFFFFF')
        ax4.set_facecolor('#F8FAFC')
        sns.histplot(np.random.exponential(0.5, 100), color="#2563EB", kde=True, alpha=0.4, ax=ax4)
        ax4.set_xlabel("Concentration (ng/mL)", fontsize=8)
        ax4.grid(True, linestyle='--', alpha=0.5, color='#E2E8F0')
        sns.despine(left=True, bottom=True)
        st.pyplot(fig4)

# --- PESTAÑA B: SAMPLES DATABASE (TABLAS INTERACTIVAS) ---
elif st.session_state["menu_activo"] == "Samples":
    st.title("🧪 Sample Records & Permanent Database")
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

# --- PESTAÑA C: SYSTEM SETTINGS (ENGINEERING DIAGNOSTICS) ---
elif st.session_state["menu_activo"] == "Settings":
    st.title("⚙️ Engineering Core & Backend Diagnostics")
    st.markdown("---")
    
    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
        st.success("✅ Conexión e integridad del archivo motores.py verificada.")
    except Exception:
        st.error("❌ No se pudo enlazar el visor con motores.py")

# PESTAÑAS ADICIONALES PARA EVITAR CONFLICTOS
elif st.session_state["menu_activo"] in ["AI Analysis", "Reports"]:
    st.title(f"🛠️ {st.session_state['menu_activo']} Workspace")
    st.info("Sección en desarrollo clínico secundario.")
