# Respuestas a las preguntas guía

**Proyecto:** Desarrollo y comparación de modelos de Machine Learning para el reconocimiento automático de dígitos manuscritos en CONAUTI S.A.C.

Estas respuestas se basan en las cinco preguntas guía del caso práctico de SENATI sobre clasificación de dígitos manuscritos.

## Pregunta 1. ¿Cuáles son los principales desafíos que enfrenta un sistema de clasificación de dígitos manuscritos en términos de variabilidad en la escritura y calidad de las imágenes?

Los principales desafíos son las diferencias en la forma, el tamaño, la inclinación y el grosor de los trazos que utiliza cada persona. Además, las imágenes pueden tener poca iluminación, bajo contraste, ruido, desenfoque o una resolución insuficiente. También pueden existir dígitos muy parecidos entre sí, lo que aumenta la posibilidad de confusión. Por ello, es importante preparar adecuadamente las imágenes y entrenar los modelos con ejemplos variados.

## Pregunta 2. ¿Cómo afecta la elección del algoritmo de aprendizaje supervisado (por ejemplo, red neuronal vs. KNN) en la precisión del sistema de reconocimiento de dígitos manuscritos?

La elección del algoritmo influye en cómo el sistema aprende y clasifica las imágenes. Una red neuronal convolucional (CNN) puede aprender características visuales de los trazos y resulta apropiada para trabajar directamente con imágenes. K-Nearest Neighbors (KNN) clasifica según la similitud con ejemplos conocidos y puede ser una referencia sencilla, aunque su coste de predicción puede aumentar con muchos datos. Support Vector Machine (SVM) puede ofrecer buenos resultados con características adecuadas, pero su rendimiento depende de la representación de los datos y de sus parámetros. No se puede afirmar cuál será más preciso sin entrenarlos y evaluarlos con el mismo conjunto de prueba.

## Pregunta 3. ¿Qué técnicas de preprocesamiento de imágenes son más efectivas para mejorar la calidad de las imágenes manuscritas antes de ser alimentadas al modelo?

Las técnicas útiles incluyen convertir las imágenes a escala de grises, ajustar su tamaño a unas dimensiones uniformes, normalizar los valores de los píxeles y reducir el ruido cuando sea necesario. También se puede mejorar el contraste y centrar el dígito. Si la entrada son formularios completos, primero se necesita detectar y segmentar cada dígito para obtener imágenes individuales. Las técnicas exactas deben elegirse según las características del conjunto de datos.

## Pregunta 4. ¿Cuáles son las principales métricas que se deben considerar para evaluar la efectividad del sistema de clasificación de dígitos manuscritos, y cómo se pueden interpretar los resultados obtenidos?

Se deben considerar las siguientes métricas:

- **Accuracy (exactitud global):** porcentaje de predicciones correctas respecto del total evaluado.
- **Precision (precisión):** de las predicciones asignadas a una clase, qué proporción era correcta.
- **Recall (sensibilidad):** de los ejemplos que realmente pertenecen a una clase, qué proporción identificó correctamente el modelo.
- **F1-score:** combina precision y recall en una sola medida.
- **Matriz de confusión:** permite ver qué dígitos se clasifican correctamente y cuáles se confunden entre sí.

Como existen diez clases (del 0 al 9), conviene revisar las métricas por clase y el promedio macro, además de la exactitud global. Las métricas deben calcularse sobre datos de prueba que no se hayan utilizado para entrenar ni ajustar el modelo.

## Pregunta 5. ¿Cómo se puede mejorar el modelo en caso de que no logre una precisión aceptable con los datos proporcionados?

Primero se deben revisar las etiquetas y la calidad de las imágenes para detectar errores o datos insuficientes. Después, se puede mejorar el preprocesamiento, añadir ejemplos representativos, aplicar aumentación de datos únicamente al conjunto de entrenamiento y ajustar los hiperparámetros. También se pueden comparar distintas arquitecturas o configuraciones y comprobar si hay sobreajuste. Finalmente, se debe volver a evaluar el modelo con un conjunto de prueba independiente para comprobar que la mejora sea real.

## Nota

Estas respuestas describen criterios técnicos generales para el caso planteado. La superioridad de un modelo y la precisión alcanzada solo podrán establecerse después de ejecutar los experimentos.
