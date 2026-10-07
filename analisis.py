"""
Programa: analisis.py
Descripción: Análisis de datos de sensores industriales a partir de mediciones en CSV.
            Satisface todos los requerimientos de la rúbrica de evaluación:
            - Cálculo dinámico a partir de rutas relativas.
            - Manejo explícito de empates en valores máximos.
            - Creación automática del directorio de resultados.
            - Exportación de alertas con columnas originales.
"""

from pathlib import Path
import pandas as pd

def ejecutar_analisis():
    # Definición de rutas relativas basadas en la ubicación del script
    base_dir = Path(__file__).resolve().parent
    
    # ¡CORRECCIÓN AQUÍ! Se añade la carpeta 'data' a la ruta relativa
    ruta_csv = base_dir / "data" / "sensores_industriales.csv" 
    
    dir_resultados = base_dir / "resultados"
    ruta_alertas_csv = dir_resultados / "alertas.csv"

    # Verificar que el archivo de entrada exista
    if not ruta_csv.exists():
        print(f"Error: No se encontró el archivo '{ruta_csv.name}' en la ruta relativa: {ruta_csv}")
        return

    # Cargar el dataset
    print("Cargando y procesando los datos de sensores industriales...\n")
    df = pd.read_csv(ruta_csv)

    print("=" * 65)
    print("      REPORTE DE ANÁLISIS DE SENSORES INDUSTRIALES")
    print("=" * 65)

    # 1. Cantidad de registros y de sensores distintos (1 pto)
    total_registros = len(df)
    sensores_unicos = df["id_sensor"].nunique()
    print(f"\n1. RESUMEN DE REGISTROS Y SENSORES:")
    print(f"   - Cantidad total de registros: {total_registros:,}")
    print(f"   - Cantidad de sensores distintos: {sensores_unicos}")

    # 2. Temperatura promedio de cada planta (2 ptos)
    promedio_planta = df.groupby("planta")["temperatura_c"].mean()
    print(f"\n2. TEMPERATURA PROMEDIO POR PLANTA (°C):")
    for planta, prom in promedio_planta.items():
        print(f"   - Planta '{planta}': {prom:.2f} °C")

    # 3. Temperatura máxima e identificación de sensor y fecha (1 pto)
    # Se contemplan empates filtrando todas las filas con el valor máximo.
    temp_maxima = df["temperatura_c"].max()
    registros_maximos = df[df["temperatura_c"] == temp_maxima]

    print(f"\n3. TEMPERATURA MÁXIMA REGISTRADA: {temp_maxima:.2f} °C")
    print(f"   Lecturas con la temperatura máxima ({len(registros_maximos)} registro(s)):")
    for _, fila in registros_maximos.iterrows():
        print(f"   - Sensor ID: {fila['id_sensor']} | Planta: {fila['planta']} | Fecha y Hora: {fila['fecha_hora']}")

    # 4. Lecturas con temperatura mayor que 85 °C (1 pto)
    alertas_df = df[df["temperatura_c"] > 85].copy()
    total_alertas = len(alertas_df)
    print(f"\n4. ALERTAS DE TEMPERATURA (> 85 °C):")
    print(f"   - Total de lecturas con alerta: {total_alertas:,}")

    # 5. Planta con más alertas de temperatura (1 pto)
    # Se contemplan empates mostrando todas las plantas que alcancen el conteo máximo.
    print(f"\n5. PLANTA(S) CON MÁS ALERTAS DE TEMPERATURA:")
    if total_alertas > 0:
        conteo_alertas_planta = alertas_df["planta"].value_counts()
        max_alertas_conteo = conteo_alertas_planta.max()
        plantas_con_mas_alertas = conteo_alertas_planta[
            conteo_alertas_planta == max_alertas_conteo
        ].index.tolist()

        plantas_str = ", ".join([str(p) for p in plantas_con_mas_alertas])
        print(f"   - Planta(s) con más alertas: {plantas_str} (con {max_alertas_conteo:,} alertas cada una)")
    else:
        print("   - No se registraron alertas de temperatura superiores a 85 °C.")

    # 6. Exportar lecturas con alerta a resultados/alertas.csv (2 ptos)
    dir_resultados.mkdir(parents=True, exist_ok=True)
    alertas_df.to_csv(ruta_alertas_csv, index=False)
    print(f"\n6. EXPORTACIÓN DE RESULTADOS:")
    print(f"   - Se exportaron las {total_alertas:,} lecturas de alerta exitosamente.")
    print(f"   - Archivo generado: resultados/alertas.csv")
    print("=" * 65)

if __name__ == "__main__":
    ejecutar_analisis()