"""Pipeline de aprendizaje no supervisado para interacciones de agentes de IA."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from generar_datos import COLUMNAS_MODELO, generar_interacciones

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "datos"
OUT_DIR = ROOT / "resultados"
MODEL_DIR = ROOT / "modelos"
SEED = 42
COLUMNA_ID = "id_interaccion"


def cargar_datos(ruta_csv: str | Path | None = None) -> tuple[pd.DataFrame, str]:
    """Carga CSV indicado o genera un CSV de demostración claramente sintético."""
    if ruta_csv:
        path = Path(ruta_csv)
        if not path.exists():
            raise FileNotFoundError(f"No existe el archivo de entrada: {path}")
        return pd.read_csv(path), "archivo_proporcionado"

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "interacciones_demo.csv"
    if not path.exists():
        generar_interacciones().to_csv(path, index=False)
    return pd.read_csv(path), "sintetico_demostracion"


def validar_datos(df: pd.DataFrame) -> pd.DataFrame:
    requeridas = set(COLUMNAS_MODELO)
    faltantes = requeridas.difference(df.columns)
    if faltantes:
        raise ValueError("Faltan columnas numéricas requeridas: " + ", ".join(sorted(faltantes)))
    if len(df) < 10:
        raise ValueError("Se requieren al menos 10 interacciones para analizar.")
    resultado = df.copy()
    for col in COLUMNAS_MODELO:
        resultado[col] = pd.to_numeric(resultado[col], errors="coerce")
    if resultado[COLUMNAS_MODELO].isna().all(axis=None):
        raise ValueError("Todas las variables numéricas están vacías o son inválidas.")
    return resultado


def ejecutar_analisis(
    ruta_csv: str | Path | None = None,
    n_clusters: int = 3,
    contamination: float = 0.05,
) -> dict[str, Any]:
    """Ejecuta K-Means e Isolation Forest y guarda resultados reproducibles."""
    if not 2 <= n_clusters <= 10:
        raise ValueError("n_clusters debe estar entre 2 y 10.")
    if not 0.01 <= contamination <= 0.20:
        raise ValueError("contamination debe estar entre 0.01 y 0.20.")

    df, origen = cargar_datos(ruta_csv)
    df = validar_datos(df)
    X = df[COLUMNAS_MODELO]

    preprocesador = Pipeline([
        ("imputador", SimpleImputer(strategy="median")),
        ("escalador", StandardScaler()),
    ])
    X_scaled = preprocesador.fit_transform(X)
    if not np.isfinite(X_scaled).all():
        raise ValueError("El preprocesamiento produjo valores no finitos.")

    kmeans = KMeans(n_clusters=n_clusters, random_state=SEED, n_init=10)
    grupos = kmeans.fit_predict(X_scaled)

    isolation = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=SEED,
        n_jobs=-1,
    )
    pred_atipicos = isolation.fit_predict(X_scaled)
    # En sklearn: -1 indica atípico y 1 indica normal.
    puntuaciones = -isolation.score_samples(X_scaled)

    resultados = df.copy()
    resultados["grupo_kmeans"] = grupos.astype(int)
    resultados["puntuacion_atipicidad"] = puntuaciones
    resultados["candidato_revision"] = pred_atipicos == -1
    resultados["origen_datos"] = df.get(
        "origen_datos", pd.Series([origen] * len(df), index=df.index)
    ).fillna(origen)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    resultados.to_csv(OUT_DIR / "interacciones_analizadas.csv", index=False)

    perfil = resultados.groupby("grupo_kmeans")[COLUMNAS_MODELO].agg(["count", "mean", "median"])
    perfil.columns = [f"{variable}_{estadistica}" for variable, estadistica in perfil.columns]
    perfil.to_csv(OUT_DIR / "perfil_grupos.csv")

    cantidad_por_grupo = resultados["grupo_kmeans"].value_counts().sort_index().to_dict()
    silueta = None
    if len(set(grupos)) > 1 and len(set(grupos)) < len(grupos):
        silueta = float(silhouette_score(X_scaled, grupos))

    resumen = {
        "estado": "completado",
        "origen_datos": str(resultados["origen_datos"].iloc[0]),
        "registros_analizados": int(len(resultados)),
        "variables": COLUMNAS_MODELO,
        "modelo_agrupamiento": "K-Means",
        "cantidad_grupos": int(n_clusters),
        "registros_por_grupo": {str(k): int(v) for k, v in cantidad_por_grupo.items()},
        "silueta": silueta,
        "modelo_atipicos": "Isolation Forest",
        "candidatos_revision": int((pred_atipicos == -1).sum()),
        "proporcion_candidatos_revision": float((pred_atipicos == -1).mean()),
        "semilla": SEED,
        "nota": "Los candidatos a revisión no son fallas confirmadas. Verificar el contexto operativo.",
    }
    with (OUT_DIR / "resumen.json").open("w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)

    joblib.dump({"preprocesador": preprocesador, "modelo": kmeans}, MODEL_DIR / "kmeans_interacciones.joblib")
    joblib.dump({"preprocesador": preprocesador, "modelo": isolation}, MODEL_DIR / "isolation_forest.joblib")

    # PCA se usa solo para visualizar en dos dimensiones, no para asignar grupos.
    if X_scaled.shape[1] >= 2:
        coordenadas = PCA(n_components=2, random_state=SEED).fit_transform(X_scaled)
        fig, ax = plt.subplots(figsize=(9, 6))
        puntos = ax.scatter(coordenadas[:, 0], coordenadas[:, 1], c=grupos, s=18, alpha=0.75)
        ax.set_title("Interacciones agrupadas por K-Means (proyección PCA)")
        ax.set_xlabel("Componente principal 1")
        ax.set_ylabel("Componente principal 2")
        fig.colorbar(puntos, ax=ax, label="Grupo K-Means")
        fig.tight_layout()
        fig.savefig(OUT_DIR / "grupos_kmeans_pca.png", dpi=140)
        plt.close(fig)

    return resumen


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="CSV de interacciones reales/autorizadas con las columnas requeridas.")
    parser.add_argument("--grupos", type=int, default=3, help="Número de grupos para K-Means (2-10).")
    parser.add_argument("--contaminacion", type=float, default=0.05, help="Proporción esperada de atípicos (0.01-0.20).")
    args = parser.parse_args()
    resultado = ejecutar_analisis(args.csv, args.grupos, args.contaminacion)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
