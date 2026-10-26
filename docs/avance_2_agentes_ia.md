# Avance 2: análisis no supervisado de interacciones de agentes de IA

## Empresa y título

**Empresa de referencia:** CONAUTI S.A.C., planteada en este proyecto académico como desarrolladora de soluciones tecnológicas basadas en agentes de inteligencia artificial.

**Título:** Sistema de análisis de interacciones de agentes de inteligencia artificial mediante modelos no supervisados.

Este avance mantiene la empresa del primer avance, pero define una problemática alineada con el desarrollo de agentes de IA. No utiliza el caso de dígitos manuscritos ni el formato de Blackboard. La problemática es una propuesta académica, no una afirmación sobre procesos internos reales de la empresa.

## 1. Análisis de la problemática

Los agentes de IA pueden recibir solicitudes, utilizar herramientas y realizar varias operaciones antes de responder. Las interacciones varían en duración, número de intentos, herramientas invocadas y consumo de tokens. Cuando hay muchos registros, revisarlos manualmente dificulta reconocer patrones de comportamiento.

Se propone un sistema que agrupe interacciones similares e identifique registros atípicos para revisión técnica. Una interacción atípica no es necesariamente una falla; puede ser una tarea legítimamente compleja.

**Objetivo general:** diseñar un sistema que analice interacciones de agentes mediante K-Means e Isolation Forest para identificar grupos y señalar registros que merezcan revisión.

**Objetivos específicos:**
1. Diseñar la estructura de almacenamiento de agentes e interacciones.
2. Seleccionar y preparar variables numéricas.
3. Aplicar K-Means para agrupar interacciones.
4. Aplicar Isolation Forest para identificar registros atípicos.
5. Interpretar resultados mediante tablas y gráficos.
6. Diseñar un portal para consultar datos y resultados.

## 2. Base de datos

La propuesta relacional incluye estas tablas:

- **agentes:** id_agente, nombre, tipo, fecha_creacion y estado.
- **interacciones:** id_interaccion, id_agente, fecha_hora, longitud_solicitud, tiempo_respuesta_ms, herramientas_utilizadas, numero_intentos, tokens_consumidos y estado_ejecucion.
- **ejecuciones_modelos:** id_ejecucion, fecha_ejecucion, nombre_modelo, version_modelo, parametros y observaciones.
- **resultados_modelo:** id_resultado, id_ejecucion, id_interaccion, grupo_kmeans, puntuacion_atipicidad y candidato_revision.

Un agente puede tener muchas interacciones; cada interacción se relaciona con el agente y puede tener resultados en varias ejecuciones. Los resultados se generan mediante el análisis y no se deben inventar antes de ejecutar los modelos.

## 3. Diseño de la vista

El portal incluye un resumen de registros, una tabla de interacciones, una sección para los grupos de K-Means, otra para candidatos a revisión de Isolation Forest y una vista de informes. Permitirá ejecutar el análisis y descargar los resultados CSV.

## 4. Elección de variables

| Variable | Utilidad |
|---|---|
| longitud_solicitud | Aproxima el tamaño de la entrada |
| tiempo_respuesta_ms | Describe la duración de la respuesta |
| herramientas_utilizadas | Cuenta herramientas invocadas |
| numero_intentos | Registra intentos de ejecución |
| tokens_consumidos | Aproxima el uso de tokens cuando esté disponible |

Los identificadores se conservan para trazabilidad, pero no se usan como variables de entrada. Se revisarán faltantes, duplicados y valores inválidos, y se escalarán las variables numéricas antes de K-Means.

## 5. Modelos no supervisados

### K-Means (obligatorio)

Agrupa interacciones a partir de sus características numéricas. Se evaluarán distintas cantidades de grupos y se analizarán los centroides, el tamaño de los grupos y el coeficiente de silueta. Los nombres interpretativos de los grupos se asignarán después de observar los resultados.

### Isolation Forest

Es el segundo modelo no supervisado. Construye particiones aleatorias para identificar observaciones que resultan más fáciles de aislar que las demás. Se aplicará a las mismas variables preparadas para priorizar registros atípicos para revisión.

El parámetro de contaminación representa la proporción esperada de atípicos que el algoritmo marca; no significa que esa proporción sea realmente defectuosa. Los registros señalados deberán revisarse en su contexto operativo.

## 6. Interpretación de resultados

Se analizará la cantidad de registros por grupo, las medias y medianas de las variables y la separación de los grupos. Para Isolation Forest se revisarán las puntuaciones y los registros seleccionados. Se utilizarán gráficos de dispersión con proyección PCA para visualización; PCA no será un tercer modelo de decisión.

No se reportan cifras de rendimiento como si fueran resultados reales de la empresa. El prototipo puede ejecutarse inicialmente con datos sintéticos y deberá identificarlos como tales.

## 7. Desarrollo del portal

El prototipo se implementa en Python con Flask, pandas y scikit-learn. El usuario podrá ejecutar ambos modelos, elegir el número de grupos y la proporción configurada para detectar atípicos, revisar resultados y descargar el CSV analizado. El procesamiento, los modelos y la interfaz se mantienen en módulos separados para facilitar su mantenimiento.

## Limitaciones

- Los datos sintéticos solo validan el flujo técnico; no demuestran el comportamiento real de los agentes de CONAUTI.
- Los resultados dependen de las variables y de la calidad de los datos.
- Un atípico no es automáticamente una falla.
- El sistema analiza métricas operativas, no la calidad semántica de las respuestas.
- Antes de utilizar registros reales se necesita autorización y una revisión de privacidad.

## Conclusión

K-Means permitirá descubrir grupos de interacciones similares e Isolation Forest ayudará a localizar registros estadísticamente atípicos. La base de datos y el portal propuesto facilitarán la consulta e interpretación de los resultados. La utilidad del sistema deberá comprobarse con datos autorizados y revisión técnica.
