"""Pruebas básicas del prototipo de análisis de interacciones."""
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from generar_datos import generar_interacciones
from pipeline import ejecutar_analisis


class PipelineTests(unittest.TestCase):
    def test_generador_es_reproducible(self):
        a = generar_interacciones(80, semilla=7)
        b = generar_interacciones(80, semilla=7)
        pd.testing.assert_frame_equal(a, b)
        self.assertIn("origen_datos", a.columns)

    def test_pipeline_produce_grupos_y_candidatos(self):
        with tempfile.TemporaryDirectory() as temp:
            ruta = Path(temp) / "interacciones.csv"
            generar_interacciones(100, semilla=3).to_csv(ruta, index=False)
            # Redirige las salidas a una carpeta temporal para no tocar archivos del usuario.
            import pipeline
            old_out, old_models = pipeline.OUT_DIR, pipeline.MODEL_DIR
            pipeline.OUT_DIR = Path(temp) / "resultados"
            pipeline.MODEL_DIR = Path(temp) / "modelos"
            try:
                resumen = ejecutar_analisis(ruta, n_clusters=3, contamination=0.05)
                self.assertEqual(resumen["estado"], "completado")
                self.assertEqual(resumen["registros_analizados"], 100)
                self.assertEqual(resumen["cantidad_grupos"], 3)
                self.assertGreaterEqual(resumen["candidatos_revision"], 1)
                self.assertTrue((pipeline.OUT_DIR / "interacciones_analizadas.csv").exists())
                self.assertTrue((pipeline.OUT_DIR / "perfil_grupos.csv").exists())
            finally:
                pipeline.OUT_DIR, pipeline.MODEL_DIR = old_out, old_models

    def test_rechaza_columnas_faltantes(self):
        with tempfile.TemporaryDirectory() as temp:
            ruta = Path(temp) / "mal.csv"
            pd.DataFrame({"tiempo_respuesta_ms": [1] * 20}).to_csv(ruta, index=False)
            with self.assertRaises(ValueError):
                ejecutar_analisis(ruta)


if __name__ == "__main__":
    unittest.main()
