# Gestión de productos (Flask + SQLite) — Trabajo individual

Aplicación web de ejemplo para la asignatura. Incluye:

- CRUD completo de productos (crear, listar/buscar, editar, eliminar).
- Autenticación de usuarios (registro, inicio y cierre de sesión).
- Base de datos SQLite conectada (`productos.db`, tablas `usuarios` y `productos`).
- Plantillas Jinja2 en `templates/`.

> **Nota pedagógica:** el código reproduce a propósito defectos de seguridad y
> estilo comunes (MD5 en contraseñas, SQL por concatenación, secreto embebido,
> `debug=True`, excepciones amplias, imports sin usar) para poder demostrar la
> detección de las herramientas de análisis.

## Requisitos

- Python 3.10+ (probado con 3.13.3)
- Entorno virtual propio

## Instalación y ejecución

```bash
python -m venv .venv
.\.venv\Scripts\activate        # Windows PowerShell
pip install -r requirements.txt
python app.py                    # crea la base de datos y levanta el servidor
```

Abrir http://127.0.0.1:5000. Usuario por defecto: `admin` / `admin123`.

## Herramientas de análisis (uso)

```bash
pip install -r requirements-herramientas.txt

# Bandit (SAST orientado a seguridad)
bandit -r . -x .venv -f html -o reporte_bandit.html
bandit -r . -x .venv -f json -o reporte_bandit.json

# Pylint (análisis estático de calidad)
pylint app.py auth.py config.py database.py productos.py

# pip-audit (vulnerabilidades en dependencias)
pip-audit -r requirements.txt
```

## Estructura

```
app.py            # punto de entrada, arranque e inicialización
config.py         # configuración (claves, rutas)
database.py       # conexión SQLite e inicialización del esquema
auth.py           # blueprint de autenticación
productos.py      # blueprint de CRUD de productos
templates/        # plantillas Jinja2
requirements.txt  # dependencias de la aplicación
```