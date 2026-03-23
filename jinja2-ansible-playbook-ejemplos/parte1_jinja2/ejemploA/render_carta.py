"""
Ejemplo A — Carta de bienvenida personalizada con Jinja2
=========================================================
Renderiza la plantilla carta.j2 con los datos de un alumno.

Requisitos:
    pip install jinja2

Uso:
    python render_carta.py
"""

from jinja2 import Environment, FileSystemLoader

# ── Datos del alumno (podrían venir de una base de datos o un JSON) ──
alumno = {
    "nombre":       "ana",
    "curso":        "Introducción a Python",
    "id_matricula": "MAT-2025-0042",
    "nota_acceso":  7.5,
}

# ── Cargar la plantilla desde el directorio actual ──
env  = Environment(loader=FileSystemLoader("."))
tmpl = env.get_template("carta.j2")

# ── Renderizar: Jinja2 sustituye {{ }} y evalúa {% %} ──
resultado = tmpl.render(**alumno)

print(resultado)

# ── Opcional: guardar el resultado en un fichero ──
with open("carta_generada.txt", "w", encoding="utf-8") as f:
    f.write(resultado)

print("\n[OK] Carta guardada en carta_generada.txt")
