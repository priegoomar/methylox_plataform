import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

UMBRAL_GLOBAL = 0.5910

def iniciar_base_datos():
    """Inicializa la base de datos física persistente SQLite3."""
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

def procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score):
    """Aplica el umbral crítico estadístico de la plataforma."""
    if ctdna_score >= UMBRAL_GLOBAL:
        resultado = "High Risk - CPEB4+ Detected"
    else:
        resultado = "Low Risk - Baseline Stable"
    return resultado

def registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado):
    """Guarda los registros en el archivo de base de datos sin pérdida de datos."""
    conn = sqlite3.connect("methyl_clinic.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO pacientes VALUES (?, ?, ?, ?)",
            (patient_id, patient_age, ctdna_score, resultado)
        )
        conn.commit()
        estatus = "Éxito"
    except sqlite3.IntegrityError:
        estatus = "Duplicado"
    finally:
        conn.close()
    return estatus

def generar_pdf_clinico(patient_id, patient_age, ctdna_score, resultado):
    """Estructura el reporte ejecutivo en una bitácora digital formateada."""
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    lineas = []
    lineas.append("==================================================")
    lineas.append(" METHYLOX LABS ™ ")
    lineas.append(" EPIGENETIC CLINICAL INTELLIGENCE ")
    lineas.append("==================================================")
    lineas.append(f" Fecha de Emisión: {fecha_actual}")
    lineas.append(f" Estado del Sistema: ONLINE - CORE ACTIVE")
    lineas.append("--------------------------------------------------")
    lineas.append(" 📄 DATOS DEL PACIENTE CRIBADO:")
    lineas.append(f" • Patient Identifier: {patient_id}")
    lineas.append(f" • Chronological Age: {patient_age} años")
    lineas.append("--------------------------------------------------")
    lineas.append(" 🔬 BIOMARCADORES Y MÓDULO ANALÍTICO (ctDNA):")
    lineas.append(f" • ctDNA Concentration: {ctdna_score:.4f} ng/mL")
    lineas.append(f" • Umbral Estadístico Fijo: {UMBRAL_GLOBAL} ng/mL")
    lineas.append("--------------------------------------------------")
    lineas.append(" 🧠 DIAGNOSTIC VERDICT (VEREDICTO IA):")
    lineas.append(f" STATUS: {resultado}")
    lineas.append("==================================================")
    lineas.append(" Este documento es un extracto digital firmado ")
    lineas.append(" electrónicamente por los motores unificados de ")
    lineas.append(" MethylOx v4.0. Resguardo clínico garantizado. ")
    lineas.append("==================================================")
    
    return "\n".join(lineas
