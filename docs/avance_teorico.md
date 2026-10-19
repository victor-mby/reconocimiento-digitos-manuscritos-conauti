# Avance 1: Marco teórico

## 1. Datos de la empresa

- **Empresa:** CONAUTI S.A.C.
- **Actividad indicada para el proyecto:** desarrollo de soluciones tecnológicas con agentes de inteligencia artificial.
- **Caso práctico de referencia:** clasificación de dígitos manuscritos, según el documento de trabajo final del curso.

## 2. Título del proyecto

**Desarrollo y comparación de modelos de Machine Learning para el reconocimiento automático de dígitos manuscritos en CONAUTI S.A.C.**

## 3. Planteamiento del problema

El procesamiento de documentos que contienen números escritos a mano puede requerir tiempo y estar expuesto a errores de digitación. La escritura varía entre personas y las imágenes pueden presentar diferencias de iluminación, tamaño, inclinación, contraste o ruido. Estas condiciones dificultan la clasificación automática de los dígitos.

En el contexto de una empresa dedicada al desarrollo de soluciones de inteligencia artificial, estudiar el reconocimiento de dígitos manuscritos permite evaluar una posible herramienta para automatizar una parte del procesamiento de documentos. Esta propuesta es académica; no presupone que la empresa tenga actualmente este problema ni que ya utilice el sistema.

## 4. Objetivo general

Desarrollar y comparar tres modelos de aprendizaje automático y aprendizaje profundo para clasificar dígitos manuscritos del 0 al 9, evaluando su rendimiento con métricas de clasificación.

## 5. Objetivos específicos

1. Identificar y preparar un conjunto de imágenes etiquetadas de dígitos manuscritos.
2. Aplicar técnicas de preprocesamiento apropiadas para mejorar la consistencia de las imágenes.
3. Entrenar una CNN, un clasificador KNN y un clasificador SVM con una metodología de evaluación comparable.
4. Medir el desempeño de los modelos mediante accuracy, precision, recall, F1-score y matriz de confusión.
5. Comparar los resultados obtenidos y documentar las limitaciones de la solución.

## 6. Modelos seleccionados

### 6.1. Red neuronal convolucional (CNN)

Una CNN es una red neuronal diseñada para procesar datos con estructura espacial, como imágenes. Sus capas convolucionales pueden aprender patrones visuales de los dígitos, por ejemplo, bordes y trazos. Se propone como modelo principal. Su rendimiento real deberá comprobarse mediante entrenamiento y evaluación.

### 6.2. K-Nearest Neighbors (KNN)

KNN clasifica una muestra a partir de las clases de sus vecinos más cercanos en el espacio de características. Se utilizará como alternativa comparativa. El resultado puede depender de la representación de las imágenes, del número de vecinos y de la métrica de distancia.

### 6.3. Support Vector Machine (SVM)

SVM busca una frontera de decisión que separe las clases. Para trabajar con imágenes, estas se representarán mediante características numéricas, por ejemplo, los píxeles normalizados. Se evaluará como otro modelo comparativo.

## 7. Metodología propuesta

1. **Obtención de datos:** seleccionar un conjunto de imágenes de dígitos manuscritos con etiquetas conocidas. Registrar la fuente y las condiciones de uso.
2. **Inspección:** comprobar las dimensiones, las etiquetas, la distribución de clases y la presencia de imágenes dañadas.
3. **Preprocesamiento:** convertir a escala de grises cuando corresponda, ajustar las dimensiones y normalizar los valores de los píxeles. La segmentación de dígitos individuales será necesaria si se parte de formularios completos.
4. **División de datos:** separar entrenamiento, validación y prueba, evitando que imágenes derivadas de una misma fuente filtren información entre conjuntos.
5. **Entrenamiento:** entrenar CNN, KNN y SVM. Ajustar los hiperparámetros usando únicamente los datos de entrenamiento y validación.
6. **Evaluación:** evaluar el conjunto de prueba una sola vez al finalizar el ajuste.
7. **Comparación:** presentar una tabla de métricas, matrices de confusión y ejemplos de predicciones correctas e incorrectas.
8. **Conclusiones:** elegir el modelo según los resultados medidos, el coste computacional y las limitaciones observadas.

## 8. Métricas de evaluación

- **Accuracy (exactitud global):** proporción total de predicciones correctas.
- **Precision (precisión):** proporción de predicciones positivas de una clase que son correctas.
- **Recall (sensibilidad):** proporción de ejemplos reales de una clase que el modelo identifica correctamente.
- **F1-score:** media armónica de precision y recall.
- **Matriz de confusión:** muestra qué clases se reconocen correctamente y cuáles se confunden entre sí.

Como se trata de diez clases (dígitos del 0 al 9), se reportarán las métricas por clase y un promedio macro cuando sea pertinente. No se asignan valores numéricos en este avance porque todavía no se han ejecutado los experimentos.

## 9. Resultado esperado

Se espera obtener una comparación reproducible entre CNN, KNN y SVM que permita identificar cuál ofrece el mejor equilibrio entre calidad de clasificación y coste computacional en el conjunto de datos seleccionado. Este resultado es una expectativa, no una conclusión experimental.

## 10. Alcance y limitaciones

El primer avance es teórico y metodológico. No incluye resultados de entrenamiento, porcentajes de precisión ni una integración en producción. La calidad de la evaluación dependerá del conjunto de datos, del preprocesamiento y de una separación correcta entre entrenamiento, validación y prueba.

El caso práctico de SENATI también menciona regresión y K-Means en su sección de evidencias, aunque el problema principal descrito es la clasificación de dígitos manuscritos. Conviene confirmar con el docente si esos algoritmos adicionales son obligatorios para la entrega, antes de ampliar el alcance.

## 11. Referencia del caso

SENATI. *Trabajo Final del Curso: Mantenimiento de Equipos Periféricos — Caso práctico: Clasificación de Dígitos Manuscritos*. Material proporcionado para el curso.
