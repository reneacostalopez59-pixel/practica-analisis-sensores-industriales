# Análisis de Sensores Industriales

## Objetivo
El objetivo de este proyecto es procesar, analizar y exportar métricas a partir de lecturas masivas de sensores industriales para monitorear anomalías de temperatura en diferentes plantas de forma automatizada.

## Descripción de los datos
El dataset (`sensores_industriales.csv`) se ubica en la carpeta `data/` y contiene 100,000 mediciones que registran la temperatura (en grados Celsius) y la vibración (en milímetros por segundo) de múltiples sensores distribuidos en cuatro plantas. 

**Nota importante:** Los datos utilizados en este proyecto son estrictamente simulados para fines didácticos, tal como se solicita en los lineamientos de la evaluación.

## Instalación y Ejecución

Sigue estos pasos detallados para reproducir el proyecto localmente de manera exitosa:

1. **Clonar el repositorio**
   Abre tu terminal y ejecuta:
   ```bash
   git clone [https://github.com/reneacostalopez59-pixel/practica-analisis-sensores-industriales.git](https://github.com/reneacostalopez59-pixel/practica-analisis-sensores-industriales.git)
   cd practica-analisis-sensores-industriales
   ```

2. **Crear y activar el entorno virtual**
   Este proyecto requiere un entorno virtual aislado llamado `.venv`:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   Instala las bibliotecas necesarias a partir del archivo de requerimientos:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el análisis**
   Corre el script principal:
   ```bash
   python analisis.py
   ```

## Resultados esperados
Al ejecutar el script, se imprimirá en la consola un reporte detallado con:
- La cantidad de registros y de sensores distintos.
- La temperatura promedio de cada planta.
- La temperatura máxima registrada, identificando el sensor y la fecha.
- El recuento de lecturas con temperatura mayor a 85 °C (alertas).
- La identificación de la planta con más alertas de temperatura.

Además, el programa creará automáticamente una carpeta llamada `resultados/` y exportará dentro de ella el archivo `alertas.csv`, el cual contendrá exclusivamente las lecturas con alerta, conservando todas las columnas originales.