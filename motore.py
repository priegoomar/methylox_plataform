# motores.py - BACKEND PURO (Temática Cleanroom)
import sqlite3
import pandas as pd
import numpy as np

UMBRAL_GLOBAL = 0.5910

def iniciar_base_datos():
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
    if ctdna_score >= UMBRAL_GLOBAL:
        resultado = "High Risk - CPEB4+ Detected"
    else:
        resultado = "Low Risk - Baseline Stable"
    return resultado

def registrar_paciente_db(patient_id, patient_age, ctdna_score, resultado):
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

def ejecutar_motores_crispr_unificados(df_origen):
    df_f1 = df_origen[df_origen["ctdna_score"] >= UMBRAL_GLOBAL]
    condicion_pam = df_f1["secuencia_pam"].str.contains("TTT[ACG]", na=False)
    condicion_gc = (df_f1["porcentaje_gc"] >= 40) & (df_f1["porcentaje_gc"] <= 60)
    df_final = df_f1[condicion_pam & condicion_gc]
    return df_final
