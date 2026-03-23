# Ejemplos Jinja2 & Ansible Playbooks
### Guía de instalación y ejecución paso a paso

---

## Estructura del proyecto

```
proyecto/
├── README.md                        ← Este fichero
│
├── parte1_jinja2/
│   ├── ejemploA/
│   │   ├── carta.j2                 ← Plantilla de carta de bienvenida
│   │   └── render_carta.py          ← Script Python para renderizarla
│   │
│   └── ejemploB/
│       ├── informe_notas.j2         ← Plantilla de informe de notas
│       └── render_informe.py        ← Script Python para renderizarla
│
└── parte2_ansible/
    ├── inventario.yml               ← Inventario de Ansible (localhost)
    ├── playbook_alumnos.yml         ← El playbook principal
    └── templates/
        └── bienvenida.j2            ← Plantilla Jinja2 usada por Ansible
```

---

## PARTE 1 — Ejemplos de Jinja2 puro (Python)

### Requisito previo: instalar Jinja2

Abre una terminal y ejecuta:

```bash
pip install jinja2
```

> Si tienes Python 3 y pip no funciona, prueba con `pip3 install jinja2`

---

### Ejemplo A — Carta de bienvenida

**¿Qué hace?**
Genera una carta personalizada para un alumno usando variables `{{ }}`,
el filtro `| capitalize` y un condicional `{% if %}`.

**Pasos:**

```bash
# 1. Entra en la carpeta del ejemplo
cd parte1_jinja2/ejemploA

# 2. Ejecuta el script
python render_carta.py

# 3. Verás la carta en pantalla y se guardará en carta_generada.txt
cat carta_generada.txt
```

**Prueba a modificarlo:**
Abre `render_carta.py` y cambia el valor de `nota_acceso` a `3.0` o `9.5`
para ver cómo cambia el mensaje del condicional `{% if %}`.

---

### Ejemplo B — Informe de notas

**¿Qué hace?**
Genera un informe con las notas de varios alumnos usando un bucle `{% for %}`,
`loop.index` para numerar y condicionales para clasificar cada nota.

**Pasos:**

```bash
# 1. Entra en la carpeta del ejemplo
cd parte1_jinja2/ejemploB

# 2. Ejecuta el script
python render_informe.py

# 3. Verás el informe en pantalla y se guardará en informe_generado.txt
cat informe_generado.txt
```

**Prueba a modificarlo:**
Abre `render_informe.py` y añade un alumno nuevo a la lista `alumnos`,
o cambia la asignatura. Vuelve a ejecutar y observa el resultado.

---

## PARTE 2 — Ansible Playbook con Jinja2

### Requisito previo: instalar Ansible

**En Linux / macOS:**
```bash
pip install ansible
```

**En Windows:**
Ansible no se ejecuta nativamente en Windows. Usa una de estas opciones:
- **WSL** (recomendado): activa el Subsistema de Windows para Linux y sigue los pasos de Linux
- **Máquina virtual** con Ubuntu o Debian

**Verificar que Ansible está instalado:**
```bash
ansible --version
```

---

### Ejemplo C — Preparar el entorno de un alumno

**¿Qué hace?**
El playbook crea una carpeta para el alumno en `/tmp/alumnos/` y genera
dentro un fichero `bienvenida.txt` usando la plantilla Jinja2 `bienvenida.j2`.
No necesita SSH ni dispositivos remotos: todo se ejecuta en `localhost`.

**Pasos:**

```bash
# 1. Entra en la carpeta del ejemplo
cd parte2_ansible

# 2. (Opcional) Comprueba el inventario
cat inventario.yml

# 3. Ejecuta el playbook en modo simulación primero (--check no hace cambios reales)
ansible-playbook -i inventario.yml playbook_alumnos.yml --check

# 4. Ejecuta el playbook de verdad
ansible-playbook -i inventario.yml playbook_alumnos.yml

# 5. Comprueba que se ha creado el fichero
cat /tmp/alumnos/ana_garcía/bienvenida.txt
```

---

### Comandos útiles para experimentar

**Cambiar el alumno sin editar el fichero** (usando `-e` para pasar variables extra):
```bash
ansible-playbook -i inventario.yml playbook_alumnos.yml \
  -e '{"alumno": {"nombre": "Carlos Ruiz", "curso": "Python Avanzado", "grupo": "b2", "beca": false}}'
```

**Ver más detalle de lo que hace Ansible** (modo verbose):
```bash
ansible-playbook -i inventario.yml playbook_alumnos.yml -v
```

**Ejecutar solo una tarea concreta** (por su nombre):
```bash
ansible-playbook -i inventario.yml playbook_alumnos.yml \
  --start-at-task "Generar fichero de bienvenida desde plantilla Jinja2"
```

**Limpiar y volver a empezar:**
```bash
rm -rf /tmp/alumnos
ansible-playbook -i inventario.yml playbook_alumnos.yml
```

---

## Preguntas frecuentes

**¿Por qué `/tmp/alumnos` y no `/alumnos`?**
La carpeta `/tmp` no requiere permisos de administrador (root). Para producción
real usarías la ruta que corresponda y ajustarías los permisos.

**¿Puedo cambiar la plantilla `.j2`?**
Sí. Edita `templates/bienvenida.j2` o cualquier `.j2` con un editor de texto
y vuelve a ejecutar. Jinja2 / Ansible la re-renderizará con los nuevos cambios.

**¿Por qué `gather_facts: false` en el playbook?**
`gather_facts` recopila información del sistema (SO, IPs, memoria…). No la
necesitamos en este ejemplo y desactivarla hace la ejecución más rápida.

**La terminal muestra `changed` o `ok` en verde. ¿Qué significa?**
- `changed` → Ansible hizo un cambio real (creó un fichero, una carpeta…)
- `ok` → La tarea se ejecutó pero no había nada que cambiar (ya existía)
- `skipped` → La tarea se saltó porque la condición `when:` era falsa
- `failed` → Algo fue mal. Lee el mensaje de error que aparece justo encima.
