# Reconocimiento de Dígitos Manuscritos - CONAUTI S.A.C.

Proyecto académico de Machine Learning y Deep Learning basado en el caso práctico de SENATI sobre la clasificación de dígitos manuscritos.

## Objetivo

Desarrollar y comparar modelos capaces de clasificar dígitos manuscritos del 0 al 9, evaluando sus resultados con métricas de clasificación.

## Contexto

El proyecto se contextualiza en CONAUTI S.A.C., empresa indicada para las prácticas del estudiante y dedicada al desarrollo de soluciones con agentes de inteligencia artificial. La solución propuesta estudia el reconocimiento automático de números escritos a mano como posible componente de un sistema de procesamiento inteligente de documentos.

## Modelos propuestos

- **CNN (red neuronal convolucional):** modelo principal para aprender características visuales de las imágenes.
- **KNN (K-Nearest Neighbors):** línea base basada en la similitud entre ejemplos.
- **SVM (Support Vector Machine):** modelo comparativo de clasificación.

La selección definitiva y la comparación se documentarán según los requisitos del curso y los resultados obtenidos experimentalmente.

## Estado actual

**Etapa 1 — Avance teórico.** Se está documentando el problema, el objetivo, los modelos candidatos y la metodología de evaluación. Todavía no se presentan métricas experimentales ni resultados de entrenamiento.

## Estructura prevista

```text
docs/       Documentación del proyecto
datos/      Instrucciones y referencias sobre los datos
notebooks/  Exploración y experimentos
src/        Código fuente
resultados/ Métricas, tablas y visualizaciones
```

## Evaluación prevista

Se considerarán accuracy, precision, recall, F1-score y matriz de confusión. Los valores se añadirán únicamente después de ejecutar y evaluar los modelos.

## Alcance

El alcance inicial es académico y experimental. No se afirma que exista una integración en producción ni que CONAUTI S.A.C. utilice actualmente esta solución.
