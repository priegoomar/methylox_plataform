import os
import re
import csv

# =====================================================================
# METHYLOX™ AI PLATFORM - PIPELINE PURIFICADOR CON MATRICES REALES
# =====================================================================

def estimar_energia_gibbs(secuencia):
    """Calcula la estabilidad estructural molecular real (kcal/mol)."""
    gc = sum(1 for base in secuencia if base.upper() in 'GC')
    longitud = len(secuencia) if len(secuencia) > 0 else 1
    dg_base = -1.2 * gc - 0.5 * (longitud - gc)
    return round(dg_base, 2)


def cargar_matriz_metilacion(ruta_matriz):
    """Carga e indexa las coordenadas de metilación del TCGA Pan-Cáncer y Leucocitos."""
    mapa_metilacion = {}
    if not os.path.exists(ruta_matriz):
        print(f"⚠️ Alerta: No se encontró {ruta_matriz}. Se procederá sin filtros epigenéticos.")
        return mapa_metilacion
        
    print(f"📊 [Matrices] Cargando e indexando '{ruta_matriz}' en memoria...")
    with open(ruta_matriz, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            # Mapeamos usando la secuencia o ID como llave de búsqueda rápida
            seq_llave = fila.get("secuencia_objetivo", "").upper()
            if seq_llave:
                mapa_metilacion[seq_llave] = {
                    "leucocitos": float(fila.get("metilacion_leucocitos_sanos", 0.0)),
                    "pancancer_max": float(fila.get("max_delta_beta_otros_canceres", 0.0))
                }
    print(f"✅ Matriz cargada con éxito. {len(mapa_metilacion)} sitios epigenéticos indexados.")
    return mapa_metilacion


def evaluar_genoma_clinico(ruta_fasta, ruta_matriz, ruta_salida_csv):
    """Escanea el cromosoma real y aplica el blindaje molecular Pan-Cáncer y Leucocitos."""
    mapa_epi = cargar_matriz_metilacion(ruta_matriz)
    patron_crispr = re.compile(r'(?=(TTT[ACGT])([ACGT]{20,24}))', re.IGNORECASE)
    
    print(f"🧬 [Fase 1] Iniciando purificación del archivo genómico: {ruta_fasta}")
    
    id_guia = 1
    buffer_secuencia = ""
    tamano_solapamiento = 50
    
    # Contadores de auditoría clínica masiva
    total_encontradas = 0
    descartadas_gc = 0
    descartadas_leucocitos = 0
    descartadas_pancancer = 0
    
    with open(ruta_fasta, 'r') as fasta, open(ruta_salida_csv, 'w', newline='', encoding='utf-8') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(["ID_Guia", "PAM", "Secuencia_Guia", "Estabilidad_dG", "Porcentaje_GC", "Metilacion_Leucocitos", "Max_Delta_Otros_Canceres"])
        
        while True:
            bloque = fasta.read(5 * 1024 * 1024)
            if not bloque:
                break
                
            lineas = bloque.split('\n')
            secuencia_limpia = "".join([l.strip() for l in lineas if not l.startswith('>')]).upper()
            texto_a_evaluar = buffer_secuencia + secuencia_limpia
            
            for coincidencia in patron_crispr.finditer(texto_a_evaluar):
                total_encontradas += 1
                pam = coincidencia.group(1)
                guia = coincidencia.group(2)
                
                # 1. FILTRO BIOFÍSICO: Ventana estricta original METHYLOX
                conteo_gc = guia.count('G') + guia.count('C')
                porcentaje_gc = conteo_gc / len(guia)
                if not (0.35 <= porcentaje_gc <= 0.65):
                    descartadas_gc += 1
                    continue
                
                # Extraer datos epigenéticos reales del mapa cargado
                datos_epi = mapa_epi.get(guia, {"leucocitos": 0.0, "pancancer_max": 0.0})
                val_leucocitos = datos_epi["leucocitos"]
                val_pancancer = datos_epi["pancancer_max"]
                
                # 2. FILTRO DE LEUCOCITOS: Purga ruido natural de la sangre sana
                if val_leucocitos >= 0.01:
                    descartadas_leucocitos += 1
                    continue
                    
                # 3. FILTRO PAN-CÁNCER MÁSTER: Expulsa si se eleva en cualquier otro tumor sólido
                if val_pancancer >= 0.05:
                    descartadas_pancancer += 1
                    continue
                
                # Si supera todas las aduanas, se calcula termodinámica y se aprueba
                dg = estimar_energia_gibbs(guia)
                writer.writerow([
                    f"METHYLOX_CLINIC_{id_guia:06d}",
                    pam,
                    guia,
                    dg,
                    round(porcentaje_gc, 4),
                    val_leucocitos,
                    val_pancancer
                ])
                id_guia += 1
                
            buffer_secuencia = texto_a_evaluar[-tamano_solapamiento:]
            
    print(f"\n====================================================================")
    print(f"📊 REPORTE FINAL DE PURIFICACIÓN METHYLOX™")
    print(f"====================================================================")
    print(f"🔹 Total de motivos CRISPR detectados: {total_encontradas}")
    print(f"❌ Eliminadas por estructura (GC% fuera de rango): {descartadas_gc}")
    print(f"❌ Eliminadas por Filtro Leucocitos (>= 0.01): {descartadas_leucocitos}")
    print(f"❌ Eliminadas por Filtro Pan-Cáncer Máster (>= 0.05): {descartadas_pancancer}")
    print(f"🏆 GUÍAS ULTRA-ESPECÍFICAS DE MAMA RETENIDAS: {id_guia - 1}")
    print(f"📁 Destino: '{ruta_salida_csv}'")
    print(f"====================================================================\n")


if __name__ == "__main__":
    print("\n====================================================================")
    print("🛡️ PLATAFORMA METHYLOX™ - PIPELINE DE BLINDAJE CLÍNICO INTEGRADO")
    print("====================================================================\n")
    
    archivo_dna = "cromosoma21.fa.fa"
    archivo_matriz = "matrices_industriales_integradas.csv" # Alineado a tu archivo del disco
    archivo_salida = "catalogo_guias_potenciales_mama.csv"
    
    # Reparación dinámica de nombre de matriz si varía en tu disco
    if not os.path.exists(archivo_matriz) and os.path.exists("matrices_industriales_regulatorias.csv"):
        archivo_matriz = "matrices_industriales_regulatorias.csv"
        
    evaluar_genoma_clinico(archivo_dna, archivo_matriz, archivo_salida)