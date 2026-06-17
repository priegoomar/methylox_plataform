import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

UMBRAL_GLOBAL = 0.5910

def iniciar_base_datos():
    conn = sqlite3.connect("methyl_clinic.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS pacientes (id TEXT PRIMARY KEY, edad INTEGER, ctdna REAL, clasificacion TEXT)")
    conn.commit()
    conn.close()

def procesar_diagnostico_clinico(patient_id, patient_age, ctdna_score):
    if ctdna_score >= UMBRAL_GLOBAL:
        resultado = "High Risk - CPEB4+ Detected"
    else:
        resultado = "Low Risk - Baseline Stable"
    return resultado

def registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado):
    conn = sqlite3.connect("methyl_clinic.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO pacientes VALUES (?, ?, ?, ?)", (patient_id, patient_age, ctdna_score, resultado))
        conn.commit()
        estatus = "Éxito"
    except sqlite3.IntegrityError:
        estatus = "Duplicado"
    finally:
        conn.close()
    return estatus

def generar_pdf_clinico(patient_id, patient_age, ctdna_score, resultado):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    reporte = f"METHYLOX LABS REPORT\nFecha: {fecha_actual}\nID Paciente: {patient_id}\nEdad: {patient_age}\nScore ctDNA: {ctdna_score:.4f}\nResultado: {resultado}"
    return reporte
