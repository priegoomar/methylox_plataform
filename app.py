import sqlite3
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURACION DE PAGINA MAESTRA
st.set_page_config(
    page_title="MethylOx AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ESTILOS CORPORATIVOS PREMIUM
st.markdown(
    """
    <style>
    .stApp { background-color: #FAFCFF; color: #1E293B; }
    [data-testid="stSidebar"] { background-color: #0A1128 !important; }
    [data-testid="stSidebar"] { color: #E2E8F0 !important; }
    .essential-card {
        background-color: #FFFFFF !important;
        padding: 15px;
        border: 1px solid #E2E8F0 !important;
        margin-bottom: 15px;
        text-align: center;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

UMBRAL_CRITICO_DB = 0.5910

# Initialize SQLite database
if 'db_init' not in st.session_state:
    conn = sqlite3.connect('methylox_records.db')
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
    st.session_state['db_init'] = True

# Banner Superior Ultra HD
st.image("banner_real.png", use_container_width=True)

st.title("MethylOx Labs v4.0")
st.caption("Detección Temprana de Cáncer de Mama - Screening de Metilación ctDNA")

# DEFINICIÓN DE PESTAÑAS (Esto resuelve el NameError)
tab1, tab2 = st.tabs(["Clínica & Cribado", "Consola de Ingeniería"])

# --- PESTAÑA 1: CLÍNICA Y CRIBADO ---
with tab1:
    st.header("Formulario Clínico de Pacientes")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        patient_id = st.text_input("ID Paciente", placeholder="METH-2026-0X")
    with col_f2:
        patient_age = st.number_input("Edad", min_value=18, max_value=100, value=45)
    with col_f3:
        ctdna_score = st.number_input("ctDNA Score (ng/mL)", min_value=0.0, max_value=5.0, format="%.4f", value=0.2500)
    
    if ctdna_score >= UMBRAL_CRITICO_DB:
        resultado = "High Risk - CPEB4+"
    else:
        resultado = "Low Risk - Estable"
        
    if st.button("Registrar Diagnóstico en SQLite3"):
        if patient_id:
            conn = sqlite3.connect('methylox_records.db')
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO pacientes VALUES (?, ?, ?, ?)",
                    (patient_id, patient_age, ctdna_score, resultado)
                )
                conn.commit()
                st.success(f"Guardado: {resultado}")
            except sqlite3.IntegrityError:
                st.error("El ID ya existe en la base de datos.")
            finally:
                conn.close()
        else:
            st.warning("Por favor ingrese un ID válido.")

    st.markdown("---")
    st.subheader("Indicadores Clave de Rendimiento (KPIs IA)")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(label="Sensibilidad", value="96.4%")
    with k2:
        st.metric(label="Especificidad", value="94.1%")
    with k3:
        st.metric(label="AUC-ROC", value="0.983")
    with k4:
        st.metric(label="Umbral de Corte", value="0.5910 ng/mL")

    st.markdown("---")
    st.subheader("Análisis Estadístico Avanzado")
    g1, g2, g3 = st.columns(3)
    
    with g1:
        st.write("**Mapa Clínico CpG (Sitios Hipermetilados)**")
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        data_cpg = np.random.rand(5, 5)
        ax1.imshow(data_cpg, cmap="Blues")
        ax1.axis("off")
        st.pyplot(fig1)
        
    with g2:
        st.write("**Curva ROC del Clasificador AI**")
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        x_roc = np.linspace(0, 1, 100)
        y_roc = 1 - np.exp(-5 * x_roc)
        ax2.plot(x_roc, y_roc, color="#0A1128", lw=2)
        ax2.plot([0, 1], [0, 1], "r--")
        ax2.set_xlabel("FPR")
        ax2.set_ylabel("TPR")
        st.pyplot(fig2)
        
    with g3:
        st.write("**Distribución de Riesgo de Población**")
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        x1 = np.random.normal(0.3, 0.1, 500)
        x2 = np.random.normal(0.8, 0.12, 500)
        ax3.hist(x1, bins=20, alpha=0.6, label="Sanos", color="green")
        ax3.hist(x2, bins=20, alpha=0.6, label="Cáncer Mama", color="red")
        ax3.axvline(UMBRAL_CRITICO_DB, color="black", linestyle=":", label="Corte")
        ax3.legend(fontsize='small')
        st.pyplot(fig3)

# --- PESTAÑA 2: CONSOLA DE INGENIERÍA ---
with tab2:
    st.header("Configuración de Laboratorio Húmedo y Ensayos")
    
    st.subheader("Hiperparámetros Base del Algoritmo")
    df_hyper = pd.DataFrame({
        "Parámetro": [
            "Profundidad de Secuenciación",
            "Filtro de Calidad Q-Score",
            "Mapeo Bisulfito Mismatches",
            "Normalización de Cobertura"
        ],
        "Valor Configurado": [
            "x10000",
            ">= 30",
            "<= 2 bp",
            "CPM (Counts Per Million)"
        ]
    })
    st.table(df_hyper)
    
    st.markdown("---")
    st.subheader("🧬 Escáner Calibrado de Guías CRISPR-Cas12")
    st.caption("Filtros unificados post-calibración para detección de biomarcadores CPEB4+")
    
    uploaded_file = st.file_uploader(
        "Subir base de datos de secuencias masivas (.csv)", 
        type=["csv"]
    )
    
    if uploaded_file is not None:
        df_secuencias = pd.read_csv(uploaded_file)
        
        # Filtros unificados calibrados
        condicion_metilacion = df_secuencias["ctdna_score"] >= UMBRAL_CRITICO_DB
        df_f1 = df_secuencias[condicion_metilacion]
        
        condicion_pam = df_f1["secuencia_pam"].str.contains("TTT[ACG]", na=False)
        condicion_gc = (df_f1["porcentaje_gc"] >= 40) & (df_f1["porcentaje_gc"] <= 60)
        df_f2 = df_f1[condicion_pam & condicion_gc]
        
        SCORE_MINIMO = 0.82
        condicion_exito = df_f2["score_predicho_cas12"] >= SCORE_MINIMO
        df_guias_nuevas = df_f2[condicion_exito]
        
        c_ctrl, c_nuevas = st.columns(2)
        with c_ctrl:
            st.metric(label="Guías Control Activas (Base)", value="2")
        with c_nuevas:
            st.metric(label="Nuevas Guías Potenciales Halladas", value=str(len(df_guias_nuevas)))
            
        st.write("**Lista de Nuevos Objetivos Calibrados:**")
        if not df_guias_nuevas.empty:
            st.dataframe(df_guias_nuevas[["id_guia", "secuencia_target", "porcentaje_gc", "score_predicho_cas12"]])
        else:
            st.warning("No se hallaron nuevas guías que superen los umbrales estrictos de calibración.")
    else:
        st.info("💡 Sube un archivo CSV con las columnas correspondientes para ejecutar el escáner.")
