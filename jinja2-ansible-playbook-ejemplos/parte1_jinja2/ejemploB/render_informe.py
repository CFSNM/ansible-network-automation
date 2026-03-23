"""
Ejemplo B — Informe de notas con bucle {% for %} en Jinja2
===========================================================
Itera sobre una lista de alumnos y genera un informe de notas
usando loop.index y condicionales dentro del bucle.

Requisitos:
    pip install jinja2

Uso:
    python render_informe.py
"""

from jinja2 import Environment, FileSystemLoader

# ── Datos de la clase ────────────────────────────────────────────────
datos = {
    "asignatura": "matemáticas",
    "fecha": "10/06/2025",
    "alumnos": [
        {"nombre": "Laura García",   "nota": 9.5},
        {"nombre": "Carlos Ruiz",    "nota": 6.0},
        {"nombre": "Marta López",    "nota": 4.5},
        {"nombre": "Pedro Sánchez",  "nota": 7.8},
    ],
}

# ── Renderizar ───────────────────────────────────────────────────────
env  = Environment(loader=FileSystemLoader("."))
tmpl = env.get_template("informe_notas.j2")
resultado = tmpl.render(**datos)

print(resultado)

# ── Guardar en fichero ───────────────────────────────────────────────
with open("informe_generado.txt", "w", encoding="utf-8") as f:
    f.write(resultado)

print("\n[OK] Informe guardado en informe_generado.txt")
