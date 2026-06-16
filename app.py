import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

# 1. CONFIGURACION DE PAGINA MAESTRA
st.set_page_config(page_title="MethylOx AI", layout="wide", initial_sidebar_state="expanded")

# 2. MOTOR DE ANIMACIÓN CORPORATIVA
st.markdown("""<style>
    .stApp { background-color: #FAFCFF; color: #1E293B; }
    [data-testid="stSidebar"] { background-color: #0A1128 !important; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    
    /* Contenedor del Banner con tu Imagen Corporativa Real */
    .enterprise-card-banner {
        background-image: url("https://githubusercontent.com");
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-position: center;
        border-radius: 16px;
        border: 1px solid #D2E4FF;
        margin-bottom: 25px;
        min-height: 250px;
        width: 100%;
    }
    
    .essential-card { 
        background-color: #FFFFFF !important; 
        padding: 15px; 
        border: 1px solid #E2E8F0 !important; 
        margin-bottom: 15px; 
        text-align: center;
        border-radius: 8px;
    }
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
    # EL LIENZO DESPLIEGA TU IMAGEN REAL INYECTADA SIN TEXTOS DE ERROR
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
                conn.commit(); conn.close(); st.success("✔️ Guardado."); st.rerun()

    conn = sqlite3.connect('methylax_records.db')
    df_p = pd.read_sql_query("SELECT * FROM pacientes", conn); conn.close()
    st.dataframe(df_p, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown('<div class="essential-card"><span>SENSITIVITY</span><h2>96.4%</h2></div>', unsafe_allow_html=True)
    with k2: st.markdown('<div class="essential-card"><span>SPECIFICITY</span><h2>94.1%</h2></div>', unsafe_allow_html=True)
    with k3: st.markdown('<div class="essential-card"><span>AUC (ROC)</span><h2>0.983</h2></div>', unsafe_allow_html=True)
    with k4: st.markdown('<div class="essential-card"><span>CRITICAL LIMIT</span><h2>0.5910</h2></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('🧬 Mapa CpG')
        p_gen = np.random.randint(100, 5000, size=15)
        m_val = np.random.uniform(0.1, 0.9, size=15)
        df1 = pd.DataFrame()
        df1['Posicion'] = p_gen
        df1['Metilacion'] = m_val
        st.scatter_chart(df1, x='Posicion', y='Metilacion', height=180)

    with c2:
        st.markdown('📈 Curva ROC')
        f_val = np.linspace(0, 1, 20)
        t_val = 1 - np.exp(-4.5 * f_val)
        df2 = pd.DataFrame()
        df2['False Positive'] = f_val
        df2['True Positive'] = t_val
        st.line_chart(df2, x='False Positive', y='True Positive', height=180)

    with c3:
        st.markdown('📊 Distribucion')
        d_bajos = np.random.normal(0.3, 0.08, 80)
        d_altos = np.random.normal(0.75, 0.1, 80)
        df3 = pd.DataFrame()
        df3['Low Risk'] = d_bajos
        df3['High Risk'] = d_altos
        st.line_chart(df3, height=180)

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
    st.dataframe(df_b, use_container_width=True, hide_index=True)
    
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
    st.dataframe(df_doe, use_container_width=True, hide_index=True)
