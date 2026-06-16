import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

# Configuración del lienzo digital al formato exacto de la referencia
st.set_page_config(page_title="MethylOx AI", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos de alta gama: Fondo degradado, Sidebar azul noche y tarjetas corporativas
st.markdown("""<style>
    .stApp { background-color: #FAFCFF; color: #1E293B; }
    [data-testid="stSidebar"] { background-color: #0A1128 !important; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    
    /* Contenedor del Banner Premium Blanco */
    .enterprise-card-banner {
        background: linear-gradient(135deg, #FFFFFF 0%, #F5F9FF 100%);
        padding: 30px; border-radius: 16px; border: 1px solid #D2E4FF; margin-bottom: 25px;
        display: flex; justify-content: space-between; align-items: center; min-height: 160px;
    }
    
    .essential-card { background-color: #FFFFFF !important; padding: 24px; border-radius: 14px; border: 1px solid #E2E8F0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }
    @keyframes pulse { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }
    .status-pulse { color: #10B981; font-weight: bold; animation: pulse 2s infinite; }
    h1, h2, h3, h4, h5 { color: #0A1128 !important; font-family: -apple-system, sans-serif; font-weight: 700; margin-top: 0; }
</style>""", unsafe_allow_html=True)

UMBRAL_CRITICO_DB = 0.5910

# Inicialización segura de la base de datos relacional local
if "db_init" not in st.session_state:
    conn = sqlite3.connect('methylax_records.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS pacientes (id TEXT PRIMARY KEY, edad INTEGER, metilacion REAL, riesgo TEXT)")
    conn.commit(); conn.close()
    st.session_state.db_init = True

with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>MethylOx™</h2><p style='color:#38BDF8; font-size:12px;'>Epigenetic AI Platform</p>", unsafe_allow_html=True)
    st.markdown("🏠 **Dashboard**\n📦 **Samples**\n🧠 **AI Analysis**")
    st.markdown("---")
    st.caption("🟢 **SYSTEM STATUS**")
    st.markdown("<span class='status-pulse'>● All systems operational</span>", unsafe_allow_html=True)

tab_clinico, tab_ingenieria = st.tabs(["📋 Panel de control clínico", "⚙️ Consola de ingeniería"])

with tab_clinico:
    # EL BANNER DIGITAL EN ALTA DEFINICIÓN IDÉNTICO A TU IMAGEN RECREADO POR HTML NATIVO
    st.markdown("""
        <div class="enterprise-card-banner">
            <div>
                <h1 style="margin:0; font-size: 38px; color: #0A1128 !important;">Laboratorios MethylOx</h1>
                <p style="color:#475569; margin-top:5px; font-size:15px; font-weight:500;">Detección temprana mediante ingeniería epigenética</p>
                <div style="display: flex; gap: 15px; margin-top: 25px; font-size: 13px; color: #2563EB; font-weight: 600;">
                    <span>🧬 Metilación de ADN</span><span>🧠 Motor de IA</span><span>🧪 Biopsia líquida</span>
                </div>
            </div>
            <div>
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
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("f_paciente", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        with f1: p_id = st.text_input("ID del paciente / Código de muestra")
        with f2: p_edad = st.number_input("Edad", min_value=1, value=50)
        with f3: p_met = st.number_input("Puntuación de ctDNA", min_value=0.0, max_value=1.0, value=0.35, format="%.4f")
        if st.form_submit_button("🔒 Analizar y guardar datos"):
            if p_id:
                r_c = "High Risk" if p_met >= UMBRAL_CRITICO_DB else "Low Risk"
                conn = sqlite3.connect('methylax_records.db'); c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO pacientes VALUES (?, ?, ?, ?)", (p_id, p_edad, p_met, r_c))
                conn.commit(); conn.close(); st.success("✔️ Saved."); st.rerun()

    conn = sqlite3.connect('methylax_records.db')
    df_p = pd.read_sql_query("SELECT * FROM pacientes", conn); conn.close()
    st.dataframe(df_p, use_container_width=True, hide_index=True)

    # 4 TARJETAS DE KPIs HORIZONTALES
    st.markdown("<br>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown('<div class="essential-card" style="text-align:center;"><span style="color:#64748B; font-size:11px; font-weight:bold;">SENSITIVITY</span><h2 style="color:#2563EB !important; margin:5px 0;">96.4%</h2></div>', unsafe_allow_html=True)
    with k2: st.markdown('<div class="essential-card" style="text-align:center;"><span style="color:#64748B; font-size:11px; font-weight:bold;">SPECIFICITY</span><h2 style="color:#2563EB !important; margin:5px 0;">94.1%</h2></div>', unsafe_allow_html=True)
    with k3: st.markdown('<div class="essential-card" style="text-align:center;"><span style="color:#64748B; font-size:11px; font-weight:bold;">AUC (ROC)</span><h2 style="color:#10B981 !important; margin:5px 0;">0.983</h2></div>', unsafe_allow_html=True)
    with k4: st.markdown('<div class="essential-card" style="text-align:center;"><span style="color:#64748B; font-size:11px; font-weight:bold;">CRITICAL LIMIT</span><h2 style="color:#EF4444 !important; margin:5px 0;">0.5910</h2></div>', unsafe_allow_html=True)

    # CUADRÍCULA SIMÉTRICA DE GRÁFICOS DE TRES COLUMNAS
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.3, 1.3, 1.4])
    
    with c1:
        st.markdown('<div class="essential-card"><h5>🧬 Mapa de Metilación CpG</h5>', unsafe_allow_html=True)
        size_samples = len(df_p) * 2 if not df_p.empty else 10
        df_cpg = pd.DataFrame({
            'Posición Genómica (kb)': np.random.randint(100, 5000, size=size_samples),
            'Nivel Metilación': np.random.uniform(0.1, 0.9, size=size_samples)
        })
        st.scatter_chart(df_cpg, x='Posición Genómica (kb)', y='Nivel Metilación', color='#2563EB', height=200, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="essential-card"><h5>📈 Curva ROC Performance</h5>', unsafe_allow_html=True)
        fpr = np.linspace(0, 1, 20)
        tpr = 1 - np.exp(-4.5 * fpr)
        df_roc = pd.DataFrame({'False Positive Rate': fpr, 'True Positive Rate': tpr})
        st.line_chart(df_roc, x='False Positive Rate', y='True Positive Rate', color='#10B981', height=200, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="essential-card"><h5>📊 Distribución de Riesgo Clínico</h5>', unsafe_allow_html=True)
        df_dist = pd.DataFrame({
            'Low Risk': np.random.normal(0.3, 0.08, 100),
            'Suspicious': np.random.normal(0.52, 0.05, 100),
            'High Risk': np.random.normal(0.75, 0.1, 100)
        })
        st.line_chart(df_dist, color=["#3B82F6", "#A855F7", "#EF4444"], height=200, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab_ingenieria:
    st.title("⚙️ Engineering Console")
    df_b = pd.DataFrame({
        "Hyperparameter": ["UMBRAL_CRITICO_DB", "BACKGROUND_NOISE_PURGE", "DATA_PERSISTENCE"], 
        "Value": ["0.5910 ng/mL", "BCAS3 Excluded", "SQLite3 Relational"]
    })
    st.dataframe(df_b, use_container_width=True, hide_index=True)
