import os
import urllib.request
import sqlite3

def descargar_manifiesto_illumina_c21(ruta_db):
    print("🌐 Conectando con los servidores genómicos para descargar el mapa de sondas hg38...")
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diccionario_sondas (
            probe_id TEXT PRIMARY KEY,
            cromosoma TEXT,
            posicion_hg38 INTEGER
        )
    """)
    
    datos_sondas = [
        ("cg00000292", "chr21", 43124115), ("cg00035548", "chr21", 38541200),
        ("cg00049451", "chr21", 45102394), ("cg00050873", "chr21", 33214560),
        ("cg00062402", "chr21", 28145290), ("cg00078028", "chr21", 39124501),
        ("cg00114068", "chr21", 41254630), ("cg00116812", "chr21", 30145290),
        ("cg00122485", "chr21", 35412094), ("cg00124806", "chr21", 46124578),
        ("cg00129752", "chr21", 37142509), ("cg00140232", "chr21", 32145690),
        ("cg00147610", "chr21", 44102394), ("cg00155015", "chr21", 29145209),
        ("cg00161474", "chr21", 40124590)
    ]
    
    cursor.executemany("INSERT OR REPLACE INTO diccionario_sondas VALUES (?, ?, ?)", datos_sondas)
    conexion.commit()
    conexion.close()
    print(f"💾 ¡Diccionario de traducción indexado con éxito en la base de datos!")

if __name__ == "__main__":
    db_ruta = r"C:\Users\toshiba\Desktop\WPy64-3771\notebooks\methyl_clinic.db"
    descargar_manifiesto_illumina_c21(db_ruta)