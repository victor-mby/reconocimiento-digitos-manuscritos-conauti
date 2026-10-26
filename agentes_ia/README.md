# Análisis de interacciones de agentes de IA

Prototipo académico para analizar métricas operativas de interacciones de agentes de inteligencia artificial. Se implementan dos modelos **no supervisados**:

- **K-Means:** agrupa interacciones similares.
- **Isolation Forest:** identifica registros estadísticamente atípicos para priorizar una revisión.

Los atípicos no se consideran fallas confirmadas. El sistema no evalúa el contenido semántico ni la calidad de las respuestas; trabaja con métricas numéricas de operación.

## Datos y privacidad

Por defecto se genera un conjunto de datos **sintético** reproducible. No representa registros reales de CONAUTI S.A.C. Para datos reales, se debe contar con autorización, eliminar información personal y confirmar que el CSV contenga las variables requeridas.

Columnas numéricas requeridas:
- `longitud_solicitud`
- `tiempo_respuesta_ms`
- `herramientas_utilizadas`
- `numero_intentos`
- `tokens_consumidos`

El CSV puede incluir columnas adicionales como `id_interaccion`, `id_agente`, `fecha_hora` y `estado_ejecucion`. Los identificadores no se usan como variables del modelo.

## Instalación

Usar Python 3.10 o superior en un entorno virtual.

Windows PowerShell:
```powershell
cd agentes_ia
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecutar modelos desde consola

Generar un CSV de demostración:
```powershell
python generar_datos.py
``

Ejecutar K-Means e Isolation Forest con datos sintéticos:
```powershell
python pipeline.py
``

Usar un CSV propio:
```powershell
python pipeline.py --csv ruta\a\interacciones.csv --grupos 3 --contaminacion 0.05
``

## Ejecutar el portal

Desde la carpeta `agentes_ia`:
```powershell
python app.py
``
Abrir `http://127.0.0.1:5000`. En el portal se puede ejecutar el análisis, consultar la distribución de grupos, revisar candidatos a inspección y descargar el CSV analizado.

## Archivos generados

- `datos/interacciones_demo.csv`: datos sintéticos de demostración.
- `resultados/interacciones_analizadas.csv`: registros con grupo y puntuación de atipicidad.
- `resultados/perfil_grupos.csv`: estadísticas descriptivas por grupo.
- `resultados/resumen.json`: resumen del análisis.
- `resultados/grupos_kmeans_pca.png`: gráfico de grupos en dos dimensiones.
- `modelos/kmeans_interacciones.joblib`: preprocesador y K-Means entrenados.
- `modelos/isolation_forest.joblib`: preprocesador y Isolation Forest entrenados.

## Validación

Ejecutar las pruebas desde esta carpeta:
```powershell
python -m unittest -v
``

La primera ejecución crea los datos sintéticos si no existe un CSV. Las métricas y los grupos pueden variar si se cambia el conjunto de entrada o los parámetros. El coeficiente de silueta mide la separación interna de los grupos y no debe interpretarse como una medida de calidad de las respuestas de los agentes.
