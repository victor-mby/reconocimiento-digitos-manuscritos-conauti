"""Genera datos sintéticos de interacciones para probar el prototipo.

Los datos no provienen de CONAUTI ni de agentes reales. Se usan únicamente
para comprobar el flujo técnico hasta que existan registros autorizados.
"""
from pathlib import Path

import numpy as np
import pandas as pd

COLUMNAS_MODELO = [
    "longitud_solicitud",
    "tiempo_respuesta_ms",
    "herramientas_utilizadas",
    "numero_intentos",
    "tokens_consumidos",
]


def generar_interacciones(cantidad: int = 600, semilla: int = 42) -> pd.DataFrame:
    """Crea un conjunto reproducible sin etiquetas de grupo predefinidas."""
    if cantidad < 30:
        raise ValueError("cantidad debe ser al menos 30 para analizar grupos.")

    rng = np.random.default_rng(semilla)
    # Perfiles de simulación para producir variedad operativa. No se exporta
    # ninguna etiqueta real o esperada: K-Means descubre los grupos por sí mismo.
    perfiles = rng.choice(3, size=cantidad, p=[0.55, 0.30, 0.15])
    longitud = np.empty(cantidad, dtype=int)
    tiempo = np.empty(cantidad, dtype=float)
    herramientas = np.empty(cantidad, dtype=int)
    intentos = np.empty(cantidad, dtype=int)
    tokens = np.empty(cantidad, dtype=int)

    for i, perfil in enumerate(perfiles):
        if perfil == 0:
            longitud[i] = rng.integers(20, 180)
            herramientas[i] = rng.choice([0, 1], p=[0.75, 0.25])
            intentos[i] = rng.choice([1, 2], p=[0.92, 0.08])
            tokens[i] = int(max(20, rng.normal(220 + longitud[i] * 1.4, 45)))
            tiempo[i] = max(80, rng.normal(350 + tokens[i] * 0.65, 90))
        elif perfil == 1:
            longitud[i] = rng.integers(100, 600)
            herramientas[i] = rng.integers(1, 4)
            intentos[i] = rng.choice([1, 2, 3], p=[0.65, 0.28, 0.07])
            tokens[i] = int(max(100, rng.normal(650 + longitud[i] * 2.0, 180)))
            tiempo[i] = max(250, rng.normal(900 + tokens[i] * 0.9 + herramientas[i] * 180, 240))
        else:
            longitud[i] = rng.integers(250, 1200)
            herramientas[i] = rng.integers(2, 7)
            intentos[i] = rng.choice([2, 3, 4, 5], p=[0.25, 0.40, 0.25, 0.10])
            tokens[i] = int(max(250, rng.normal(1600 + longitud[i] * 2.5, 450)))
            tiempo[i] = max(500, rng.normal(1700 + tokens[i] * 1.1 + herramientas[i] * 250, 500))

    # Añade unos pocos casos extremos para probar la detección de atípicos.
    extremos = max(2, cantidad // 100)
    indices = rng.choice(cantidad, size=extremos, replace=False)
    tiempo[indices] *= rng.uniform(3.0, 5.0, size=extremos)
    tokens[indices] *= rng.integers(2, 4, size=extremos)

    fecha = pd.date_range("2026-01-01", periods=cantidad, freq="15min")
    return pd.DataFrame({
        "id_interaccion": np.arange(1, cantidad + 1),
        "id_agente": [f"AG-{n:02d}" for n in rng.integers(1, 6, size=cantidad)],
        "fecha_hora": fecha.astype(str),
        "longitud_solicitud": longitud,
        "tiempo_respuesta_ms": np.round(tiempo, 2),
        "herramientas_utilizadas": herramientas,
        "numero_intentos": intentos,
        "tokens_consumidos": tokens,
        "origen_datos": "sintetico_demostracion",
    })


def guardar_datos(ruta: str | Path, cantidad: int = 600, semilla: int = 42) -> Path:
    destino = Path(ruta)
    destino.parent.mkdir(parents=True, exist_ok=True)
    generar_interacciones(cantidad, semilla).to_csv(destino, index=False)
    return destino


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent
    archivo = guardar_datos(raiz / "datos" / "interacciones_demo.csv")
    print(f"Datos sintéticos guardados en: {archivo}")
    print("Aviso: no son datos reales de CONAUTI ni de agentes en producción.")
