"""Portal Flask sencillo para ejecutar y consultar el análisis de interacciones."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from flask import Flask, flash, redirect, render_template_string, request, url_for

from pipeline import OUT_DIR, ejecutar_analisis

app = Flask(__name__)
app.secret_key = "cambiar-esta-clave-en-despliegue-local"
HTML = """
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>CONAUTI | Análisis de agentes IA</title>
<style>
:root{font-family:system-ui,-apple-system,Segoe UI,sans-serif;color:#172033;background:#f4f6fb}
body{margin:0}header{background:#172554;color:white;padding:24px max(20px,calc((100% - 1100px)/2))}
main{max-width:1100px;margin:24px auto;padding:0 18px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}
.card{background:white;border:1px solid #dce2ee;border-radius:12px;padding:18px;box-shadow:0 3px 12px #15213a0b}
.number{font-size:1.7rem;font-weight:700;margin-top:8px}.muted{color:#5b6475;font-size:.92rem}
button{background:#1d4ed8;color:white;border:0;border-radius:8px;padding:11px 16px;font-weight:600;cursor:pointer}
input,select{padding:9px;border:1px solid #cbd5e1;border-radius:7px;max-width:100%}
form{display:flex;gap:12px;align-items:end;flex-wrap:wrap}label{display:grid;gap:6px;font-size:.9rem}
table{width:100%;border-collapse:collapse;font-size:.9rem}th,td{text-align:left;padding:9px;border-bottom:1px solid #e5e7eb}
th{background:#f8fafc}.notice{padding:12px;border-radius:8px;background:#eff6ff;margin:12px 0}
img{max-width:100%;border-radius:8px}a{color:#1d4ed8}
</style></head>
<body>
<header><h1>CONAUTI S.A.C.</h1><div>Análisis de interacciones de agentes de inteligencia artificial</div></header>
<main>
<div class="notice"><strong>Prototipo académico.</strong> Si no se carga un CSV, el sistema usa datos sintéticos de demostración, no datos reales de CONAUTI.</div>
{% with messages = get_flashed_messages() %}{% if messages %}{% for message in messages %}<div class="notice">{{message}}</div>{% endfor %}{% endif %}{% endwith %}
<section class="card"><h2>Ejecutar análisis</h2>
<form method="post" action="{{url_for('analizar')}}" enctype="multipart/form-data">
<label>Archivo CSV opcional<input type="file" name="archivo" accept=".csv"></label>
<label>Número de grupos K-Means<select name="grupos"><option>2</option><option selected>3</option><option>4</option><option>5</option></select></label>
<label>Proporción atípica<select name="contaminacion"><option value="0.01">1%</option><option value="0.03">3%</option><option value="0.05" selected>5%</option><option value="0.10">10%</option></select></label>
<button type="submit">Ejecutar modelos</button></form>
<p class="muted">Columnas numéricas requeridas: longitud_solicitud, tiempo_respuesta_ms, herramientas_utilizadas, numero_intentos y tokens_consumidos.</p></section>
{% if resumen %}
<section class="grid" style="margin-top:16px">
<div class="card"><div class="muted">Registros analizados</div><div class="number">{{resumen.registros_analizados}}</div></div>
<div class="card"><div class="muted">Grupos encontrados</div><div class="number">{{resumen.cantidad_grupos}}</div></div>
<div class="card"><div class="muted">Candidatos a revisión</div><div class="number">{{resumen.candidatos_revision}}</div></div>
<div class="card"><div class="muted">Silueta K-Means</div><div class="number">{{"%.3f"|format(resumen.silueta) if resumen.silueta is not none else "N/D"}}</div></div>
</section>
<section class="card" style="margin-top:16px"><h2>Distribución por grupo</h2><table><thead><tr><th>Grupo</th><th>Interacciones</th></tr></thead><tbody>
{% for grupo,cantidad in resumen.registros_por_grupo.items() %}<tr><td>{{grupo}}</td><td>{{cantidad}}</td></tr>{% endfor %}
</tbody></table></section>
{% if grafico %}<section class="card" style="margin-top:16px"><h2>Visualización de grupos</h2><img src="{{url_for('static_grafico')}}" alt="Dispersión de grupos K-Means"></section>{% endif %}
<section class="card" style="margin-top:16px"><h2>Interacciones candidatas a revisión</h2><p class="muted">Son registros estadísticamente atípicos según Isolation Forest. No son fallas confirmadas.</p>
<table><thead><tr><th>ID</th><th>Tiempo (ms)</th><th>Herramientas</th><th>Intentos</th><th>Tokens</th><th>Grupo</th><th>Puntuación</th></tr></thead><tbody>
{% for row in atipicos %}<tr><td>{{row.id_interaccion}}</td><td>{{row.tiempo_respuesta_ms}}</td><td>{{row.herramientas_utilizadas}}</td><td>{{row.numero_intentos}}</td><td>{{row.tokens_consumidos}}</td><td>{{row.grupo_kmeans}}</td><td>{{"%.4f"|format(row.puntuacion_atipicidad)}}</td></tr>{% endfor %}
</tbody></table><p><a href="{{url_for('descargar')}}">Descargar resultados CSV</a></p></section>
{% endif %}
</main></body></html>
"""


def leer_resultados():
    ruta = OUT_DIR / "resumen.json"
    if not ruta.exists():
        return None, [], False
    resumen = json.loads(ruta.read_text(encoding="utf-8"))
    archivo = OUT_DIR / "interacciones_analizadas.csv"
    df = pd.read_csv(archivo)
    atipicos = df[df["candidato_revision"]].sort_values("puntuacion_atipicidad", ascending=False).head(20)
    return resumen, atipicos.to_dict(orient="records"), (OUT_DIR / "grupos_kmeans_pca.png").exists()


@app.get("/")
def inicio():
    resumen, atipicos, grafico = leer_resultados()
    return render_template_string(HTML, resumen=resumen, atipicos=atipicos, grafico=grafico)


@app.post("/analizar")
def analizar():
    archivo = request.files.get("archivo")
    grupos = int(request.form.get("grupos", 3))
    contaminacion = float(request.form.get("contaminacion", 0.05))
    try:
        if archivo and archivo.filename:
            if not archivo.filename.lower().endswith(".csv"):
                flash("El archivo debe tener extensión .csv.")
                return redirect(url_for("inicio"))
            # Guardar la carga en una ubicación controlada del prototipo.
            entrada = OUT_DIR / "entrada_usuario.csv"
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            archivo.save(entrada)
            ejecutar_analisis(entrada, grupos, contaminacion)
        else:
            ejecutar_analisis(n_clusters=grupos, contamination=contaminacion)
        flash("Análisis completado. Revisa los grupos y los candidatos a revisión.")
    except (ValueError, OSError) as exc:
        flash(f"No se pudo ejecutar el análisis: {exc}")
    return redirect(url_for("inicio"))


@app.get("/grafico")
def static_grafico():
    from flask import send_file
    grafico = OUT_DIR / "grupos_kmeans_pca.png"
    if not grafico.exists():
        return "Todavía no hay un gráfico. Ejecuta el análisis primero.", 404
    return send_file(grafico, mimetype="image/png")


@app.get("/descargar")
def descargar():
    from flask import send_file
    csv = OUT_DIR / "interacciones_analizadas.csv"
    if not csv.exists():
        flash("Primero ejecuta el análisis.")
        return redirect(url_for("inicio"))
    return send_file(csv, as_attachment=True, download_name="interacciones_analizadas.csv")


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
