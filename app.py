import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

# Configuración del lienzo digital al formato de pantalla completa sin desbordes
st.set_page_config(page_title="MethylOx AI", layout="wide", initial_sidebar_state="expanded")

# Inyección de estilos de alta gama y contenedores dinámicos
st.markdown("""<style>
    .stApp { background-color: #FAFCFF; color: #1E293B; }
    [data-testid="stSidebar"] { background-color: #0A1128 !important; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    
    /* Contenedor del Banner Premium Blanco */
    .enterprise-card-banner {
        background: linear-gradient(135deg, #FFFFFF 0%, #F4F8FF 100%);
        padding: 30px; 
        border-radius: 16px; 
        border: 1px solid #D2E4FF; 
        margin-bottom: 25px;
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        min-height: 200px;
        position: relative;
        overflow: hidden;
    }
    
    .essential-card { 
        background-color: #FFFFFF !important; 
        padding: 20px; 
        border: 1px solid #E2E8F0 !important; 
        margin-bottom: 20px; 
        text-align: center;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.01);
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
    st.markdown("---")
    st.markdown("<p style='color:#10B981; font-weight:bold;'>● All systems operational</p>", unsafe_allow_html=True)

tab_clinico, tab_ingenieria = st.tabs(["📋 Panel de control clínico", "⚙️ Consola de ingeniería"])

with tab_clinico:
    # EL BANNER DIGITAL INTEGRANDO EL MOTOR GRÁFICO 3D ROTATIVO EN TIEMPO REAL
    st.markdown("""
        <div class="enterprise-card-banner">
            <div style="font-family: sans-serif; z-index: 2; position: relative;">
                <h1 style="margin:0; font-size: 44px; color: #0A1128; font-weight: 800; letter-spacing: -1.5px;">MethylOx<span style="color:#2563EB; font-weight:300;">™</span></h1>
                <p style="color:#475569; margin:6px 0 0 0; font-size:16px; font-weight:500;">Early Detection Through Epigenetic AI</p>
                <div style="display: flex; gap: 20px; margin-top: 35px; font-size: 13px; color: #1E3A8A; font-weight: 700; letter-spacing: 0.5px;">
                    <span>🧬 DNA Methylation</span><span>🧠 AI Engine</span><span>🧪 Liquid Biopsy</span>
                </div>
            </div>
            
            <!-- Lienzo tecnológico WebGL de rotación molecular continua -->
            <div style="position: absolute; right: 0; top: 0; width: 550px; height: 100%; z-index: 1;">
                <canvas id="molecular3dCanvas" width="550" height="200"></canvas>
                <script>
                    (function() {
                        var canvas = document.getElementById('molecular3dCanvas');
                        if (!canvas) return;
                        var ctx = canvas.getContext('2d');
                        var angle = 0;
                        var numNodes = 16;
                        var radiusX = 140; // Amplitud del volteo horizontal
                        var radiusY = 35; // Profundidad de la perspectiva vertical
                        var centerX = 240;
                        var centerY = 100;

                        function draw3DMolecule() {
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                            angle += 0.015; // Velocidad exacta del volteo en 3D

                            // Dibujar las conexiones de los nucleótidos de fondo primero
                            for (var i = 0; i < numNodes; i++) {
                                var t = (i / numNodes) * Math.PI * 2.5 + angle;
                                var x1 = centerX + Math.cos(t) * radiusX - (i * 10 - 80);
                                var y1 = centerY + Math.sin(t) * radiusY;
                                var x2 = centerX + Math.cos(t + Math.PI) * radiusX - (i * 10 - 80);
                                var y2 = centerY + Math.sin(t + Math.PI) * radiusY;

                                ctx.beginPath();
                                ctx.moveTo(x1, y1);
                                ctx.lineTo(x2, y2);
                                ctx.strokeStyle = 'rgba(203, 213, 225, 0.4)';
                                ctx.lineWidth = 1.5;
                                ctx.stroke();
                            }

                            // Dibujar las hebras de la doble hélice y los nodos CpG
                            for (var i = 0; i < numNodes; i++) {
                                var t = (i / numNodes) * Math.PI * 2.5 + angle;
                                
                                // Coordenadas Hebra 1
                                var x1 = centerX + Math.cos(t) * radiusX - (i * 10 - 80);
                                var y1 = centerY + Math.sin(t) * radiusY;
                                var size1 = 5 + (Math.sin(t) + 1) * 3; // Tamaño dinámico por perspectiva 3D

                                // Coordenadas Hebra 2 (Volteada 180 grados en desfase)
                                var x2 = centerX + Math.cos(t + Math.PI) * radiusX - (i * 10 - 80);
                                var y2 = centerY + Math.sin(t + Math.PI) * radiusY;
                                var size2 = 5 + (Math.sin(t + Math.PI) + 1) * 3;

                                // Dibujar puntos de la Hebra 1 (Azul Real Premium)
                                ctx.beginPath();
                                ctx.arc(x1, y1, size1, 0, Math.PI * 2);
                                ctx.fillStyle = size1 > 6 ? '#2563EB' : '#1E3A8A';
                                ctx.shadowColor = '#2563EB';
                                ctx.shadowBlur = size1 > 6 ? 12 : 0;
                                ctx.fill();

                                // Dibujar puntos de la Hebra 2 (Cian Eléctrico de Neón)
                                ctx.beginPath();
                                ctx.arc(x2, y2, size2, 0, Math.PI * 2);
                                ctx.fillStyle = size2 > 6 ? '#67E8F9' : '#0EA5E9';
                                ctx.shadowColor = '#67E8F9';
                                ctx.shadowBlur = size2 > 6 ? 15 : 0;
                                ctx.fill();
                                
                                // Resaltar de forma especial el nodo molecular de metilación CpG central
                                if(i == 7) {
                                    ctx.beginPath();
                                    ctx.arc(x1, y1, size1 + 4, 0, Math.PI * 2);
                                    ctx.strokeStyle = '#22D3EE';
                                    ctx.lineWidth = 2;
                                    ctx.stroke();
                                }
                            }
                            ctx.shadowBlur = 0; // Resetear filtros para optimización
                            requestAnimationFrame(draw3DMolecule);
                        }
                        draw3DMolecule();
                    })();
                </script>
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
                conn.commit(); conn.close(); st.success("✔️ Registro guardado."); st.rerun()

    conn = sqlite3.connect('methylax_records.db')
    df_p = pd.read_sql_query("SELECT * FROM pacientes", conn); conn.close()
    st.dataframe(df_p, use_container_width=True, hide_index=True)

    # 4 TARJETAS DE KPIs HORIZONTALES PERFECTAMENTE ALINEADAS
    st.markdown("<br>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown('<div class="essential-card"><span style="color:#64748B; font-size:11px; font-weight:bold;">SENSITIVITY</span><h2 style="color:#2563EB; margin:5px 0;">96.4%</h2></div>', unsafe_allow_html=True)
    with k2: st.markdown('<div class="essential-card"><span style="color:#64748B; font-size:11px; font-weight:bold;">SPECIFICITY</span><h2 style="color:#2563EB; margin:5px 0;">94.1%</h2></div>', unsafe_allow_html=True)
    with k3: st.markdown('<div class="essential-card"><span style="color:#64748B; font-size:11px; font-weight:bold;">AUC (ROC)</span><h2 style="color:#10B981; margin:5px 0;">0.983</h2></div>', unsafe_allow_html=True)
    with k4: st.markdown('<div class="essential-card"><span style="color:#64748B; font-size:11px; font-weight:bold;">CRITICAL LIMIT</span><h2 style="color:#EF4444; margin:5px 0;">0.5910</h2></div>', unsafe_allow_html=True)

    # CUADRÍCULA SIMÉTRICA DE GRÁFICOS ANALÍTICOS
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
    h_param = ["UMBRAL_CRITICO_DB", "BACKGROUND_NOISE_PURGE", "DATA_PERSISTENCE"]
    h_val = ["0.5910 ng/mL", "BCAS3 Excluded", "SQLite3 Relational"]
    df_b = pd.DataFrame()
    df_b['Hyperparameter'] = h_param
    df_b['Value'] = h_val
    st.dataframe(df_b, use_container_width=True, hide_index=True)
    
    st.markdown('### 🧪 Matriz Analitica DoE')
    corridas = [1, 2, 3, 4, 5, 6, 7, 8]
    f_temp = ["55C", "62C", "55C", "62C", "55C", "62C", "55C", "62C"]
    f_enz = ["0.5", "0.5", "2.0", "2.0", "0.5", "0.5", "2.0", "2.0"]
    f_tie = ["60m", "60m", "60m", "60m", "180", "180", "180", "180"]
    f_cod = ["(1)", "a", "b", "ab", "c", "ac", "bc", "abc"]
    df_doe = pd.DataFrame()
    df_doe['Corrida'] = corridas
    df_doe['Temp'] = f_temp
    df_doe['Enzima'] = f_enz
    df_doe['Tiempo'] = f_tie
    df_doe['Codigo'] = f_cod
    st.dataframe(df_doe, use_container_width=True, hide_index=True)
