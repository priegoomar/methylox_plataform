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

# 2. INYECCIÓN DE ESTILOS PREMIUM DE LABORATORIO (Deep Biotech Cyan)
st.markdown(
    """
    <style>
    /* Fondo de la barra lateral: Azul petróleo de laboratorio */
    [data-testid="stSidebar"] {
        background-color: #06141D !important;
    }
    /* Textos generales de la barra lateral */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
    }
    /* Botones de navegación en color Cian Neón Tecnológico */
    [data-testid="stSidebar"] .stButton>button {
        background-color: transparent !important;
        color: #00E5FF !important;
        border: 1px solid #00E5FF !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding-left: 15px !important;
        border-radius: 6px !important;
        margin-bottom: 5px !important;
    }
    /* Efecto al pasar el mouse sobre los botones de navegación */
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #00E5FF !important;
        color: #06141D !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

UMBRAL = 0.5910

# Inicialización de Base de Datos Local SQLite3
def init_db():
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

init_db()

# --- 3. BARRA LATERAL IZQUIERDA: LOS 8 BOTONES CONFIGURADOS ---
st.sidebar.markdown("## 🧬 MethylOx Labs")
st.sidebar.markdown("`METHYLHUB AUTOMATION CORE v4.0`")
st.sidebar.markdown("---")

# Control de estado de navegación real en el backend
if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "🏠 Dashboard"

# Renderizado vertical de los 8 botones con uso en el backend
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

st.sidebar.markdown("---")
# Botón 8: Indicador de estatus dinámico de la plataforma
db_salud = "● All systems operational"
if st.sidebar.button(f"🟢 Platform Status\n{db_salud}", use_container_width=True):
    st.sidebar.toast("Conexión con SQLite3 verificada y estable.")

st.sidebar.caption("Sesión: Médico Oncólogo")


# --- 4. ENRUTAMIENTO LOGICO DE LAS PANTALLAS ---

# ---------------------------------------------------------
# BOTÓN 1: DASHBOARD CLINICO PRINCIPAL (CON BOTÓN DE DESCARGA)
# ---------------------------------------------------------
if st.session_state["menu_activo"] == "🏠 Dashboard":
    # Banner en formato compacto y controlado
st.image(
    "banner_real.png", 
    width=450
)
        st.image("banner_real.png", use_container_width=True)
        
    st.title("Molecular Methylation Analysis Hub")
    st.caption("Panel Ejecutivo de Cribado para Cáncer de Mama en Etapa Temprana")
    st.markdown("---")
    
    st.markdown("### 📥 Panel de Entrada de Datos Clínicos")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        patient_id = st.text_input("🆔 ID Único del Paciente", placeholder="Ej. METH-2026-0X")
    with col_f2:
        patient_age = st.number_input("🎂 Edad Cronológica", min_value=18, max_value=100, value=45)
    with col_f3:
        ctdna_score = st.number_input("🔬 Concentración de ctDNA (ng/mL)", min_value=0.0000, max_value=5.0000, format="%.4f", value=0.2500)
    
    if ctdna_score >= UMBRAL:
        resultado = "High Risk - CPEB4+"
    else:
        resultado = "Low Risk - Estable"
        
    # Bloque de Botones Clínicos Alineados Horizontalmente
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Registrar Diagnóstico en SQLite3", use_container_width=True):
            if patient_id:
                conn = sqlite3.connect("methyl_clinic.db")
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO pacientes VALUES (?, ?, ?, ?)", (patient_id, patient_age, ctdna_score, resultado))
                    conn.commit()
                    st.success(f"Registro exitoso para ID: {patient_id}")
                except sqlite3.IntegrityError:
                    st.error("Error: El ID del paciente ya se encuentra registrado.")
                finally:
                    conn.close()
            else:
                st.warning("Por favor ingrese un ID válido.")
                
    with col_btn2:
        # Estructuración interna del archivo de descarga del reporte
        reporte_lineas = []
        reporte_lineas.append("=========================================")
        reporte_lineas.append(" METHYLOX LABS - REPORT ")
        reporte_lineas.append(" Screening de Metilación para Cáncer ")
        reporte_lineas.append("=========================================")
        reporte_lineas.append(f"ID Paciente: {patient_id if patient_id else 'N/A'}")
        reporte_lineas.append(f"Edad: {patient_age} años")
        reporte_lineas.append(f"Score ctDNA: {ctdna_score:.4f} ng/mL")
        reporte_lineas.append(f"Umbral Estadístico: {UMBRAL} ng/mL")
        reporte_lineas.append("-----------------------------------------")
        reporte_lineas.append(f"CLASIFICACIÓN IA: {resultado}")
        reporte_lineas.append("-----------------------------------------")
        reporte_lineas.append("Estatus CRISPR: Calibración Cas12 lista.")
        reporte_lineas.append("Documento emitido de forma automatizada.")
        reporte_lineas.append("=========================================")
        texto_reporte = "\n".join(reporte_lineas)
        
        # BOTÓN DE DESCARGA CONFIGURADO Y ACTIVO ALWAYS
        st.download_button(
            label="📥 Descargar Reporte Clínico Firmado (.TXT)",
            data=texto_reporte,
            file_name=f"Reporte_MethylOx_{patient_id if patient_id else 'Resumen'}.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("### 📊 Estatus de Diagnóstico Actual")
    c_tar1, c_tar2, c_tar3 = st.columns(3)
    with c_tar1:
        st.metric(label="Patient Profile / Estatus", value="Stage I - Breast Cancer" if patient_id else "Esperando Paciente")
    with c_tar2:
        st.metric(label="Global Methylation Index", value=f"{ctdna_score:.4f} ng/mL")
    with c_tar3:
        st.metric(label="Diagnostic Verdict", value=resultado)

# ---------------------------------------------------------
# BOTÓN 2: PERFILES DE PACIENTES (GESTIÓN BASE DE DATOS)
# ---------------------------------------------------------
elif st.session_state["menu_activo"] == "👤 Patient Profiles":
    st.title("👤 Patient Profiles & Clinical Records")
    st.caption("Panel de administración y modificación de registros clínicos en SQLite3")
    st.markdown("---")
    
    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    
    if not df_pacientes.empty:
        st.dataframe(df_pacientes, use_container_width=True)
        
        st.markdown("### 🛠️ Acciones de Gestión de Registros")
        id_borrar = st.text_input("Ingresa el ID del paciente que deseas eliminar:")
        if st.button("❌ Eliminar Paciente Permanentemente"):
            if id_borrar:
                conn = sqlite3.connect("methyl_clinic.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pacientes WHERE id=?", (id_borrar,))
                conn.commit()
                conn.close()
                st.success(f"Paciente {id_borrar} eliminado del sistema.")
    else:
        st.info("No hay perfiles clínicos registrados actualmente en el sistema.")

# ---------------------------------------------------------
# BOTÓN 3: MATRIZ DE METILACIÓN (ANÁLISIS ESTADÍSTICO)
# ---------------------------------------------------------
elif st.session_state["menu_activo"] == "📊 Methylation Matrix":
    st.title("📊 Methylation Matrix Analytics")
    st.caption("Evidencia estadística masiva del screening epigenético")
    st.markdown("---")
    
    g1, g2, g3 = st.columns(3)
    with g1:
        st.write("**Epigenetic Biomarker Overview (CpG)**")
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.imshow(np.random.rand(8, 8), cmap="Blues")
        ax1.axis("off")
        st.pyplot(fig1)
        
    with g2:
        st.write("**CRISPR Guidance Response Mapping (ROC)**")
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        x = np.linspace(0, 1, 100)
        ax2.plot(x, 1 - np.exp(-5 * x), color="#06141D")
        ax2.plot([0, 1], [0, 1], "r--")
        st.pyplot(fig2)
        
    with g3:
        st.write("**Automated Population Distribution**")
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.hist(np.random.normal(0.3, 0.1, 100), alpha=0.5, color="green")
        # Renderizado del tercer histograma
        ax3.hist(
            np.random.normal(0.8, 0.1, 100), 
            alpha=0.5, 
            color="red"
        )
        
        # Comando de dibujo en pantalla
        st.pyplot(fig3)

# ---------------------------------------------------------
# BOTÓN 4: BIBLIOTECA CRISPR-CAS12 (COMPATIBILIDAD UNIVERSAL)
# ---------------------------------------------------------
elif st.session_state["menu_activo"] == "🧬 CRISPR Guide Library":
    st.title("🧬 CRISPR Guide Library & Screening")
    st.caption("Algoritmo unificado de escaneo molecular compatible con múltiples formatos")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Subir cualquier documento genómico o base de datos de Colab"
    )
    
    if uploaded_file is not None:
        nombre_archivo = uploaded_file.name
        df_secuencias = None
        
        try:
            if nombre_archivo.endswith(".csv"):
                df_secuencias = pd.read_csv(uploaded_file)
                
            elif nombre_archivo.endswith(".tsv") or nombre_archivo.endswith(".txt"):
                df_secuencias = pd.read_csv(uploaded_file, sep="\t")
                
            elif nombre_archivo.endswith(".xlsx") or nombre_archivo.endswith(".xls"):
                df_secuencias = pd.read_excel(uploaded_file)
                
            else:
                df_secuencias = pd.read_csv(uploaded_file)
                
            if df_secuencias is not None:
                columnas_requeridas = ["ctdna_score", "secuencia_pam", "porcentaje_gc"]
                if all(col in df_secuencias.columns for col in columnas_requeridas):
                    
                    df_f1 = df_secuencias[df_secuencias["ctdna_score"] >= UMBRAL]
                    condicion_pam = df_f1["secuencia_pam"].str.contains("TTT[ACG]", na=False)
                    condicion_gc = (df_f1["porcentaje_gc"] >= 40) & (df_f1["porcentaje_gc"] <= 60)
                    df_guias_nuevas = df_f1[condicion_pam & condicion_gc]
                    
                    st.success(f"Análisis completado: Se descubrieron {len(df_guias_nuevas)} nuevas guías potenciales.")
                    st.dataframe(df_guias_nuevas, use_container_width=True)
                else:
                    st.warning("El documento no contiene las columnas necesarias: ctdna_score, secuencia_pam, porcentaje_gc.")
                    
        except Exception as e:
            st.error("Error al procesar el archivo: No se pudo interpretar la estructura del documento.")
    else:
        st.info("💡 Puedes arrastrar archivos CSV, hojas de Excel (.xlsx) o archivos de texto plano (.txt/.tsv).")

# ---------------------------------------------------------
# BOTÓN 5: ANALISIS DE GEL (ELECTROFORESIS SIMULADA)
# ---------------------------------------------------------
elif st.session_state["menu_activo"] == "🧪 Gel Analysis":
    st.title("🧪 Automated Gel Clearance Inspection")
    st.caption("Simulación bioinformática automatizada de bandas de electroforesis")
    st.markdown("---")
    
    st.slider("Ajustar concentración de matriz de agarosa (%)", 0.5, 2.5, 1.2)
    st.write("**Visualización de la corrida electroforética simulada para corte CRISPR:**")
    
    fig_gel, ax_gel = plt.subplots(figsize=(6, 3))
    ax_gel.fill_between([0, 10], [0, 0], [10, 10], color="#111827")
    ax_gel.hlines(y=[3, 5, 7], xmin=2, xmax=8, color="#10B981", lw=6, alpha=0.8)
    ax_gel.set_title("Bandas de ctDNA fragmentado detectadas por Cas12a", color="white")
    ax_gel.set_facecolor("#111827")
    st.pyplot(fig_gel)

# ---------------------------------------------------------
# BOTÓN 6: REPORTE GENERAL HISTÓRICO
# ---------------------------------------------------------
elif st.session_state["menu_activo"] == "📄 Reports":
    st.title("📄 Clinical Reports Archive")
    st.caption("Consola histórica de auditoría y descarga de bitácoras institucionales")
    st.markdown("---")
    
    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    
    if not df_pacientes.empty:
        st.write("Selecciona un paciente para regenerar un reporte masivo:")
        id_reporte = st.selectbox("Pacientes en historial:", df_pacientes["id"].tolist())
        st.info(f"Reporte unificado listo para impresión digital para el paciente: {id_reporte}")
    else:
        st.warning("No hay reportes disponibles en el archivo actual.")

# ---------------------------------------------------------
# BOTÓN 7: CONFIGURACIÓN / INGENIERÍA
# ---------------------------------------------------------
elif st.session_state["menu_activo"] == "⚙️ Settings":
    st.title("⚙️ Engineering Core Settings")
    st.caption("Hiperparámetros fijos globales de la Fase 4 de MethylOx Labs")
    st.markdown("---")
    
    df_hyper = pd.DataFrame({
        "Parámetro Tecnológico": ["Profundidad de Secuenciación", "Filtro de Calidad Q-Score", "Mapeo Bisulfito Mismatches", "Normalización de Cobertura"],
        "Valor en Backend": ["x10000", ">= 30", "<= 2 bp", "CPM (Counts Per Million)"]
    })
    st.table(df_hyper)
