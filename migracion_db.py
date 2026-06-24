import os
import csv
import sqlite3

# =====================================================================
# METHYLOX™ AI PLATFORM - SCRIPT DE MIGRACIÓN GENÓMICA MASIVA LOCAL
# =====================================================================

def migrar_catalogo_a_sqlite(ruta_csv, ruta_db):
    """
    Lee las 761,778 guías del CSV y las inserta de forma
    masiva en la base de datos local 'methyl_clinic.db'.
    """
    if not os.path.exists(ruta_csv):
        print(f"⚠️ Error: No se encuentra el catálogo de la Fase 2 ('{ruta_csv}').")
        return
        
    print(f"🗄️ [SQLite3] Conectando a la base de datos clínica: '{ruta_db}'")
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    
    # Crear la tabla de guías genómicas si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guias_genomicas (
            id_guia TEXT PRIMARY KEY,
            pam TEXT,
            secuencia_guia TEXT,
            estabilidad_dg REAL,
            porcentaje_gc REAL,
            estatus_seguridad TEXT
        )
    """)
    
    cursor.execute("DELETE FROM guias_genomicas")
    print("🧬 Preparando migración masiva por lotes...")
    
    lote = []
    tamano_lote = 10000
    contador_total = 0
    
    with open(ruta_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            lote.append((
                fila.get("ID_Guia"),
                fila.get("PAM"),
                fila.get("Secuencia_Guia"),
                float(fila.get("Estabilidad_dG", 0.0)),
                float(fila.get("Porcentaje_GC", 0.0)),
                fila.get("Estatus_Seguridad", "ULTRA_SEGURA_MAMA")
            ))
            
            if len(lote) >= tamano_lote:
                cursor.executemany("INSERT INTO guias_genomicas VALUES (?, ?, ?, ?, ?, ?)", lote)
                conexion.commit()
                contador_total += len(lote)
                lote = []
                print(f" -> {contador_total} guías indexadas en la base de datos...")
                
        if lote:
            cursor.executemany("INSERT INTO guias_genomicas VALUES (?, ?, ?, ?, ?, ?)", lote)
            conexion.commit()
            contador_total += len(lote)
            
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_secuencia ON guias_genomicas(secuencia_guia)")
    conexion.commit()
    conexion.close()
    
    print(f"\n====================================================================")
    print(f"🏆 ¡INTERCONEXIÓN COMPLETED CON ÉXITO!")
    print(f"🏆 Se indexaron {contador_total} guías reales en tu SQLite3 local.")
    print(f"====================================================================\n")

if __name__ == "__main__":
    archivo_csv = "catalogo_guias_ultra_seguras_mama.csv"
    base_datos = "methyl_clinic.db"
    migrar_catalogo_a_sqlite(archivo_csv, base_datos)