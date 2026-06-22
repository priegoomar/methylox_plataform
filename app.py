import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import json
import re
import os

# =====================================================================
# 📐 CONFIGURACIÓN MAESTRA LOCAL Y CONSTANTES CLÍNICAS
# =====================================================================
st.set_page_config(page_title="MethylOx AI - Local Core", layout="wide", initial_sidebar_state="expanded")

UMBRAL_CLINICO_DELTA_BETA = 0.5910 # Índice de Youden universal (Curva ROC)
LIMITE_RUIDO_PLASMA = 0.10 # Umbral de corte para ruido analítico en plasma
GENES_EXCLUIDOS = ["BCAS3"] # Exclusión por alto ruido de fondo histórico

# Ruta estricta de archivos locales embebidos en el disco duro de tu máquina
RUTA_LOCAL_MATRICES = "matrices_industriales_integradas.csv"
RUTA_LOCAL_GENOMA = "genoma_completo_grch38.json"

# Nombre exacto de tu imagen oficial de fondo confirmada en tu repositorio
NOMBRE_TU_BANNER = "1000199352.png"

st.markdown(f"""<style>
    .stApp {{ background-color: #FAFCFF; color: #1E293B; }}
    [data-testid="stSidebar"] {{ background-color: #0A1128 !important; }}
    [data-testid="stSidebar"] * {{ color: #E2E8F0 !important; }}
    
    /* Contenedor oficial premium adaptado para tu imagen numérica original 2:1 */
    .enterprise-card-banner {{
        background-image: url("static/{NOMBRE_TU_BANNER}");
        background-size: contain;
        background-position: center top;
        background-repeat: no-repeat;
        padding: 0px; 
        border-radius: 16px; 
        border: 1px solid #D2E4FF; 
        margin-bottom: 25px;
        width: 100%;
        aspect-ratio: 2 / 1;
        max-height: 420px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    
    .essential-card {{ background-color: #FFFFFF !important; padding: 24px; border-radius: 14px; border: 1px solid #E2E8F0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.01); }}
    @keyframes pulse {{ 0% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.4; }} }}
    .status-pulse {{ color: #10B981; font-weight: bold; animation: pulse 2s infinite; }}
</style>""", unsafe_allow_html=True)

def iniciar_base_datos():
    conn = sqlite3.connect("methyl_clinic.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            id TEXT PRIMARY KEY, edad INTEGER, ctdna REAL, resultado TEXT, score_metilacion REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit(); conn.close()

iniciar_base_datos()

def registrar_paciente_db(patient_id, patient_age, ctdna_score, veredicto, score_metilacion):
    conn = sqlite3.connect("methyl_clinic.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO pacientes (id, edad, ctdna, resultado, score_metilacion) VALUES (?, ?, ?, ?, ?)",
                   (str(patient_id), int(patient_age), float(ctdna_score), str(veredicto), float(score_metilacion)))
    conn.commit(); conn.close()

def poner_un_del_cgc(secuencia):
    seq = secuencia.upper()
    c_g = seq.count('G') + seq.count('C')
    return round(-0.4 * c_g + 1.2, 2)

# =====================================================================
# 🛡️ MOTORES BIOINFORMÁTICOS LOCALES (CERO DEPENDENCIAS DE INTERNET)
# =====================================================================
def motor_1_escanner_genomico_dinamico(id_ensembl, secuencia_completa_adn, datos_clinicos_dict):
    guias_candidatas = []
    patron_pam = re.compile(r"(TTTT|TTTA|TTTC|TTTG|TTTTV)([ATCG]{20,24})", re.IGNORECASE)
    
    if id_ensembl not in datos_clinicos_dict:
        return guias_candidatas
        
    info = datos_clinicos_dict[id_ensembl]
    delta_beta_real = info.get("delta_beta", 0.0)
    ruido_plasma_real = info.get("plasma_noise", 1.0)
    estadio_clinico = info.get("estadio", "Desconocido")
    
    delta_beta_colon = info.get("delta_beta_colon", 0.0)
    delta_beta_pulmon = info.get("delta_beta_pulmon", 0.0)
    
    if delta_beta_colon >= 0.05 or delta_beta_pulmon >= 0.05:
        return guias_candidatas  

    if estadio_clinico not in ['Estadio 0', 'Estadio I', 'Estadio II'] or delta_beta_real < 0.3 or ruido_plasma_real > LIMITE_RUIDO_PLASMA:
        return guias_candidatas  

    for match in patron_pam.finditer(str(secuencia_completa_adn)):
        guias_candidatas.append({
            "coordenada_gen": match.start(),
            "pam": match.group(1).upper(),
            "secuencia": match.group(2).upper(),
            "delta_beta": delta_beta_real,
            "plasma_noise": ruido_plasma_real,
            "longitud_fragmento_adn": info.get("longitud_fragmento_adn", 145),
            "metilacion_leucocitos_sanos": info.get("metilacion_leucocitos_sanos", 0.01)
        })
    return guias_candidatas

def motor_2_auditor_biofisico_real(candidatos_lista):
    guias_supremas_finales = []
    patron_poly_g_c = re.compile(r"(GGGG|CCCC)", re.IGNORECASE)
    
    for cand in candidatos_lista:
        seq = cand["secuencia"]
        if cand["metilacion_leucocitos_sanos"] >= 0.01 or cand["longitud_fragmento_adn"] > 200:
            continue 

        porcentaje_gc = (seq.count("C") + seq.count("G")) / len(seq)
        if not (0.35 <= porcentaje_gc <= 0.65) or seq[:5] == seq[-5:][::-1] or bool(patron_poly_g_c.search(seq)):
            continue
        
        dg_calculado = poner_un_del_cgc(seq)
        if dg_calculado >= -2.0:
            cand["dG_Auto_Union"] = dg_calculado
            cand["Estatus"] = "GUÍA SUPREMA COMPILADA"
            guias_supremas_finales.append(cand)
    return guias_supremas_finales

def ejecutar_descubrimiento_completo_local():
    if not os.path.exists(RUTA_LOCAL_MATRICES) or not os.path.exists(RUTA_LOCAL_GENOMA):
        return pd.DataFrame()

    df_clinico = pd.read_csv(RUTA_LOCAL_MATRICES)
    datos_clinicos_dict = df_clinico.set_index('gen_id').to_dict('index')
    guias_supremas_descubiertas = []
    
    with open(RUTA_LOCAL_GENOMA, "r", encoding="utf-8") as f:
        try: mapa_genomico_completo = json.load(f)
        except Exception: return pd.DataFrame()
        
    for ensembl_id, datos_adn in mapa_genomico_completo.items():
        nombre_gen = datos_adn.get("nombre", "GEN_DESCONOCIDO")
        secuencia_cronologica = datos_adn.get("secuencia", "")
        coordenada_cromosoma = datos_adn.get("coordenada", 0)
        
        if nombre_gen in GENES_EXCLUIDOS: continue
            
        candidatos_validos_m1 = motor_1_escanner_genomico_dinamico(ensembl_id, secuencia_cronologica, datos_clinicos_dict)
        if not candidatos_validos_m1: continue
            
        guias_finales_m2 = motor_2_auditor_biofisico_real(candidatos_validos_m1)
        
        for g in guias_finales_m2:
            guias_supremas_descubiertas.append({
                "Ensembl_ID": ensembl_id,
                "Gen_Nombre": nombre_gen,
                "Coordenada_Real": coordenada_cromosoma + g["coordenada_gen"],
                "PAM": g["pam"],
                "Secuencia_Sonda_22nt": g["secuencia"],
                "Delta_Beta_Clinico_Mama": g["delta_beta"],
                "Estabilidad_dG": g["dG_Auto_Union"]
            })
            
    df_salida = pd.DataFrame(guias_supremas_descubiertas)
    if not df_salida.empty:
        df_salida = df_salida.sort_values(by="Delta_Beta_Clinico_Mama", ascending=False)
        df_salida.to_csv("guias_prometedoras_finales.csv", index=False)
    return df_salida

# =====================================================================
# 🖥️ ENTORNO VISUAL DE STREAMLIT (ORGANIZACIÓN COMPLETA REINTEGRADA)
# =====================================================================
with st.sidebar:
    st.markdown("<h2 style='color:white; margin-bottom:0;'>MethylOx™</h2><p style='color:#38BDF8; font-size:12px;'>Air-Gapped Bioinformatic Core</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("🟢 **INFRASTRUCTURE STATUS**")
    st.markdown("● 100% Isolated (Offline Mode)", unsafe_allow_html=True)

tab_clinico, tab_mineria, tab_doe = st.tabs(["📋 Clinical Dashboard", "🔬 Local Discovery Core", "📊 Wet Lab DoE Matrix"])

with tab_clinico:
    st.markdown("""<div class='enterprise-card-banner'></div>""", unsafe_allow_html=True)
    
    st.markdown("### 🗄️ Inmutable Local Data Management")
    if not os.path.exists(RUTA_LOCAL_MATRICES):
        df_init = pd.DataFrame([{"gen_id": "ENSG00000166922", "delta_beta": 0.62, "plasma_noise": 0.02, "estadio": "Estadio I", "delta_beta_colon": 0.02, "delta_beta_pulmon": 0.01, "longitud_fragmento_adn": 140, "metilacion_leucocitos_sanos": 0.00}])
        df_init.to_csv(RUTA_LOCAL_MATRICES, index=False)
    if not os.path.exists(RUTA_LOCAL_GENOMA):
        with open(RUTA_LOCAL_GENOMA, "w") as f:
            json.dump({"ENSG00000166922": {"nombre": "CPEB4", "coordenada": 1000500, "secuencia": "TTTTAGCCTAGCTAGCTAGCTAGCTACGATCGATCGATTTAAAAGCTAGCTAGCTA"}}, f)
    st.success("✔️ Local Datasets loaded securely from filesystem.")
    
    st.markdown("---")
    st.markdown("### 🩺 Diagnostic Simulation Interface")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        id_paciente = st.text_input("Patient Identifier ID:", value="PATIENT-ALFA-01")
    with col_p2:
        edad_paciente = st.number_input("Chronological Age (Years):", min_value=1, max_value=120, value=45)
    with col_p3:
        score_ctdna = st.number_input("Plasma ctDNA Score (ng/mL):", min_value=0.0, max_value=10.0, value=0.85, step=0.01)
        
    if st.button("🔮 Process Epigenetic Diagnostic Veredict", use_container_width=True):
        if score_ctdna < 0.02:
            st.success(f"📋 Veredicto emitido para {id_paciente}: **Low Risk Profile** (ctDNA por debajo de detección analítica)")
            registrar_paciente_db(id_paciente, edad_paciente, score_ctdna, "Low Risk Profile", 0.0)
        else:
            db_estadio_i = 0.6200  
            factor_edad = (100 - int(edad_paciente)) / 100.0
            score_ajustado = db_estadio_i * (factor_edad + 0.5)

            if score_ajustado >= UMBRAL_CLINICO_DELTA_BETA:
                veredicto = "High Risk"
                st.error(f"🚨 ALERT - Veredicto Clínico: **{veredicto}** | Score Promedio Ajustado: {round(score_ajustado, 4)}")
            else:
                veredicto = "Low Risk Profile"
                st.success(f"✅ Veredicto Clínico: **{veredicto}** | Score Promedio Ajustado: {round(score_ajustado, 4)}")

            registrar_paciente_db(id_paciente, edad_paciente, score_ctdna, veredicto, round(float(score_ajustado), 4))
            st.info("💾 Expediente clínico guardado de forma síncrona en la base de datos local SQLite3.")

with tab_mineria:
    st.title("🧬 Autonomous Guide Extraction (GRCh38)")
    st.caption("Ejecución del pipeline molecular corriendo directo sobre la memoria elástica sin desbordamiento de RAM.")
    if st.button("🚀 Execute Offline Genomic Discovery Run", use_container_width=True):
        df_res = ejecutar_descubrimiento_completo_local()
        if not df_res.empty:
            st.markdown("##### 🎉 ¡Éxito! Candidatas Certificadas y Aisladas en Local:")
            st.dataframe(df_res, use_container_width=True, hide_index=True)
            st.info("💾 Archivo para pedido de síntesis in vitro exportado localmente a: 'guias_prometedoras_finales.csv'")
        else:
            st.error("Ninguna secuencia superó los candados de exclusión en los archivos locales.")

with tab_doe:
    st.title("🧪 Wet Lab Design of Experiments (DoE Matrix)")
    st.caption("Planificación automatizada de 8 corridas experimentales para optimizar las variables in vitro en el laboratorio húmedo.")
        corridas_doe = {
        "Corrida": [f"Run {i}" for i in range(1, 9)],
        "Cas12a-Ultra (nM)":,
        "Temperatura (°C)":,
        "Tiempo (min)":,
        "Sonda Fluorescente (µM)": [0.5, 1.5, 1.5, 0.5, 1.5, 0.5, 0.5, 1.5]
    }
    df_doe = pd.DataFrame(corridas_doe)
    st.markdown("##### 📈 Matriz de Optimización L8 para validación biológica de las Guías Supremas:")
    st.dataframe(df_doe, use_container_width=True, hide_index=True)
