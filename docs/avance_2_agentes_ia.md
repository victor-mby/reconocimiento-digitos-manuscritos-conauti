# Avance 2: análisis de interacciones de agentes de inteligencia artificial

**Empresa de referencia:** CONAUTI S.A.C.  
**Título del proyecto:** Sistema de análisis de interacciones de agentes de inteligencia artificial mediante modelos no supervisados.  
**Curso:** Machine Learning y Deep Learning  
**Alcance:** prototipo académico implementado en Python.

## 1. Descripción del proyecto

El proyecto propone analizar métricas operativas de las interacciones realizadas por agentes de inteligencia artificial. Estas interacciones pueden diferir en la extensión de la solicitud, el tiempo de respuesta, la cantidad de herramientas utilizadas, el número de intentos y el consumo de tokens.

Cuando el volumen de registros aumenta, la revisión manual dificulta la identificación de patrones y de comportamientos poco habituales. Para apoyar el análisis, se implementan dos modelos no supervisados: **K-Means**, que agrupa interacciones similares, e **Isolation Forest**, que señala registros estadísticamente atípicos para su revisión.

La problemática se plantea con fines académicos. No constituye una afirmación sobre incidentes, datos ni procedimientos internos reales de CONAUTI S.A.C.

### 1.1 Objetivo general

Desarrollar un prototipo que procese métricas de interacciones de agentes de IA, agrupe registros según sus características e identifique observaciones atípicas mediante modelos de aprendizaje no supervisado.

### 1.2 Objetivos específicos

1. Generar y preparar un conjunto de datos reproducible.
2. Seleccionar variables numéricas relacionadas con el comportamiento operativo de las interacciones.
3. Implementar K-Means e Isolation Forest mediante scikit-learn.
4. Obtener resultados tabulares y métricas útiles para interpretar los grupos.
5. Representar visualmente los grupos y facilitar la revisión de registros atípicos.
6. Desarrollar un portal web para ejecutar el análisis y descargar los resultados.

### 1.3 Alcance del prototipo

El prototipo trabaja con datos sintéticos generados para probar el flujo de procesamiento. Permite cargar un archivo CSV, preparar variables, ejecutar los modelos y consultar los resultados desde una interfaz web. No se conecta a agentes reales ni a sistemas internos de CONAUTI, y no determina por sí solo que una interacción sea defectuosa.

## 2. Organización del repositorio

La implementación del avance se encuentra en la carpeta `agentes_ia/`; la documentación se almacena en `docs/`.

| Archivo | Responsabilidad |
|---|---|
| `agentes_ia/generar_datos.py` | Genera datos sintéticos reproducibles para probar el flujo. |
| `agentes_ia/pipeline.py` | Prepara los datos, ejecuta K-Means e Isolation Forest, calcula resúmenes y guarda resultados. |
| `agentes_ia/app.py` | Implementa el portal web con Flask para ejecutar análisis y consultar resultados. |
| `agentes_ia/test_pipeline.py` | Contiene pruebas automatizadas para aspectos básicos del procesamiento. |
| `agentes_ia/requirements.txt` | Declara las dependencias necesarias para instalar el prototipo. |
| `agentes_ia/README.md` | Describe la configuración, ejecución y uso del módulo. |
| `docs/avance_2_agentes_ia.md` | Presenta la documentación técnica del avance. |

El Avance 2 está en la rama `avance-2-agentes-ia`. Los archivos del Avance 1 se conservan en el repositorio; esta implementación no reemplaza el proyecto anterior en la rama principal.

## 3. Flujo de procesamiento

1. **Entrada de datos:** se utiliza un CSV proporcionado por el usuario o se genera un conjunto sintético de prueba.
2. **Validación:** se comprueba la presencia de las variables requeridas y se identifican datos que deben prepararse antes del análisis.
3. **Preparación:** las variables numéricas se organizan, se tratan valores faltantes mediante imputación por mediana y se escalan para reducir el efecto de las diferencias de magnitud.
4. **Agrupamiento:** K-Means asigna a cada interacción un grupo según la similitud de sus características.
5. **Detección de atípicos:** Isolation Forest asigna una clasificación y puntuación de anomalía a cada registro.
6. **Interpretación:** se calculan resúmenes por grupo y métricas de separación cuando las condiciones de los datos lo permiten.
7. **Visualización y exportación:** se generan resultados tabulares y una proyección PCA destinada a visualizar los grupos.
8. **Consulta:** el portal presenta los resultados y permite descargar el CSV analizado.

PCA se utiliza como técnica de visualización en dos dimensiones; no constituye un tercer modelo de decisión del sistema.

## 4. Base de datos y estructura de los registros

La propuesta de almacenamiento contempla las siguientes entidades:

| Entidad | Campos principales | Propósito |
|---|---|---|
| `agentes` | id_agente, nombre, tipo, fecha_creacion, estado | Identificar los agentes registrados. |
| `interacciones` | id_interaccion, id_agente, fecha_hora y métricas operativas | Almacenar las observaciones analizadas. |
| `ejecuciones_modelos` | id_ejecucion, fecha_ejecucion, nombre_modelo, version_modelo, parametros | Registrar cada ejecución de análisis. |
| `resultados_modelo` | id_resultado, id_ejecucion, id_interaccion, grupo_kmeans, puntuacion_atipicidad, candidato_revision | Relacionar los resultados calculados con cada interacción. |

Esta estructura es el diseño lógico propuesto para una posible persistencia relacional. El prototipo actual procesa datos mediante archivos CSV y no debe describirse como si ya implementara todas estas tablas en una base de datos operativa.

## 5. Selección de variables

Las variables de entrada representan características numéricas de cada interacción.

| Variable | Descripción | Uso analítico |
|---|---|---|
| `longitud_solicitud` | Tamaño de la solicitud de entrada | Distinguir interacciones según la extensión de la entrada. |
| `tiempo_respuesta_ms` | Tiempo de respuesta en milisegundos | Comparar la duración de procesamiento. |
| `herramientas_utilizadas` | Cantidad de herramientas invocadas | Describir el nivel de uso de herramientas. |
| `numero_intentos` | Cantidad de intentos registrados | Identificar diferencias en la ejecución. |
| `tokens_consumidos` | Tokens consumidos por la interacción | Aproximar el uso de recursos del modelo. |

Los identificadores sirven para rastrear los registros, pero no son variables predictoras. Antes del análisis deben revisarse los valores faltantes, duplicados, rangos imposibles y diferencias de escala. La interpretación de cada variable depende de que el CSV de entrada mantenga las unidades y el significado esperados.

## 6. Modelos implementados

### 6.1 K-Means

K-Means es un algoritmo de aprendizaje no supervisado que divide las observaciones en un número definido de grupos. Cada registro se asigna al grupo cuyo centroide resulta más cercano según la distancia utilizada por el algoritmo.

En este proyecto se aplica sobre las variables numéricas preparadas. El parámetro `n_clusters` determina cuántos grupos se forman y se puede configurar desde el flujo de ejecución. Los grupos se interpretan posteriormente mediante sus tamaños y los valores característicos de sus variables; no se les asigna un significado empresarial antes de examinar los datos.

Para valorar la separación se calcula el coeficiente de silueta cuando el número y la distribución de grupos permiten hacerlo. Este indicador complementa la interpretación, pero no demuestra por sí solo que los grupos sean útiles para el negocio.

### 6.2 Isolation Forest

Isolation Forest es un algoritmo no supervisado de detección de anomalías. Construye particiones aleatorias y considera potencialmente atípicas aquellas observaciones que pueden aislarse con mayor facilidad que la mayoría de los registros.

El modelo utiliza las variables numéricas preparadas para señalar interacciones que se apartan del patrón general. El parámetro `contamination` define la proporción esperada de observaciones atípicas que se utiliza para establecer el umbral; no representa una tasa real de fallas confirmadas.

Los registros marcados se consideran **candidatos a revisión técnica**. Una tarea compleja, una solicitud extensa o un tiempo de respuesta elevado pueden ser legítimos y deben interpretarse en su contexto.

### 6.3 Preparación y reproducibilidad

El pipeline centraliza la preparación de variables y la ejecución de ambos algoritmos. El uso de una semilla controlada en la generación de datos facilita repetir las pruebas. Sin embargo, la reproducibilidad completa también depende de las versiones instaladas, los parámetros y los datos utilizados.

## 7. Interpretación de resultados

La interpretación contempla los siguientes elementos:

- **Distribución de grupos:** cantidad de interacciones asignadas a cada grupo.
- **Perfil de los grupos:** medias y medianas de las variables para reconocer diferencias entre conjuntos.
- **Coeficiente de silueta:** indicador complementario de separación y cohesión de los grupos, cuando se puede calcular.
- **Puntuación de anomalía:** valor utilizado por Isolation Forest para ordenar o clasificar observaciones atípicas según el modelo.
- **Proyección PCA:** representación en dos dimensiones para facilitar la inspección visual de la distribución.

Los gráficos y las puntuaciones no sustituyen la revisión de los registros originales. Tampoco se deben presentar resultados de datos sintéticos como evidencia del comportamiento de agentes reales de CONAUTI.

## 8. Portal web

El archivo `app.py` contiene la interfaz desarrollada con Flask. El portal permite iniciar el análisis, proporcionar datos en formato CSV, configurar la cantidad de grupos y el parámetro de contaminación, y consultar o descargar los resultados disponibles.

La interfaz sirve como punto de acceso al pipeline; la preparación de datos y la lógica de los modelos se mantienen separadas de la presentación. Esta organización facilita el mantenimiento y permite ampliar el sistema en una etapa posterior.

## 9. Instalación y ejecución en Windows

Desde una terminal ubicada en la carpeta `agentes_ia`, ejecutar:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python pipeline.py
python app.py
```

Después de iniciar Flask, abrir en el navegador:

```text
http://127.0.0.1:5000
```

Para ejecutar las pruebas automatizadas desde esa misma carpeta:

```powershell
python -m unittest -v
```

La ejecución debe verificarse en el equipo donde se instalen las dependencias. La existencia del código y de las pruebas no demuestra, por sí sola, que la aplicación se haya ejecutado correctamente ni que todas las pruebas hayan pasado.

## 10. Dependencias principales

| Biblioteca | Función |
|---|---|
| Python | Lenguaje de implementación. |
| pandas | Lectura, transformación y organización de datos tabulares. |
| scikit-learn | Imputación, escalado, K-Means, Isolation Forest, PCA y métricas relacionadas. |
| Flask | Servidor y portal web. |
| matplotlib | Generación de gráficos de análisis. |
| joblib | Persistencia de objetos de modelo cuando se utiliza en el pipeline. |

Las versiones instalables concretas están definidas en `requirements.txt`. Para reproducir el entorno conviene registrar la versión de Python y las versiones efectivamente instaladas.

## 11. Pruebas y limitaciones

Las pruebas incluidas contemplan la reproducibilidad de los datos, el funcionamiento básico del pipeline y el manejo de columnas requeridas. Deben ejecutarse y revisarse sus resultados antes de declarar la implementación validada.

| Aspecto | Estado o consideración |
|---|---|
| Datos | El prototipo admite datos sintéticos; estos no equivalen a registros reales de CONAUTI. |
| Validación de ejecución | Debe confirmarse ejecutando el pipeline, el portal y las pruebas en un entorno configurado. |
| Interpretación | Los grupos requieren análisis; sus etiquetas no tienen significado empresarial automático. |
| Anomalías | Un registro atípico no equivale necesariamente a un error, incidente o falla. |
| Calidad de datos | Las variables deben conservar sus unidades y definiciones para que los resultados sean interpretables. |
| Integración real | No se incluye conexión con agentes de producción ni con sistemas internos de la empresa. |
| Base de datos | Se documenta un diseño relacional propuesto; el prototipo actual se centra en el procesamiento de archivos CSV. |
| Privacidad | La utilización de datos reales requiere autorización, control de acceso y revisión de la información sensible. |

## 12. Conclusión

El Avance 2 desarrolla un prototipo de análisis de interacciones de agentes de inteligencia artificial mediante K-Means e Isolation Forest. El primero permite explorar grupos de comportamiento y el segundo ayuda a priorizar registros atípicos para su revisión. El pipeline, la generación de datos, las pruebas y el portal web organizan la solución en componentes diferenciados.

La siguiente etapa consiste en ejecutar y verificar el prototipo, documentar las salidas obtenidas y, si se cuenta con autorización, evaluar su utilidad con datos representativos. Hasta completar esas comprobaciones, las conclusiones deben limitarse al diseño y a las capacidades previstas del sistema.
