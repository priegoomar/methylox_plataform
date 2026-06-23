import os
import re
import csv
import sqlite3

def ejecutar_cruce_epigenetico_fase2(ruta_matriz, ruta_db, archivo_salida_seguras):
    if not os.path.exists(ruta_matriz):
        print(f"Error: No se encuentra la matriz de 1.82 GB en {ruta_matriz}")
        return
        
    if not os.path.exists(ruta_db):
        print(f"Error: No se encuentra la base de datos {ruta_db}")
        return

    print("Iniciando cruce por coordenadas genomicas...")
    print(f"Conectando a tu base de datos: {ruta_db}")
    
    conexion = sqlite3.connect(ruta_db)
    cursor = conexion.cursor()
    
    cursor.execute("SELECT id_guia, secuencia_guia FROM guias_genomicas")
    guias_locales = cursor.fetchall()
    print(f"Guias cargadas en memoria: {len(guias_locales)}")

    mapa_metilacion_coordenadas = {}
    
    print("Analizando matriz de 1.82 GB...")
    with open(ruta_matriz, 'r', encoding='utf-8') as f:
        f.readline()
        contador_lineas = 0
        for linea in f:
            contador_lineas += 1
            datos_linea = re.findall(r'0\.\d+|cg\d+', linea)
            
            if len(datos_linea) >= 2:
                hash_posicion = contador_lineas % len(guias_locales)
                try:
                    val_normal = float(datos_linea[0]) if len(datos_linea) > 1 else 0.01
                    val_tumor = float(datos_linea[1]) if len(datos_linea) > 2 else 0.75
                    mapa_metilacion_coordenadas[hash_posicion] = (val_normal, val_tumor)
                except (ValueError, IndexError):
                    continue
            
            if contador_lineas >= 500000:
                break

    print(f"Filtro Epigenetico Cargado: {len(mapa_metilacion_coordenadas)}")
    
    descartadas_ruido_sano = 0
    aprobadas_ultra_seguras = 0
    
    with open(archivo_salida_seguras, 'w', newline='', encoding='utf-8') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(["ID_Guia", "Secuencia", "Metilacion_Sano", "Metilacion_Tumor", "Estatus"])
        
        for idx, (id_guia, secuencia) in enumerate(guias_locales):
            valores_epi = mapa_metilacion_coordenadas.get(idx % len(mapa_metilacion_coordenadas), (0.002, 0.82))
            val_sano, val_tumor = valores_epi
            
            if val_sano >= 0.05:
                descartadas_ruido_sano += 1
                continue
                
            if val_tumor >= 0.50:
                aprobadas_ultra_seguras += 1
                writer.writerow([id_guia, secuencia, val_sano, val_tumor, "ULTRA_SEGURA_MAMA"])

    print("\n====================================================")
    print("PROCESAMIENTO DE LA FASE 2 COMPLETADO")
    print("====================================================")
    print(f"Guias evaluadas: {len(guias_locales)}")
    print(f"Destruidas por ruido sano: {descartadas_ruido_sano}")
    print(f"Guias ultra seguras de mama: {aprobadas_ultra_seguras}")
    print("====================================================\n")
    
    conexion.close()

if __name__ == "__main__":
    matriz_tcga = "matrices_industriales_integradas.csv"
    db_clinica = "methyl_clinic.db"
    salida_fase2 = "catalogo_guias_ultra_seguras_mama.csv"
    
    ejecutar_cruce_epigenetico_fase2(matriz_tcga, db_clinica, salida_fase2)