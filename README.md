# Reconocimiento de Dígitos Manuscritos - CONAUTI S.A.C.

Proyecto académico de Machine Learning y Deep Learning para clasificar dígitos manuscritos del 0 al 9 y comparar CNN, KNN y SVM.

## Estado
La documentación inicial era teórica. Se incorpora ahora un primer prototipo ejecutable en `main.py`. Debe ejecutarse localmente para generar métricas; este repositorio no afirma resultados antes de correr el experimento.

## Requisitos
- Python 3.10–3.12 recomendado para compatibilidad de TensorFlow.
- Conexión a internet en la primera ejecución para descargar MNIST.
- RAM recomendada: 8 GB o más; el entrenamiento puede tardar según el equipo.

## Instalación (Windows)
```powershell
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```
Si Python 3.11 no está instalado, instala una versión compatible con TensorFlow antes de continuar. No se recomienda usar una versión de Python no soportada por TensorFlow.

## Qué hace el programa
1. Descarga MNIST con Keras: imágenes en escala de grises de 28×28 píxeles y etiquetas 0–9.
2. Convierte los píxeles a valores entre 0 y 1.
3. Entrena una CNN con el conjunto de entrenamiento y evalúa con el conjunto de prueba completo.
4. Entrena KNN y SVM con un subconjunto reproducible para controlar el coste computacional.
5. Guarda métricas, reportes por clase, matrices de confusión y modelos.

## Archivos generados
- `resultados/comparacion_modelos.csv`
- `resultados/metricas_*.csv`
- `resultados/reporte_*.txt`
- `resultados/matriz_confusion_*.png`
- `modelos/cnn_mnist.keras`
- `modelos/knn_mnist.joblib`
- `modelos/svm_mnist.joblib`

Los resultados solo existirán después de ejecutar el programa. La comparación debe interpretarse teniendo en cuenta que CNN se evalúa con todo el test de MNIST y KNN/SVM con un subconjunto de test.

## Modelos
- CNN: red neuronal convolucional para aprender características visuales.
- KNN: clasifica según vecinos más cercanos.
- SVM: clasificador con kernel RBF y escalado de características.

## Estructura
```
main.py
requirements.txt
docs/
datos/
resultados/
modelos/       # se crea al ejecutar
```

## Limitaciones
- El prototipo usa MNIST estándar, no datos privados de CONAUTI.
- No es una integración de producción ni un sistema OCR para formularios completos.
- Los hiperparámetros son una configuración inicial y pueden requerir ajuste.
- La CNN entrena tres épocas por defecto; esto no garantiza rendimiento óptimo.
- KNN/SVM usan subconjuntos por coste computacional; para una comparación rigurosa se recomienda evaluar todos los modelos sobre el mismo test, tras ajustar tiempos y recursos.
- El caso de SENATI menciona también regresión y K-Means en la sección de evidencias; confirma con el docente si esos algoritmos son obligatorios.

## Documentación
- [Avance teórico](docs/avance_teorico.md)
- [Preguntas guía](docs/preguntas_guia.md)
- [Diagrama de solución](docs/diagrama_solucion.md)
