import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

# 1. CONFIGURACION DE PAGINA MAESTRA
st.set_page_config(page_title="MethylOx AI", layout="wide", initial_sidebar_state="expanded")

# IMAGEN PREMIUM CONVERTIDA EN CODIGO PURO (Inyección directa sin enlaces externos)
img_base64 = "iVBORw0KGgoAAAANSUhEUgAAA+gAAADwCAMAAAC380UDAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAAAAAO7u7v///+/v75mZmf///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAAUnRSTlMAQM/f379/D9/f369fX9+vr++vn5+ff39fX19fX09PT09PT08vLy8vLy8vLy8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8ftPsh0AAAC0Zp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"

# 2. ESTILOS BASE DE ALTA COMPATIBILIDAD
st.markdown(f"""<style>
    .stApp {{ background-color: #FAFCFF; color: #1E293B; }}
    [data-testid="stSidebar"] {{ background-color: #0A1128 !important; }}
    [data-testid="stSidebar"] * {{ color: #E2E8F0 !important; }}
    
    /* Contenedor del Banner con tu Imagen Corporativa Real */
    .enterprise-card-banner {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 16px;
        border: 1px solid #D2E4FF;
        margin-bottom: 25px;
        min-height: 250px;
        width: 100%;
    }}
    
    .essential-card {{ 
        background-color: #FFFFFF !important; 
        padding: 15px; 
        border: 1px solid #E2E8F0 !important; 
        margin-bottom: 15px; 
        text-align: center;
        border-radius: 8px;
    }}
</style>""", unsafe_allow_html=True)

UMBRAL_CRITICO_DB = 0.5910

if "db_init" not in st.session_state:
    conn = sqlite3.connect('methylax_records.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS pacientes (id TEXT PRIMARY KEY, edad INTEGER, metilacion REAL, riesgo TEXT)")
    conn.commit(); conn.close()
    st.session_state.db_init = True

with st.sidebar:
    st.markdown("<h2 style='color:white;'>MethylOx™</h2>", unsafe_allow_html=True)
    st.markdown("🏠 **Dashboard**\n📦 **Samples**\n🧠 **AI Analysis**")

tab_clinico, tab_ingenieria = st.tabs(["📋 Panel Clinico", "⚙️ Consola Ingenieria"])

with tab_clinico:
    # EL LIENZO DESPLIEGA TU IMAGEN REAL INYECTADA
    st.markdown('<div class="enterprise-card-banner"></div>', unsafe_allow_html=True)

    with st.form("f_paciente", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        with f1: p_id = st.text_input("ID del paciente / Codigo de muestra")
        with f2: p_edad = st.number_input("Edad", min_value=1, value=50)
        with f3: p_met = st.number_input("Puntuacion de ctDNA", min_value=0.0, max_value=1.0, value=0.35, format="%.4f")
        if st.form_submit_button("🔒 Analizar y guardar datos"):
            if p_id:
                r_c = "High Risk" if p_met >= UMBRAL_CRITICO_DB else "Low Risk"
                conn = sqlite3.connect('methylax_records.db'); c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO pacientes VALUES (?, ?, ?, ?)", (p_id, p_edad, p_met, r_c))

with tab_ingenieria:
    st.markdown('⚙️ Consola Ingenieria')
    h_param = []
    h_param.append("UMBRAL_CRITICO_DB")
    h_param.append("BACKGROUND_NOISE_PURGE")
    h_param.append("DATA_PERSISTENCE")
    h_val = []
    h_val.append("0.5910 ng/mL")
    h_val.append("BCAS3 Excluded")
    h_val.append("SQLite3 Relational")
    df_b = pd.DataFrame()
    df_b['Hyperparameter'] = h_param
    df_b['Value'] = h_val
    st.dataframe(df_b)
    
    st.markdown('### 🧪 Matriz Analitica DoE')
    corridas = []
    corridas.append("1")
    corridas.append("2")
    corridas.append("3")
    corridas.append("4")
    corridas.append("5")
    corridas.append("6")
    corridas.append("7")
    corridas.append("8")
    f_temp = []
    f_temp.append("55C")
    f_temp.append("62C")
    f_temp.append("55C")
    f_temp.append("62C")
    f_temp.append("55C")
    f_temp.append("62C")
    f_temp.append("55C")
    f_temp.append("62C")
    f_enz = []
    f_enz.append("0.5")
    f_enz.append("0.5")
    f_enz.append("2.0")
    f_enz.append("2.0")
    f_enz.append("0.5")
    f_enz.append("0.5")
    f_enz.append("2.0")
    f_enz.append("2.0")
    f_tie = []
    f_tie.append("60m")
    f_tie.append("60m")
    f_tie.append("60m")
    f_tie.append("60m")
    f_tie.append("180")
    f_tie.append("180")
    f_tie.append("180")
    f_tie.append("180")
    f_cod = []
    f_cod.append("(1)")
    f_cod.append("a")
    f_cod.append("b")
    f_cod.append("ab")
    f_cod.append("c")
    f_cod.append("ac")
    f_cod.append("bc")
    f_cod.append("abc")
    df_doe = pd.DataFrame()
    df_doe['Corrida'] = corridas
    df_doe['Temp'] = f_temp
    df_doe['Enzima'] = f_enz
    df_doe['Tiempo'] = f_tie
    df_doe['Codigo'] = f_cod
    st.dataframe(df_doe)
