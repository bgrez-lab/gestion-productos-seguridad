# Gestión de productos (Flask + SQLite) — Trabajo individual

Aplicación web de ejemplo para la asignatura **Desarrollo Avanzado** sobre análisis
de código y detección de vulnerabilidades. Incluye:

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
- Entorno virtual propio (`.venv`)

## Instalación y ejecución

```bash
python -m venv .venv
.\.venv\Scripts\activate        # Windows PowerShell
pip install -r requirements.txt
python app.py                    # crea la base de datos y levanta el servidor
```

Abrir http://127.0.0.1:5000. Usuario por defecto: `admin` / `admin123`.

## Herramientas de análisis utilizadas

| Herramienta | Categoría | Instalación | Uso |
|---|---|---|---|
| **Bandit** | SAST (seguridad) | `pip install bandit` | `bandit -r . -x .venv -f html -o reporte_bandit.html` |
| **Pylint** | Linter (calidad) | `pip install pylint` | `pylint app.py auth.py config.py database.py productos.py` |
| **Semgrep** | SAST (reglas) | `pip install semgrep` | `semgrep scan --config auto --json -o evidencia/semgrep_scan.json` |
| **SonarCloud** | Plataforma calidad + SAST (nube) | Cuenta en sonarcloud.io conectada al repo vía GitHub App | Analiza **automáticamente** en cada push a `main` |
| **Pip-audit** | Dependencias | `pip install pip-audit` | `pip-audit -r requirements.txt` |
| **Claude (IA)** | Code review por IA | Conversación guiada | Revisión línea a línea con hallazgos y correcciones (ver `evidencia/revision_claude.md`) |

### Resultados principales (versión vulnerable)

- **Bandit:** 6 hallazgos (MD5, inyección SQL, secreto embebido, debug, credenciales).
- **Semgrep:** 16 hallazgos (inyección SQL, debug, NaN injection, CSRF, etc.).
- **SonarCloud:** 9 issues — 8 vulnerabilidades (2 bloqueantes/críticas) + 1 bug. Quality Gate ROJO.
- **Claude:** 14 hallazgos (vulnerabilidades, errores y malas prácticas).

Ver `evidencia/` con los reportes y `informe.md` con el análisis completo.

## Estructura

```
app.py            # punto de entrada, arranque e inicialización
config.py         # configuración (claves, rutas)
database.py       # conexión SQLite e inicialización del esquema
auth.py           # blueprint de autenticación
productos.py      # blueprint de CRUD de productos
templates/        # plantillas Jinja2
evidencia/        # reportes y capturas de las herramientas
sonar-project.properties  # configuración del análisis de Sonar
requisitos: requirements.txt y requirements-herramientas.txt
```