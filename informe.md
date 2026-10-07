# Informe de Aplicación al Caso de Big Data

## 5. Las 5 V aplicadas al proyecto

A continuación, se describen las 5 V del Big Data en el contexto del sistema de sensores industriales:

| V del Big Data | Relación con el sistema de sensores | Ejemplo concreto | Estado (Actual o Futura ampliación) |
| :--- | :--- | :--- | :--- |
| **Volumen** | Se refiere a la cantidad de datos generados y almacenados por el sistema a lo largo del tiempo. | Acumular terabytes de información histórica generada al pasar de cientos a miles de sensores. | Futura ampliación (el CSV actual de 100k registros y ~4.4 MiB no representa un alto volumen). |
| **Velocidad** | Es la rapidez con la que se generan, reciben y necesitan ser procesados los datos. | Recibir y procesar mediciones de los sensores **cada segundo** en tiempo real. | Futura ampliación (el CSV actual es estático y fue analizado en diferido). |
| **Variedad** | Representa la diversidad de formatos y fuentes de procedencia de los datos. | Integrar distintos formatos: tablas numéricas de sensores, **fotografías** de las máquinas y texto libre. | Futura ampliación (el CSV actual es estrictamente tabular y estructurado). |
| **Veracidad** | Es la confiabilidad, calidad y limpieza de los datos registrados por los dispositivos. | Asegurar que un sensor no envíe valores nulos, corruptos o con "ruido" debido a una falla de calibración. | Actual / Futura ampliación. |
| **Valor** | Es la utilidad de negocio o el beneficio extraído al analizar la información. | Identificar qué planta tiene más lecturas sobre los **85 °C** para enfocar los recursos de mantenimiento preventivo. | Actual (reflejado en el script `analisis.py`). |

---

## 6. Tipos de datos y procesamiento tradicional

**Clasificación de los elementos:**
*   **El CSV de sensores:** Datos Estructurados (filas y columnas definidas).
*   **Un mensaje JSON enviado por un sensor:** Datos Semiestructurados (tiene etiquetas/claves jerárquicas pero no una estructura de tabla rígida).
*   **Una fotografía de una máquina:** Datos No Estructurados.
*   **El texto libre de un reporte de mantenimiento:** Datos No Estructurados.

**¿Por qué 100,000 registros no convierten automáticamente al archivo en Big Data?**
Tener 100,000 registros no es Big Data porque el tamaño total del archivo es lo suficientemente pequeño (unos pocos Megabytes) para caber en la memoria RAM de cualquier computadora convencional. Puede ser procesado rápidamente con herramientas tradicionales (como la biblioteca estándar de Python o Excel) utilizando un solo nodo (una sola máquina), sin requerir procesamiento distribuido (como Hadoop o Spark) ni clústeres de servidores.

**Limitaciones al aumentar la escala:**
Si el sistema escala a miles de sensores enviando datos cada segundo, aparecerán problemas como:
1.  **Desbordamiento de memoria:** Los datos ya no cabrán en la RAM de una sola computadora.
2.  **Tiempos de procesamiento inaceptables:** Leer y analizar el histórico completo tomará horas o días usando herramientas tradicionales.
3.  **Latencia en alertas críticas:** Un enfoque tradicional por lotes no permitirá detectar una sobrecarga térmica (ej. > 85 °C) en el momento exacto en que ocurre.

---

## 7. Batch y Streaming

*   **Tipo de procesamiento realizado en el programa (`analisis.py`):**
    *   **Identificación y justificación:** Se realizó procesamiento **Batch (por lotes)**. Esto se debe a que el programa lee un conjunto de datos estático, finito y previamente almacenado (`sensores_industriales.csv`) en su totalidad antes de procesarlo y generar el reporte final. No hay ingesta continua de datos durante la ejecución.

*   **Enfoque para emitir una alerta pocos segundos después de una lectura > 85 °C:**
    *   Se requiere un procesamiento en **Streaming (flujo continuo)**. El tiempo de respuesta necesario es casi inmediato (baja latencia). Los datos deben ser evaluados en movimiento, directamente en la memoria a medida que llegan del sensor, antes de ser almacenados a largo plazo.

*   **Enfoque para generar un resumen al terminar el día:**
    *   Se utilizaría un procesamiento **Batch (por lotes)**. Dado que el resultado solo se necesita una vez al día, la latencia no es un problema. El sistema puede recolectar todas las métricas durante la jornada y ejecutar una tarea pesada programada (ej. a medianoche) para consolidar el reporte.

---

## 8. Lambda y Kappa

**Escenario A: Combinar una ruta histórica por lotes con otra rápida para mediciones recientes.**
*   **Arquitectura elegida:** Arquitectura **Lambda**.
*   **Justificación:** Lambda está diseñada exactamente para este propósito. Separa el flujo en dos capas: una "Batch Layer" para procesar todo el histórico de forma robusta pero lenta, y una "Speed Layer" (Streaming) para procesar solo los datos más recientes en tiempo real y llenar el hueco de información hasta que termine el proceso batch.
*   **Diagrama:**
    ```text
                 +---> [ Capa Batch (Histórico) ] ---+
                 |                                   |
    [ Datos ] ---+                                   +---> [ Capa Serving (Consultas) ]
                 |                                   |
                 +---> [ Capa Speed (Streaming) ] ---+
    ```

**Escenario B: Una sola lógica de eventos y conservar mediciones para reprocesar.**
*   **Arquitectura elegida:** Arquitectura **Kappa**.
*   **Justificación:** Kappa elimina la dualidad de Lambda y trata todo (tanto los datos en tiempo real como el reprocesamiento histórico) como un único flujo de streaming. Guarda todos los eventos inmutables en un sistema de mensajería (ej. Kafka); si se necesita reprocesar el histórico, simplemente se vuelve a "reproducir" el flujo de eventos desde el principio bajo la misma lógica.
*   **Diagrama:**
    ```text
    [ Datos ] ---> [ Log Inmutable de Eventos (ej. Kafka) ] ---> [ Capa de Stream Processing ] ---> [ Capa Serving ]
    ```

---

## 9. Analítica descriptiva, predictiva y prescriptiva

A partir del caso de estudio y el análisis del archivo:

*   **Descriptiva (Qué pasó):**
    1. La temperatura máxima registrada en toda la operación fue de **104.99 °C**.
    2. Al analizar los eventos críticos, se detectó que la **Planta_3** fue la instalación que presentó la mayor cantidad de alertas por superar el umbral de los 85 °C.

*   **Predictiva (Qué podría pasar):**
    *   **Pregunta:** ¿Cuál es la probabilidad de que el rotor de la máquina principal en una planta específica falle durante los próximos 7 días?
    *   **Datos adicionales necesarios:** Para investigar esto se necesitarían los registros históricos de fallas previas, el tiempo de vida útil de la pieza, y la correlación entre picos de vibración anómalos y sobrecalentamientos sostenidos (ya que una lectura alta aislada no demuestra falla).

*   **Prescriptiva (Qué acción tomar):**
    *   **Acción propuesta:** Si el modelo predictivo detecta un riesgo inminente de falla (>90% de probabilidad) debido a temperaturas y vibraciones en ascenso, el sistema debe recomendar enviar un comando automático para reducir la velocidad operativa de esa máquina al 50% y agendar a un técnico de mantenimiento para el siguiente turno.
    *   **Información a revisar antes de decidir:** Antes de aprobar la acción, un tomador de decisiones revisaría el impacto económico de detener parcial o totalmente la producción de esa máquina versus el costo logístico de reemplazar la pieza si se rompe catastróficamente, así como la disponibilidad inmediata de refacciones y técnicos en ese horario.