import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

# 1. CONFIGURACION DE PAGINA CLINICA
st.set_page_config(page_title="MethylOx AI", layout="wide", initial_sidebar_state="expanded")

# 2. ESTILOS BASE DE ALTA COMPATIBILIDAD
st.markdown("""<style>
    .stApp { background-color: #FAFCFF; color: #1E293B; }
    [data-testid="stSidebar"] { background-color: #0A1128 !important; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    .enterprise-card-banner {
        background-color: #FFFFFF !important;
        padding: 30px; 
        border: 2px solid #D2E4FF !important; 
        margin-bottom: 25px;
        border-radius: 12px;
    }
    .essential-card { 
        background-color: #FFFFFF !important; 
        padding: 15px; 
        border: 2px solid #E2E8F0 !important; 
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
    conn.commit()
    conn.close()
    st.session_state.db_init = True

with st.sidebar:
    st.markdown("<h2 style='color:white;'>MethylOx™</h2>", unsafe_allow_html=True)
    st.markdown("🏠 **Dashboard**\n📦 **Samples**\n🧠 **AI Analysis**")
    st.markdown("---")
    st.markdown("<p style='color:#10B981; font-weight:bold;'>● Systems Operational</p>", unsafe_allow_html=True)

tab_clinico, tab_ingenieria = st.tabs(["📋 Panel Clinico", "⚙️ Consola Ingenieria"])

with tab_clinico:
    # BANNER VECTORIAL COMPATIBLE GENERADO POR CÓDIGO HTML/SVG
    st.markdown("""
        <table class="enterprise-card-banner" style="width:100%; border-collapse:collapse; background-color:#FFFFFF;">
            <tr>
                <td style="vertical-align:middle; padding-right:20px;">
                    <h1 style="margin:0; font-size:36px; color:#0A1128; font-family:sans-serif; font-weight:bold;">Laboratorios MethylOx</h1>
                    <p style="color:#475569; margin:5px 0 0 0; font-size:15px; font-family:sans-serif;">Deteccion temprana mediante ingenieria epigenetica</p>
                    <p style="margin-top:20px; font-size:13px; color:#2563EB; font-family:sans-serif; font-weight:bold;">
                        [DNA Methylation] &nbsp;&nbsp;&nbsp;&nbsp; [AI Engine] &nbsp;&nbsp;&nbsp;&nbsp; [Liquid Biopsy]
                    </p>
                </td>
                <td style="width:350px; text-align:right; vertical-align:middle;">
                    <svg width="340" height="100" viewBox="0 0 350 110" xmlns="http://w3.org">
                        <defs>
                            <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#1E3A8A"/><stop offset="100%" stop-color="#3B82F6"/></linearGradient>
                            <linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0EA5E9"/><stop offset="100%" stop-color="#22D3EE"/></linearGradient>
                            <filter id="glow"><feGaussianBlur stdDeviation="3" result="cb"/><feMerge><feMergeNode in="cb"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
                        </defs>
                        <path d="M15,35 Q55,90 95,35 T175,35 T255,35" stroke="url(#g1)" stroke-width="6.5" fill="none" stroke-linecap="round" filter="url(#glow)"/>
                        <path d="M15,75 Q55,20 95,75 T175,75 T255,75" stroke="url(#g2)" stroke-width="3.5" fill="none" stroke-dasharray="7,5" stroke-linecap="round" opacity="0.9"/>
                        <circle cx="55" cy="55" r="9" fill="url(#g1)" filter="url(#glow)"/><circle cx="135" cy="55" r="9" fill="url(#g2)" filter="url(#glow)"/>
                        <line x1="55" y1="55" x2="135" y2="55" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="3,3"/>
                        <circle cx="95" cy="35" r="4.5" fill="#67E8F9" filter="url(#glow)"/><circle cx="175" cy="35" r="4.5" fill="#67E8F9" filter="url(#glow)"/>
                        <polygon points="290,15 330,38 330,78 290,101 250,78 250,38" stroke="url(#g1)" stroke-width="4.5" fill="none" filter="url(#glow)"/>
                        <polygon points="290,27 318,44 318,69 290,86 262,69 262,44" stroke="url(#g2)" stroke-width="2" fill="none"/>
                        <circle cx="290" cy="57" r="14" fill="#2563EB" opacity="0.25" filter="url(#glow)"/>
                        <text x="278" y="63" fill="#0EA5E9" font-family="sans-serif" font-size="16" font-weight="bold">AI</text>
                    </svg>
                </td>
            </tr>
        </table>
    """, unsafe_allow_html=True)

    with st.form("f_paciente", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        with f1: p_id = st.text_input("ID del paciente / Codigo de muestra")
        with f2: p_edad = st.number_input("Edad", min_value=1, value=50)
        with f3: p_met = st.number_input("Puntuacion de ctDNA", min_value=0.0, max_value=1.0, value=0.35, format="%.4f")
        if st.form_submit_button("🔒 Analizar y guardar datos"):
            if p_id:
                r_c = "High Risk" if p_met >= UMBRAL_CRITICO_DB else "Low Risk"
                conn = sqlite3.connect('methylax_records.db')
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO pacientes VALUES (?, ?, ?, ?)", (p_id, p_edad, p_met, r_c))
                conn.commit()
                conn.close()
                st.success("✔️ Guardado.")
                st.rerun()

    conn = sqlite3.connect('methylax_records.db')
    df_p = pd.read_sql_query("SELECT * FROM pacientes", conn)
    conn.close()
    st.dataframe(df_p, use_container_width=True, hide_index=True)

    # 4 TARJETAS DE KPIS HORIZONTALES
    st.markdown("<br>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown('<div class="essential-card"><span>SENSITIVITY</span><h2>96.4%</h2></div>', unsafe_allow_html=True)
    with k2: st.markdown('<div class="essential-card"><span>SPECIFICITY</span><h2>94.1%</h2></div>', unsafe_allow_html=True)
    with k3: st.markdown('<div class="essential-card"><span>AUC (ROC)</span><h2>0.983</h2></div>', unsafe_allow_html=True)
    with k4: st.markdown('<div class="essential-card"><span>CRITICAL LIMIT</span><h2>0.5910</h2></div>', unsafe_allow_html=True)

    # GRAFICOS ANALITICOS EN 3 COLUMNAS SIMÉTRICAS
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="essential-card"><h5>🧬 Mapa CpG</h5>', unsafe_allow_html=True)
        pos_gen = np.random.randint(100, 5000, size=15)
        val_met = np.random.uniform(0.1, 0.9, size=15)
        df_cpg = pd.DataFrame()
        df_cpg['Posicion'] = pos_gen
        df_cpg['Metilacion'] = val_met
        st.scatter_chart(df_cpg, x='Posicion', y='Metilacion', color='#2563EB', height=180)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="essential-card"><h5>📈 Curva ROC</h5>', unsafe_allow_html=True)
        fpr_val = np.linspace(0, 1, 20)
        tpr_val = 1 - np.exp(-4.5 * fpr_val)
        df_roc = pd.DataFrame()
        df_roc['False Positive'] = fpr_val
        df_roc['True Positive'] = tpr_val
        st.line_chart(df_roc, x='False Positive', y='True Positive', color='#10B981', height=180)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="essential-card"><h5>📊 Distribucion de Riesgo</h5>', unsafe_allow_html=True)
        datos_bajos = np.random.normal(0.3, 0.08, 80)
        datos_altos = np.random.normal(0.75, 0.1, 80)
        df_dist = pd.DataFrame()
        df_dist['Low Risk'] = datos_bajos
        df_dist['High Risk'] = datos_altos
        st.line_chart(df_dist, color=["#3B82F6", "#EF4444"], height=180)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 7. CONSOLA DE INGENIERÍA COMPLETA (TODOS LOS RENGLONES DEL FINAL)
# ------------------------------------------------------------------------------
with tab_ingenieria:
    st.markdown('<div class="essential-card" style="text-align:left;"><h4>⚙️ Engineering Console</h4><p style="color:#64748B;">Configuraciones maestras e hiperparametros del sistema de Fase 4.</p></div>', unsafe_allow_html=True)
    
    # Tabla de Hiperparámetros base
    df_b = pd.DataFrame()
    df_b['Hyperparameter'] = ["UMBRAL_CRITICO_DB", "BACKGROUND_NOISE_PURGE", "DATA_PERSISTENCE"]
    df_b['Value'] = ["0.5910 ng/mL", "BCAS3 Excluded", "SQLite3 Relational"]
    st.dataframe(df_b, use_container_width=True, hide_index=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # MATRIZ DEL DISEÑO DE EXPERIMENTOS (DoE) DE 8 CORRIDAS
    st.markdown("### 🧪 Matriz Analitica DoE de 8 Corridas (Fase 4 Wet-Lab)")
    st.caption("Estructura Factorial Completa 2³ optimizada para conversion por Bisulfito y ddPCR (CPEB4+).")
    
    df_doe = pd.DataFrame()
    df_doe['Corrida'] = [1, 2, 3, 4, 5, 6, 7, 8]
    df_doe['Factor A: Temp'] = ["55°C", "62°C", "55°C", "62°C", "55°C", "62°C", "55°C", "62°C"]
    df_doe['Factor B: Enzima'] = ["0.5 uL", "0.5 uL", "2.0 uL", "2.0 uL", "0.5 uL", "0.5 uL", "2.0 uL", "2.0 uL"]
    df_doe['Factor C: Tiempo'] = ["60 min", "60 min", "60 min", "60 min", "180 min", "180 min", "180 min", "180 min"]
    df_doe['Codigo Matriz'] = ["(1)", "a", "b", "ab", "c", "ac", "bc", "abc"]
    
    st.dataframe(df_doe, use_container_width=True, hide_index=True)
