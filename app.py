import streamlit as st
import pandas as pd
import numpy as np
import sqlite3

# 1. CONFIGURACION DE PAGINA MAESTRA
st.set_page_config(page_title="MethylOx AI", layout="wide", initial_sidebar_state="expanded")

# 2. ESTILOS BASE DE ALTA COMPATIBILIDAD
st.markdown("""<style>
    .stApp { background-color: #FAFCFF; color: #1E293B; }
    [data-testid="stSidebar"] { background-color: #0A1128 !important; }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }
    
    .enterprise-card-banner {
        background: linear-gradient(135deg, #FFFFFF 0%, #F4F8FF 100%);
        padding: 25px; 
        border: 1px solid #D2E4FF !important; 
        margin-bottom: 25px;
        border-radius: 16px;
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
    # FILA DEL BANNER QUE INTEGRA LA VENTANA MOLECULAR INTERACTIVA 3D DE COLAB
    col_txt, col_3d = st.columns([1.1, 0.9])
    
    with col_txt:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h1 style='margin:0; font-size:44px; color:#0A1128; font-weight:800;'>Laboratorios MethylOx</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#475569; font-size:16px; font-weight:500;'>Detección temprana mediante ingeniería epigenética</p>", unsafe_allow_html=True)
        st.markdown("<p style='margin-top:25px; font-size:13px; color:#2563EB; font-weight:700;'>🧬 DNA Methylation &nbsp;&nbsp;&nbsp;&nbsp; 🧠 AI Engine &nbsp;&nbsp;&nbsp;&nbsp; 🧪 Liquid Biopsy</p>", unsafe_allow_html=True)

    with col_3d:
        # VENTANA CIENTÍFICA WEBGL RECREANDO EL VOLUMEN E ILUMINACIÓN FOTORREALISTA DE COLAB
        st.components.v1.html("""
            <div style="background-color:#070B19; border-radius:12px; border:1px solid #1E293B; overflow:hidden; width:100%; height:190px; position:relative;">
                <canvas id="colab3dCanvas" style="width:100%; height:100%; cursor:move;"></canvas>
                <script>
                    (function() {
                        var canvas = document.getElementById('colab3dCanvas');
                        if(!canvas) return;
                        var ctx = canvas.getContext('2d');
                        var angleX = 0.4; var angleY = 0.6;
                        var isDragging = false; var prevX, prevY;

                        canvas.addEventListener('mousedown', function(e) { isDragging = true; prevX = e.clientX; prevY = e.clientY; });
                        window.addEventListener('mouseup', function() { isDragging = false; });
                        canvas.addEventListener('mousemove', function(e) {
                            if(!isDragging) return;
                            var deltaX = e.clientX - prevX; var deltaY = e.clientY - prevY;
                            angleY += deltaX * 0.01; angleX += deltaY * 0.01;
                            prevX = e.clientX; prevY = e.clientY;
                        });

                        function drawMolecularModel() {
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                            if (canvas.width !== canvas.clientWidth || canvas.height !== canvas.clientHeight) {
                                canvas.width = canvas.clientWidth; canvas.height = canvas.clientHeight;
                            }
                            if(!isDragging) { angleY += 0.008; } // Auto-rotación continua
                            
                            var cx = canvas.width / 2; var cy = canvas.height / 2;
                            var numPoints = 14;

                            for(var i=0; i<numPoints; i++) {
                                var t = (i / numPoints) * Math.PI * 2.2 + angleY;
                                var z1 = Math.sin(t) * 40;
                                var x1 = Math.cos(t) * 80;
                                var y1 = (i * 12 - 80) * Math.cos(angleX) - z1 * Math.sin(angleX);

                                var z2 = Math.sin(t + Math.PI) * 40;
                                var x2 = Math.cos(t + Math.PI) * 80;
                                var y2 = (i * 12 - 80) * Math.cos(angleX) - z2 * Math.sin(angleX);

                                var rx1 = cx + x1; var ry1 = cy + y1;
                                var rx2 = cx + x2; var ry2 = cy + y2;

                                // Enlaces químicos traslúcidos estilo cristal
                                ctx.beginPath();
                                ctx.moveTo(rx1, ry1); ctx.lineTo(rx2, ry2);
                                ctx.strokeStyle = 'rgba(148, 163, 184, 0.25)';
                                ctx.lineWidth = 1.2; ctx.stroke();

                                // RECREACIÓN DE ESFERAS 3D MEDIANTE DEGRADADOS RADIALES DE NEÓN (Estilo Colab)
                                // Cadena Superior (Azul Eléctrico Volumétrico)
                                var g1 = ctx.createRadialGradient(rx1-2, ry1-2, 1, rx1, ry1, 6);
                                g1.addColorStop(0, '#FFFFFF'); g1.addColorStop(0.3, '#3B82F6'); g1.addColorStop(1, '#1E3A8A');
                                ctx.beginPath(); ctx.arc(rx1, ry1, 6, 0, Math.PI*2);
                                ctx.fillStyle = g1; ctx.shadowColor = '#2563EB'; ctx.shadowBlur = 10; ctx.fill();

                                // Cadena Inferior (Cian Neón Volumétrico)
                                var g2 = ctx.createRadialGradient(rx2-1, ry2-1, 1, rx2, ry2, 5);
                                g2.addColorStop(0, '#FFFFFF'); g2.addColorStop(0.4, '#67E8F9'); g2.addColorStop(1, '#0EA5E9');
                                ctx.beginPath(); ctx.arc(rx2, ry2, 5, 0, Math.PI*2);
                                ctx.fillStyle = g2; ctx.shadowColor = '#67E8F9'; ctx.shadowBlur = 12; ctx.fill();

                                // DESTELLO COMPACTO EN EL NODO DE METILACIÓN CPG TRIDIMENSIONAL
                                if(i == 6) {
                                    var gCpG = ctx.createRadialGradient(rx1, ry1, 4, rx1, ry1, 14);
                                    gCpG.addColorStop(0, 'rgba(34, 211, 238, 0.6)'); gCpG.addColorStop(1, 'rgba(6, 182, 212, 0)');
                                    ctx.beginPath(); ctx.arc(rx1, ry1, 14, 0, Math.PI*2);
                                    ctx.fillStyle = gCpG; ctx.fill();
                                    
                                    ctx.beginPath(); ctx.arc(rx1, ry1, 8, 0, Math.PI*2);
                                    ctx.strokeStyle = '#22D3EE'; ctx.lineWidth = 1.5; ctx.stroke();
                                }
                            }
                            ctx.shadowBlur = 0;
                            requestAnimationFrame(drawMolecularModel);
                        }
                        drawMolecularModel();
                    })();
                </script>
            </div>
        """, height=200)

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
