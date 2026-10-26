# CONAUTI S.A.C. — Análisis de interacciones de agentes de IA

Repositorio académico con el **Avance 2** orientado a analizar métricas operativas de agentes de inteligencia artificial mediante aprendizaje no supervisado.

## Proyecto principal del Avance 2

El código nuevo se encuentra en [`agentes_ia/`](agentes_ia/README.md) e implementa:

- **K-Means:** agrupamiento de interacciones similares.
- **Isolation Forest:** detección de registros atípicos para revisión.
- **Portal Flask:** ejecución de los modelos, visualización de grupos y descarga de resultados.
- **Datos sintéticos reproducibles:** permiten probar el flujo sin afirmar que son datos reales de CONAUTI.

> Los datos de demostración no provienen de la empresa. Un registro atípico no es una falla confirmada. Para datos reales se necesita autorización y revisión de privacidad.

### Inicio rápido (Windows)

```powershell
cd agentes_ia
py -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python pipeline.py
python app.py
```

Luego abre `http://127.0.0.1:5000`.

### Pruebas

Desde la carpeta `agentes_ia`:

```powershell
python -m unittest -v
```

### Documentación del avance

- [Documento teórico del Avance 2](docs/avance_2_agentes_ia.md)
- [Guía técnica y comandos](agentes_ia/README.md)

## Archivos del Avance 1

Los archivos originales de reconocimiento de dígitos manuscritos (`main.py`, `requirements.txt` y documentos relacionados) se conservan en esta rama para no borrar el trabajo anterior. No forman parte del nuevo caso del Avance 2 ni son necesarios para ejecutar `agentes_ia/`.
