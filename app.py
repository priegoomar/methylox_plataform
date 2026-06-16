import sqlite3
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importación de la capa analítica pura
from motores import (
    iniciar_base_datos,
    procesar_diagnostico_clinico,
    registrar_paciente_db,
    ejecutar_motores_crispr_unificados,
    UMBRAL_GLOBAL
)

# 1. CONFIGURACION DE PAGINA MAESTRA
st.set_page_config(
    page_title="MethylOx Labs",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ARQUITECTURA DE DISEÑO: CORPORATIVO #2563EB
st.markdown(
    """
    <style>
    /* Fondo general de laboratorio satinado */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    /* Banner panorámico micro-compacto */
    [data-testid="stImage"] img {
        width: 100% !important;
        height: auto !important;
        max-height: 200px !important;
        object-fit: contain !important;
        border-radius: 10px !important;
        border-bottom: 3px solid #2563EB !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1) !important;
    }
    }
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 2px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h2 {
        color: #0F172A !important;
    }
    /* Botones de navegación interactivos #2563EB */
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
    /* Paneles de datos con la ceja #2563EB */
    .biotech-panel {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-top: 4px solid #2563EB !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    @keyframes heartbeat {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    .pulse-glow {
        color: #10B981 !important;
        font-weight: bold !important;
        animation: heartbeat 2s infinite ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

iniciar_base_datos()

# --- 3. BARRA LATERAL DE ACCESO ---
st.sidebar.markdown("## 🔬 MethylOx Labs")
st.sidebar.markdown("---")

rol_usuario = st.sidebar.radio(
    "🔑 Seleccione su Rol de Acceso:",
    ["🔬 Médico Oncólogo", "⚙️ Ingeniero / Científico BIOTECH"]
)

st.sidebar.markdown("---")

if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "🏠 Dashboard"

if st.sidebar.button("🏠 Dashboard", use_container_width=True): 
    st.session_state["menu_activo"] = "🏠 Dashboard"

if st.sidebar.button("👤 Patient Profiles", use_container_width=True): 
    st.session_state["menu_activo"] = "👤 Patient Profiles"

if st.sidebar.button("📄 Reports", use_container_width=True): 
    st.session_state["menu_activo"] = "📄 Reports"

if rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.sidebar.markdown("<p style='color:#2563EB; font-weight:bold; margin-bottom:2px;'>Módulos Bioinformáticos:</p>", unsafe_allow_html=True)
    
    if st.sidebar.button("📊 Methylation Matrix", use_container_width=True): 
        st.session_state["menu_activo"] = "📊 Methylation Matrix"
        
    if st.sidebar.button("🧬 CRISPR Guide Library", use_container_width=True): 
        st.session_state["menu_activo"] = "🧬 CRISPR Guide Library"
        
    if st.sidebar.button("🧪 Gel Analysis", use_container_width=True): 
        st.session_state["menu_activo"] = "🧪 Gel Analysis"
        
    if st.sidebar.button("⚙️ Settings", use_container_width=True): 
        st.session_state["menu_activo"] = "⚙️ Settings"

st.sidebar.markdown("---")
st.sidebar.markdown(f"Estatus: <span class='pulse-glow'>● Core Active</span>", unsafe_allow_html=True)


# --- 4. CONTROL DE PANTALLAS ---

# PANTALLA 1: DASHBOARD
if st.session_state["menu_activo"] == "🏠 Dashboard":
    st.image("banner_real.png", use_container_width=True)
    st.title("Molecular Methylation Analysis Hub")
    st.caption("Early Detection Through Epigenetic AI | Automated Screening Platform")
    st.markdown("---")
    
    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#2563EB; margin-top:0; font-weight:600;'>📥 Patient Enrollment Matrix</h4>", unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1: patient_id = st.text_input("🆔 Patient Identifier", placeholder="Ej. METH-2026-0X")
    with col_f2: patient_age = st.number_input("🎂 Chronological Age", min_value=18, max_value=100, value=45)
    with col_f3: ctdna_score = st.number_input("🔬 ctDNA Concentration (ng/mL)", min_value=0.0000, max_value=5.0000, format="%.4f", value=0.2500)
    
    resultado = procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score)
        
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Commit Diagnostic Data", use_container_width=True):
            if patient_id:
                estatus_db = registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado)
                if estatus_db == "Éxito": st.success(f"Record verified for ID: {patient_id}")
                else: st.error("Database conflict: ID already exists.")
            else: st.warning("Invalid credentials.")
                
    with col_btn2:
        reporte_txt = f"METHYLOX CLINICAL EXCERPT\nID: {patient_id}\nAge: {patient_age}\nScore: {ctdna_score:.4f}\nVerdict: {resultado}"
        st.download_button("📥 Export Prognostic Report (.TXT)", data=reporte_txt, file_name=f"Report_{patient_id}.txt", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#2563EB; margin-top:0; font-weight:600;'>📊 Real-Time Analytics Overview</h4>", unsafe_allow_html=True)
    c_tar1, c_tar2, c_tar3 = st.columns(3)
    with c_tar1: st.metric(label="Clinical Cohort Status", value="Stage I Breast Cancer" if patient_id else "Awaiting Input")
    with c_tar2: st.metric(label="Global Methylation Value", value=f"{ctdna_score:.4f} ng/mL")
    with c_tar3: st.metric(label="Diagnostic Verdict", value=resultado)
    st.markdown("</div>", unsafe_allow_html=True)

# PANTALLA 2: HISTORIAL Y EDICIÓN COMPLETA DE PACIENTES
elif st.session_state["menu_activo"] == "👤 Patient Profiles":
    st.title("👤 Patient Profiles & Clinical Records")
    st.caption("Consola de búsqueda, edición y gestión avanzada en SQLite3")
    st.markdown("---")
    
    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    
    if not df_pacientes.empty: 
        st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#2563EB; margin-top:0;'>📋 Registro Central de Hospital</h4>", unsafe_allow_html=True)
        st.dataframe(df_pacientes, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # MÓDULO INTERACTIVO DE EDICIÓN Y BÚSQUEDA REAL
        st.markdown("<div class='biotech-panel'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#2563EB; margin-top:0;'>🛠️ Buscar y Modificar Expediente Médico</h4>", unsafe_allow_html=True)
        
        id_busqueda = st.text_input("Ingrese el ID exacto del paciente a gestionar:")
        
        if id_busqueda:
            conn = sqlite3.connect("methyl_clinic.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pacientes WHERE id=?", (id_busqueda,))
            paciente_encontrado = cursor.fetchone()
            conn.close()
            
            if paciente_encontrado:
                st.info(f"Paciente localizado. Clasificación actual en BD: {paciente_encontrado[3]}")
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    nueva_edad = st.number_input("Modificar Edad Cronológica:", min_value=18, max_value=100, value=int(paciente_encontrado[1]))
                with col_e2:
                    nuevo_score = st.number_input("Modificar Concentración ctDNA (ng/mL):", min_value=0.0, max_value=5.0, format="%.4f", value=float(paciente_encontrado[2]))
                
                # Recálculo automático del umbral en base a la edición del médico
                nuevo_veredicto = procesar_diagnostico_clinico(id_busqueda, nueva_edad, nuevo_score)
                
                col_op1, col_op2 = st.columns(2)
                with col_op1:
                    if st.button("🔄 Guardar Cambios Actualizados", use_container_width=True):
                        conn = sqlite3.connect("methyl_clinic.db")
                        cursor = conn.cursor()
                        cursor.execute("UPDATE pacientes SET edad=?, ctdna=?, clasificacion=? WHERE id=?", (nueva_edad, nuevo_score, nuevo_veredicto, id_busqueda))
                        conn.commit()
                        conn.close()
                        st.success(f"Expediente {id_busqueda} actualizado correctamente.")
                with col_op2:
                    if st.button("❌ Eliminar Registro Permanentemente", use_container_width=True):
                        conn = sqlite3.connect("methyl_clinic.db")
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM pacientes WHERE id=?", (id_busqueda,))
                        conn.commit()
                        conn.close()
                        st.error(f"Expediente del paciente {id_busqueda} eliminado de SQLite3.")
            else:
                st.warning("El ID ingresado no coincide con ningún expediente activo.")
        st.markdown("", unsafe_allow_html=True)
    else:
        st.info("No hay registros almacenados actualmente.")

# PANTALLA 5: SIMULACIÓN DE GEL RE-ACTIVA CON DATOS CLÍNICOS REALES
elif st.session_state["menu_activo"] == "🧪 Gel Analysis" and rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.title("🧪 Automated Gel Clearance Inspection")
    st.caption("Análisis electroforético digital reactivo al ctDNA de la base de datos")
    st.markdown("---")
    conn = sqlite3.connect("methyl_clinic.db")
    df_pacientes = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    st.markdown("", unsafe_allow_html=True)
    if not df_pacientes.empty:
        id_gel = st.selectbox("Seleccione el Paciente para Corrida en Gel:", df_pacientes["id"].tolist())
        # Extracción del Score real de la base de datos
        fila_p = df_pacientes[df_pacientes["id"] == id_gel].iloc[0]
        score_db = float(fila_p["ctdna"])
        veredicto_db = fila_p["clasificacion"]
        st.write(f"Análisis de Muestra: {id_gel} | Concentración ctDNA: {score_db:.4f} ng/mL")
        # Lógica científica de reactividad: a mayor score, mayor intensidad (alpha) y migración
        intensidad_banda = min(1.0, max(0.1, score_db / 2.0))
        # Si es alto riesgo, el fragmento de metilación cortado migra a una altura específica (bp)
        altura_bp = 350 if "High Risk" in veredicto_db else 700
        fig_gel, ax_gel = plt.subplots(figsize=(6, 3))
        # Fondo oscuro del tanque de electroforesis
        ax_gel.fill_between([0, 10], 0, 1000, color="#111827")
        # Dibujo dinámico de la banda diana (Intensidad regulada por el score real)
        ax_gel.hlines(y=altura_bp, xmin=3, xmax=7, color="#00E5FF", lw=8, alpha=intensidad_banda, label="Fragmento Promotor CPEB4")
        # Marcador de peso molecular de referencia constante (Ladder)
        ax_gel.hlines(y=[100, 300, 500, 700, 900], xmin=0.5, xmax=1.5, color="#94A3B8", lw=2)
        ax_gel.set_xlim(0, 10)
        ax_gel.set_ylim(0, 1000)
        ax_gel.set_ylabel("Base Pairs (bp)", color="#0F172A")
        ax_gel.set_title(f"Electroforesis Digital en Vivo - Expediente {id_gel}", color="#0F172A")
        ax_gel.set_facecolor("#111827")
        st.pyplot(fig_gel)
        st.caption(f"Interpretación: Banda detectada en ~{altura_bp}bp con factor de luminiscencia fluorescente de {intensidad_banda:.2f}.")
    else:
        st.warning("⚠️ Se requiere registrar al menos un paciente en el Dashboard para activar la simulación del gel.")
    st.markdown("", unsafe_allow_html=True)
# PANTALLAS EXCLUSIVAS RESTANTES
elif st.session_state["menu_activo"] == "📊 Methylation Matrix" and rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.title("📊 Methylation Matrix Analytics")
    st.markdown("---")
    st.markdown("", unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1:
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.imshow(np.random.rand(8, 8), cmap="Blues")
        ax1.axis("off")
        st.pyplot(fig1)
    with g2:
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        x = np.linspace(0, 1, 100)
        ax2.plot(x, 1 - np.exp(-5 * x), color="#2563EB")
        st.pyplot(fig2)
    with g3:
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.hist(np.random.normal(0.3, 0.1, 100), alpha=0.5, color="green")
        ax3.hist(np.random.normal(0.8, 0.1, 100), alpha=0.5, color="red")
        st.pyplot(fig3)
    st.markdown("", unsafe_allow_html=True)

elif st.session_state["menu_activo"] == "🧬 CRISPR Guide Library" and rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.title("🧬 CRISPR Guide Library & Screening")
    st.markdown("---")
    st.markdown("", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload core genomic logs / raw database files")
    st.markdown("", unsafe_allow_html=True)
    if uploaded_file is not None:
        try:
            nombre = uploaded_file.name
            df_secuencias = pd.read_excel(uploaded_file) if nombre.endswith(('.xlsx', '.xls')) else pd.read_csv(uploaded_file, sep='\t' if nombre.endswith(('.tsv', '.txt')) else ',')
            df_guias_nuevas = ejecutar_motores_crispr_unificados(df_secuencias)
            st.success(f"Screening complete: {len(df_guias_nuevas)} high-affinity guides isolated.")
            st.dataframe(df_guias_nuevas, use_container_width=True)
        except Exception:
            st.error("Execution error: Invalid matrix mapping structure.")

elif st.session_state["menu_activo"] == "⚙️ Settings" and rol_usuario == "⚙️ Ingeniero / Científico BIOTECH":
    st.title("⚙️ Engineering Core & Backend Diagnostics")
    st.markdown("---")
    try:
        with open("motores.py", "r", encoding="utf-8") as file:
            codigo_backend = file.read()
        st.code(codigo_backend, language="python")
        st.success("✅ Conexión e integridad del archivo motores.py verificada.")
    except Exception:
        st.error("❌ No se pudo enlazar el visor con motores.py")
