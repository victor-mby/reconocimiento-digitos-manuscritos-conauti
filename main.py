"""
Proyecto académico: reconocimiento de dígitos manuscritos (0-9).
Ejecuta CNN, KNN y SVM sobre MNIST y guarda métricas y matrices de confusión.
La primera ejecución necesita internet para descargar MNIST mediante Keras.
"""
from pathlib import Path
import json
import time
import warnings

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "resultados"
MODELS = ROOT / "modelos"
OUT.mkdir(exist_ok=True)
MODELS.mkdir(exist_ok=True)

def cargar_datos():
    """Carga MNIST, normaliza píxeles a [0,1] y prepara datos para cada modelo."""
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    # CNN necesita canal explícito: (alto, ancho, canales).
    x_train_cnn = x_train[..., np.newaxis]
    x_test_cnn = x_test[..., np.newaxis]
    # KNN/SVM usan vectores de 784 características por imagen.
    x_train_flat = x_train.reshape(len(x_train), -1)
    x_test_flat = x_test.reshape(len(x_test), -1)
    return (x_train_cnn, x_train_flat, y_train), (x_test_cnn, x_test_flat, y_test)

def guardar_evaluacion(nombre, y_real, y_pred, segundos, notas=""):
    """Guarda métricas, reporte por clase y matriz de confusión."""
    accuracy = accuracy_score(y_real, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(
        y_real, y_pred, average="macro", zero_division=0
    )
    fila = {
        "modelo": nombre, "accuracy": accuracy, "precision_macro": p,
        "recall_macro": r, "f1_macro": f1,
        "tiempo_entrenamiento_segundos": segundos, "notas": notas
    }
    pd.DataFrame([fila]).to_csv(OUT / f"metricas_{nombre.lower()}.csv", index=False)
    with open(OUT / f"reporte_{nombre.lower()}.txt", "w", encoding="utf-8") as f:
        f.write(classification_report(y_real, y_pred, digits=4, zero_division=0))
    cm = confusion_matrix(y_real, y_pred, labels=list(range(10)))
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(cm, cmap="Blues")
    ax.set(title=f"Matriz de confusión — {nombre}", xlabel="Predicción", ylabel="Etiqueta real")
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    for i in range(10):
        for j in range(10):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(OUT / f"matriz_confusion_{nombre.lower()}.png", dpi=150)
    plt.close(fig)
    return fila

def construir_cnn():
    """Define una CNN compacta para imágenes MNIST de 28x28 píxeles."""
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(28, 28, 1)),
        tf.keras.layers.Conv2D(32, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(64, 3, activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model

def ejecutar():
    np.random.seed(SEED)
    tf.random.set_seed(SEED)
    (x_train_cnn, x_train_flat, y_train), (x_test_cnn, x_test_flat, y_test) = cargar_datos()
    filas = []

    print("\n[1/3] Entrenando CNN...")
    cnn = construir_cnn()
    inicio = time.perf_counter()
    cnn.fit(x_train_cnn, y_train, validation_split=0.1, epochs=3, batch_size=128, verbose=2)
    t = time.perf_counter() - inicio
    pred_cnn = np.argmax(cnn.predict(x_test_cnn, verbose=0), axis=1)
    cnn.save(MODELS / "cnn_mnist.keras")
    filas.append(guardar_evaluacion("CNN", y_test, pred_cnn, t, "MNIST completo; 3 épocas"))
    
    # Los modelos clásicos pueden ser costosos; por defecto se limita el entrenamiento.
    n_train = min(12000, len(x_train_flat))
    n_test = min(2000, len(x_test_flat))
    rng = np.random.default_rng(SEED)
    idx_train = rng.choice(len(x_train_flat), size=n_train, replace=False)
    idx_test = rng.choice(len(x_test_flat), size=n_test, replace=False)
    xtr, ytr = x_train_flat[idx_train], y_train[idx_train]
    xte, yte = x_test_flat[idx_test], y_test[idx_test]

    print("\n[2/3] Entrenando KNN con subconjunto reproducible...")
    knn = KNeighborsClassifier(n_neighbors=3, weights="distance", n_jobs=-1)
    inicio = time.perf_counter()
    knn.fit(xtr, ytr)
    t = time.perf_counter() - inicio
    pred = knn.predict(xte)
    import joblib
    joblib.dump(knn, MODELS / "knn_mnist.joblib")
    filas.append(guardar_evaluacion("KNN", yte, pred, t, f"Entrenamiento={n_train}; prueba={n_test}; subconjunto aleatorio seed={SEED}"))

    print("\n[3/3] Entrenando SVM con subconjunto reproducible...")
    svm = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=5, gamma="scale"))
    inicio = time.perf_counter()
    svm.fit(xtr, ytr)
    t = time.perf_counter() - inicio
    pred = svm.predict(xte)
    joblib.dump(svm, MODELS / "svm_mnist.joblib")
    filas.append(guardar_evaluacion("SVM", yte, pred, t, f"Entrenamiento={n_train}; prueba={n_test}; subconjunto aleatorio seed={SEED}"))

    resumen = pd.DataFrame(filas).sort_values("f1_macro", ascending=False)
    resumen.to_csv(OUT / "comparacion_modelos.csv", index=False)
    with open(OUT / "resumen.json", "w", encoding="utf-8") as f:
        json.dump(filas, f, ensure_ascii=False, indent=2)
    print("\nComparación final (ordenada por F1 macro):")
    print(resumen.to_string(index=False))
    print(f"\nResultados guardados en: {OUT}")
    print(f"Modelos guardados en: {MODELS}")
    print("Nota: CNN usa el conjunto de prueba completo de MNIST; KNN y SVM usan un subconjunto de prueba, así que sus métricas no son directamente idénticas en tamaño.")

if __name__ == "__main__":
    ejecutar()
