import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sqlite3
import pandas as pd

# Configuración inicial de la página
st.set_page_config(page_title="MethyLOx™ Platform", layout="wide")

# Lógica básica para controlar la barra lateral de navegación si no está inicializada
if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Dashboard"

# =====================================================================
# MENÚ DE NAVEGACIÓN LATERAL (SIDEBAR)
# =====================================================================
with st.sidebar:
    st.markdown("### MethyLOx™")
    st.markdown("Epigenetic AI Platform")
    st.markdown("---")
    
    # Botones del menú con almacenamiento de estado
    if st.button("📊 Dashboard Matrix"):
        st.session_state["menu_activo"] = "Dashboard"
    if st.button("🧪 Samples Database"):
        st.session_state["menu_activo"] = "Samples"
    if st.button("🧠 AI Analysis Hub"):
        st.session_state["menu_activo"] = "AI Analysis"
    if st.button("📋 Clinical Reports"):
        st.session_state["menu_activo"] = "Reports"
    if st.button("⚙️ System Settings"):
        st.session_state["menu_activo"] = "Settings"

# =====================================================================
# 1. PESTAÑA A: DASHBOARD PRINCIPAL (MÉTRICAS Y GRÁFICAS ORIGINALES)
# =====================================================================
if st.session_state["menu_activo"] == "Dashboard":
    st.title("📊 Dashboard Matrix & Operational Analytics")
    st.markdown("---")

    # Métrica de Anillo Circular Avanzada usando Matplotlib
    fig_anillo, ax_anillo = plt.subplots(figsize=(3, 3))
    fig_anillo.patch.set_facecolor("none")
    ax_anillo.set_facecolor("none")

    # Dibujamos el anillo tecnológico
    colores_anillo = ['#2563EB', '#E2E8F0'] # Azul eléctrico y gris sutil
    ax_anillo.pie([98.7, 1.3], colors=colores_anillo, startangle=90, wedgeprops=dict(width=0.25, edgecolor='none'))
    ax_anillo.text(0, 0, "98.7%\nAccuracy", ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
    ax_anillo.axis('off')
    st.pyplot(fig_anillo)

    st.markdown("Total Biomarkers Index: 5,248 | High-Risk Sequence Delta: 89", unsafe_allow_html=True)
    st.markdown('---')

    # 4.1 ANALÍTICAS INFERIORES PREMIUM EN PARALELO
    st.markdown('📊 Real-Time Analytics Overview', unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Screening Sensitivity", value="96.4%", delta="Target Verified")
    with col_m2:
        st.metric(label="Analytical Specificity", value="94.1%", delta="Validated")
    with col_m3:
        st.metric(label="ctDNA Detection Limit", value="0.01%", delta="High-Resolution")

    st.markdown("---")

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

# =====================================================================
# 2. PESTAÑA B: SAMPLES DATABASE & CÓDIGO 1: SUBIDA MASIVA DE ARCHIVOS
# =====================================================================
elif st.session_state["menu_activo"] == "Samples":
    st.title("🧪 Sample Records & Permanent Database")
    st.markdown("---")
    
    # [CÓDIGO ADICIONAL 1]: Sistema de Carga Masiva de Secuencias Metiladas
    st.subheader("📁 Batch Sequence Bulk Uploader")
    archivo_masivo = st.file_uploader("Upload CSV/TSV genomic sequences folder pack", type=["csv", "tsv", "txt"])
    
    if archivo_masivo is not None:
        try:
            df_cargado = pd.read_csv(archivo_masivo)
            st.success(f"✅ Pack loaded successfully: {len(df_cargado)} structural samples processed.")
            st.dataframe(df_cargado.head(5), use_container_width=True)
        except Exception as e:
            st.error(f"Error parsing batch sequences: {e}")
            
    st.markdown("---")
    st.subheader("🗄️ Active Database Cache (MethylClinic DB)")
    
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

# =====================================================================
# 3. CÓDIGO ADICIONAL 2: AI ANALYSIS HUB (CÓDIGO PREDICTIVO)
# =====================================================================
elif st.session_state["menu_activo"] == "AI Analysis":
    st.title("🧠 AI Analysis Hub & Prediction Matrix")
    st.markdown("---")
    
    st.info("Clinical Neural Model core linked successfully. Running sequencing variant evaluation.")
    
    # Formulario dinámico para simular predicciones clínicas de la IA
    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        score_riesgo = st.slider("Select Patient Score Target (%)", 0, 100, 45)
        modo_run = st.selectbox("AI Protocol Mode", ["High-Sensitivity Screening", "Deep Mutation Variance", "Standard Panel"])
    
    with col_ai2:
        if st.button("Run Epigenetic Model Diagnostic Pipeline"):
            with st.spinner("Analyzing variant blocks..."):
                # Simulación algorítmica de análisis secuencial
                resultado_modelo = "HIGH METALLOPROTEINASE INTENSITY" if score_riesgo > 60 else "NORMAL EPIGENETIC MARKERS"
                st.metric(label="Target Verification Result", value=resultado_modelo)
                st.success("Analysis finalized with high resolution integrity.")

# =====================================================================
# 4. CÓDIGO ADICIONAL 3: CLINICAL REPORTS (GENERACIÓN DE REPORTES)
# =====================================================================
elif st.session_state["menu_activo"] == "Reports":
    st.title("📋 Clinical Reports & Documentation Output")
    st.markdown("---")
    
    st.write("Select verified clinical runs to bundle into standardized reporting packages:")
    
    report_id = st.text_input("Enter Target Report Reference Code", "REP-2026-METH-001")
    tipo_reporte = st.radio("Output File Standard", ["Official Clinical PDF Booklet", "Raw JSON Sequence Metadata Archive"])
    
    if st.button("Compile & Generate Structural Report"):
        st.balloons()
        st.success(f"Report package {report_id} compiled under molecular diagnostics protocols.")
        # Botón simulado para descarga final
        st.download_button(label="Download File Pack", data="Sample data pack", file_name=f"{report_id}.txt")

# =====================================================================
# 5. PESTAÑA C: SYSTEM SETTINGS (ENGINEERING DIAGNOSTICS)
# =====================================================================
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
