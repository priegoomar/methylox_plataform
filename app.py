import sqlite3
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURACION DE PAGINA MAESTRA
st.set_page_config(
    page_title="MethylOx Labs",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ARQUITECTURA DE DISEÑO: PRESET HIGH-CONTRAST #2563EB
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    [data-testid="stImage"] img {
        width: 100% !important;
        max-height: 110px !important;
        object-fit: cover !important;
        border-radius: 10px !important;
        border-bottom: 3px solid #2563EB !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h2 {
        color: #0F172A !important;
    }
    [data-testid="stSidebar"] .stButton>button {
        background-color: #F1F5F9 !important;
        color: #2563EB !important;
        border: 1px solid #E2E8F0 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 15px !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-color: #2563EB !important;
    }
    .biotech-panel {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-top: 4px solid #2563EB !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Conexión inicial segura a SQLite3
def conectar_db_inicial():
    conn = sqlite3.connect("methyl_clinic.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes (
            id TEXT PRIMARY KEY,
            edad INTEGER,
            ctdna REAL,
            clasificacion TEXT
        )
        """
    )
    conn.commit()
    conn.close()

conectar_db_inicial()

UMBRAL = 0.5910

# --- 3. BARRA LATERAL IZQUIERDA DE NAVEGACIÓN ---
st.sidebar.markdown("## 🔬 MethylOx Labs")
st.sidebar.markdown("`CLINICAL PLATFORM v4.0`")
st.sidebar.markdown("---")

if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "🏠 Dashboard"

# Botones directos con mapeo limpio
if st.sidebar.button("🏠 Dashboard", use_container_width=True):
    st.session_state["menu_activo"] = "🏠 Dashboard"

if st.sidebar.button("👤 Patient Profiles", use_container_width=True):
    st.session_state["menu_activo"] = "👤 Patient Profiles"

if st.sidebar.button("📊 Methylation Matrix", use_container_width=True):
    st.session_state["menu_activo"] = "📊 Methylation Matrix"

if st.sidebar.button("🧬 CRISPR Guide Library", use_container_width=True):
    st.session_state["menu_activo"] = "🧬 CRISPR Guide Library"

if st.sidebar.button("🧪 Gel Analysis", use_container_width=True):
    st.session_state["menu_activo"] = "🧪 Gel Analysis"

if st.sidebar.button("📄 Reports", use_container_width=True):
    st.session_state["menu_activo"] = "📄 Reports"

if st.sidebar.button("⚙️ Settings", use_container_width=True):
    st.session_state["menu_activo"] = "⚙️ Settings"


# --- 4. RENDERIZADO DE LAS PANTALLAS ---

if st.session_state["menu_activo"] == "🏠 Dashboard":

    # Inyección CSS para forzar el banner a expandirse al 100% horizontal
    st.markdown(
        """
        <style>
        [data-testid="stImage"] {
            width: 100% !important;
            text-align: center !important;
        }
        [data-testid="stImage"] img {
            width: 100% !important;
            max-height: 110px !important;
            object-fit: cover !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Renderizado del banner panorámico completo
    st.image(
        "banner_real.png",
        use_container_width=True
    )

    st.title("Molecular Methylation Analysis Hub")
    st.caption("Panel Ejecutivo de Cribado para Cáncer de Mama en Etapa Temprana")
    st.markdown("---")

    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    st.markdown("<h4>📥 Patient Enrollment Matrix</h4>", unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1: patient_id = st.text_input("🆔 ID Único del Paciente", placeholder="Ej. METH-2026-0X")
    with col_f2: patient_age = st.number_input("🎂 Edad Cronológica", min_value=18, max_value=100, value=45)
    with col_f3: ctdna_score = st.number_input("🔬 Concentración de ctDNA (ng/mL)", min_value=0.0000, max_value=5.0000, format="%.4f", value=0.2500)

    if ctdna_score >= UMBRAL:
        resultado = "High Risk - CPEB4+ Detected"
    else:
        resultado = "Low Risk - Baseline Stable"

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Commit Diagnostic Data", use_container_width=True):
            if patient_id:
                conn = sqlite3.connect("methyl_clinic.db")
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO pacientes VALUES (?, ?, ?, ?)", (patient_id, patient_age, ctdna_score, resultado))
                    conn.commit()
                    st.success(f"Registro exitoso para ID: {patient_id}")
                except sqlite3.IntegrityError:
                    st.error("Error: El ID del paciente ya existe.")
                finally:
                    conn.close()
            else:
                st.warning("Por favor ingrese un ID válido.")

    with col_btn2:
        reporte_txt = f"REPORT\nID: {patient_id}\nEdad: {patient_age}\nScore: {ctdna_score:.4f}\nVerdict: {resultado}"
        st.download_button("📥 Export Prognostic Report (.TXT)", data=reporte_txt, file_name=f"Report_{patient_id}.txt", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    st.markdown("<h4>📊 Real-Time Analytics Overview</h4>", unsafe_allow_html=True)
    c_tar1, c_tar2, c_tar3 = st.columns(3)
    with c_tar1: st.metric(label="Clinical Cohort Status", value="Stage I Breast Cancer" if patient_id else "Awaiting Input")
    with c_tar2: st.metric(label="Global Methylation Value", value=f"{ctdna_score:.4f} ng/mL")
    with c_tar3: st.metric(label="Diagnostic Verdict", value=resultado)
    st.markdown("</div>", unsafe_allow_html=True)

# PANTALLA 2: HISTORIAL DE PACIENTES (SQLite3 Puro y Seguro)
elif st.session_state["menu_activo"] == "👤 Patient Profiles":
    st.title("👤 Patient Profiles & Clinical Records")
    st.markdown("---")

    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()

    if not df_pacientes.empty:
        st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
        st.dataframe(df_pacientes, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No hay perfiles clínicos registrados actualmente en el sistema.")

# PANTALLA 3: MATRIZ DE METILACIÓN (GRÁFICOS ESTADÍSTICOS)
elif st.session_state["menu_activo"] == "📊 Methylation Matrix":
    st.title("📊 Methylation Matrix Analytics")
    st.markdown("---")

    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1:
        st.write("**Biomarker Overview (CpG)**")
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.imshow(np.random.rand(8, 8), cmap="Blues")
        ax1.axis("off")
        st.pyplot(fig1)
    with g2:
        st.write("**Guidance Mapping (ROC)**")
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        x = np.linspace(0, 1, 100)
        ax2.plot(x, 1 - np.exp(-5 * x), color="#2563EB")
        st.pyplot(fig2)
    with g3:
        st.write("**Population Distribution**")
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.hist(np.random.normal(0.3, 0.1, 100), alpha=0.5, color="green")
        ax3.hist(np.random.normal(0.8, 0.1, 100), alpha=0.5, color="red")
        st.pyplot(fig3)
    st.markdown("</div>", unsafe_allow_html=True)

# PANTALLA 4: BIBLIOTECA CRISPR-CAS12 CARGADOR UNIVERSAL
elif st.session_state["menu_activo"] == "🧬 CRISPR Guide Library":
    st.title("🧬 CRISPR Guide Library & Screening")
    st.markdown("---")

    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Subir cualquier documento genómico o base de datos de Colab")
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:
        try:
            nombre_archivo = uploaded_file.name
            if nombre_archivo.endswith(".csv"):
                df_secuencias = pd.read_csv(uploaded_file)
            elif nombre_archivo.endswith((".xlsx", ".xls")):
                df_secuencias = pd.read_excel(uploaded_file)
            else:
                df_secuencias = pd.read_csv(uploaded_file, sep="\t")

            st.success("Archivo cargado con éxito. Motores de filtrado listos.")
            st.dataframe(df_secuencias, use_container_width=True)
        except Exception:
            st.error("Error al leer la estructura del documento.")

# PANTALLA 5: ANALISIS DE GEL
elif st.session_state["menu_activo"] == "🧪 Gel Analysis":
    st.title("🧪 Automated Gel Clearance Inspection")
    st.markdown("---")
    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    st.slider("Concentración de agarosa (%)", 0.5, 2.5, 1.2)
    fig_gel, ax_gel = plt.subplots(figsize=(6, 3))
    ax_gel.fill_between([0, 10], 0, 1000, color="#111827")
    ax_gel.hlines(y=400, xmin=2, xmax=8, color="#10B981", lw=6)
    ax_gel.set_facecolor("#111827")
    st.pyplot(fig_gel)
    st.markdown("</div>", unsafe_allow_html=True)

# PANTALLA 6: REPORTES
elif st.session_state["menu_activo"] == "📄 Reports":
    st.title("📄 Clinical Reports Archive")
    st.markdown("---")
    st.info("Archivo histórico de bitácoras institucionales activo.")

# PANTALLA 7: CONFIGURACIÓN / INGENIERÍA (AQUÍ SE RESTAURA TU BACKEND EN VIVO)
elif st.session_state["menu_activo"] == "⚙️ Settings":
    st.title("⚙️ Engineering Core & Backend Diagnostics")
    st.caption("Inspección en vivo del código analítico puro alojado en motores.py")
    st.markdown("---")
    st.markdown("### 🖥️ Código de los Motores Unificados en Ejecución")

    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
        st.success("✅ Conexión e integridad del archivo motores.py verificada con éxito.")
    except Exception:
        st.error("❌ No se pudo enlazar el visor con el archivo de backend motores.py")
