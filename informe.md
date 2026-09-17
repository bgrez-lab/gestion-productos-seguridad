# Informe: Herramientas de Análisis de Código y Detección de Vulnerabilidades

**Asignatura:** Desarrollo Avanzado — **Trabajo:** Individual
**Estudiante:** Paloma Chavez — **Fecha:** 17 de septiembre de 2026
**Repositorio:** https://github.com/bgrez-lab/gestion-productos-seguridad

---

## 1. Introducción

La calidad y la seguridad del software no se garantizan porque "el programa funcione";
muchas vulnerabilidades graves (inyecciones SQL, almacenamiento inseguro de contraseñas,
secretos expuestos) llegan a producción precisamente porque nunca se analizó el código.
Las herramientas de análisis estático (SAST) y los linters permiten detectar este tipo de
problemas de forma temprana, automatizada y económica.

Este trabajo investiga tres herramientas complementarias (**Bandit, Semgrep y SonarCloud**)
y las aplica sobre una aplicación web propia (CRUD de productos con autenticación y base de
datos SQLite). El ejercicio se completa con una revisión asistida por IA (Claude) y con la
corrección de los hallazgos para demostrar la mejora medida antes/después.

---

## 2. Herramientas investigadas

### 2.1 Bandit — SAST orientado a seguridad para Python
- **Qué es:** analizador estático de seguridad para Python, oficial de PyCQA; recorre el AST
  buscando patrones de riesgo conocidos (B-series: B201 debug, B324 MD5, B608 SQL inyección, B105 secretos).
- **Uso:** `bandit -r . -x .venv` (formato texto, JSON, HTML).

### 2.2 Semgrep — SAST de reglas (gratuito/open source)
- **Qué es:** analizador por *patrones* multiplataforma; busca código con reglas YAML
  (estilo grep con sintaxis de programación). Corre cientos de reglas de seguridad de la comunidad.
- **Uso:** `semgrep scan --config auto --json -o reporte.json`.

### 2.3 SonarCloud — Plataforma integral de calidad de código (SAST en la nube)
- **Qué es:** la versión cloud de SonarQube. Analiza 30+ lenguajes, clasifica issues en
  *Vulnerability / Bug / Code Smell* con severidad, calcula **Quality Gates** (rojo/verde) y
  detecta problemas de mantenibilidad, duplicación y cobertura.
- **Uso:** cuenta en sonarcloud.io conectada al repositorio GitHub. Análisis automático en
  cada push (integración vía GitHub App).

### 2.4 Herramientas complementarias
- **Pylint** (linter de estilo/calidad) y **pip-audit** (vulnerabilidades en dependencias),
  ya disponibles en el proyecto; **Claude** (revisión de código asistida por IA, se documenta aparte).

### 2.5 Cuadro comparativo

| Criterio | Bandit | Semgrep | SonarCloud |
|---|---|---|---|
| Categoría | SAST (seguridad) | SAST (reglas) | Plataforma calidad + SAST |
| Instalación | `pip install bandit` | `pip install semgrep` | Nube + GitHub App |
| Lenguajes | Python | C/Js/Python/Go, etc. (64+) | 30+ lenguajes |
| Detección principal | Patrones de riesgo Python | Reglas personalizables (YAML) | Bugs, vulns, code smells, duplicación |
| Quality Gate | No | No | **Sí** (rojo/verde) |
| Alertas por severidad | Sí (low/med/high) | Sí (warning/error) | Sí (info…blocker) |
| Integración CI/CD | Script | Script | Automática en cada push |
| Cobertura de pruebas | No | No | Sí |
| Ventajas | Simple, rápido, enfocado en seguridad Python | Multilenguaje, reglas escribibles a medida, gratuito | Dashboard completo, Quality Gate, duplicación/cobertura |
| Desventajas | Solo Python, sin reglas propias | Sirve de configuración, puede dar falsos positivos si se adaptan reglas de otros frameworks | Depende de la nube; el plan gratuito exige repositorio público |

---

## 3. Descripción del programa desarrollado

Aplicación web **Flask + SQLite** que gestiona productos de un catálogo:

- **CRUD completo** sobre la entidad *producto* (crear, listar/buscar, editar, eliminar).
- **Autenticación** con registro, inicio y cierre de sesión, sobre la entidad *usuario*.
- **Base de datos relacional** SQLite conectada (`productos.db`, tablas `usuarios` y `productos`).

Esquema:

```
app.py            → arranque, configuración de seguridad (CSRF, secret key)
auth.py           → registro, login, logout
productos.py      → CRUD de productos
database.py       → conexión SQLite e inicialización del esquema
config.py         → configuración (clave, rutas)
templates/        → plantillas Jinja2 (base, login, registro, listar, formulario)
```

Para poder *demostrar* la detección de las herramientas, la versión inicial incluía
**a propósito** defectos clásicos de aplicaciones reales: contraseñas con MD5, consultas SQL
por concatenación, clave secreta embebida, `debug=True`, excepciones demasiado amplias e
imports sin uso.

---

## 4. Metodología

1. **Preparación:** se configuró el control de versiones (Git), un `.gitignore` correcto y se
   publicó el proyecto en GitHub (`bgrez-lab/gestion-productos-seguridad`).
2. **Análisis inicial (baseline):** se ejecutaron Bandit, pylint, Semgrep y SonarCloud sobre la
   versión vulnerable y se documentó cada hallazgo. Se completó con una revisión línea a línea
   asistida por IA (Claude).
3. **Análisis de resultados:** para cada hallazgo se registró tipo, severidad, ubicación,
   explicación y corrección propuesta.
4. **Corrección:** se aplicaron las correcciones (hash seguro, SQL parametrizado, CSRF,
   claves por entorno, validaciones).
5. **Re-análisis:** se volvió a ejecutar cada herramienta sobre el código corregido para cuantificar
   la mejora; SonarCloud se re-analiza solo en cada push.

---

## 5. Resultados del análisis

### 5.1 Resumen antes / después

| Herramienta | Versión vulnerable | Versión corregida | Mejora |
|---|---|---|---|
| Bandit | 7 hallazgos (2 high) | **0** | 100 % |
| Semgrep | 16 hallazgos | 4 (falsos positivos) | 12 detectados reales |
| SonarCloud | 9 issues (8 vulnerabilidades) | **0 abiertas** (Quality Gate OK) | 100 % |
| Pylint | 9.46/10 | **9.94/10** | +0.48 |
| Claude (IA) | 14 hallazgos | verificados corregidos | — |

### 5.2 Hallazgo más importante 1: contraseñas con MD5 (crítico)

- **Tipo:** vulnerabilidad — **Severidad:** crítica (Bandit B324; SonarCloud S4790; IA C1).
- **Ubicación:** `auth.py:30` y `database.py:61` (semilla del admin).
- **Explicación:** MD5 es criptográficamente roto; permite ataques de diccionario y rainbow tables.
- **Corrección:** `werkzeug.security.generate_password_hash()` (PBKDF2 con salt) para crear y
  `check_password_hash()` para verificar.

### 5.3 Hallazgo 2: inyección SQL (crítico)

- **Tipo:** vulnerabilidad — **Severidad:** alta (Bandit B608; Semgrep tainted-sql-string; IA C2-C3).
- **Ubicación:** `auth.py:43` (login) y `productos.py:51` (búsqueda).
- **Explicación:** el dato del usuario se concatena en la cadena SQL. Payload `' OR '1'='1`
  para evadir el login.
- **Corrección:** consultas parametrizadas: `SELECT ... WHERE usuario = ?` y `LIKE ? ESCAPE '\'`.

### 5.4 Hallazgo 3: CSRF desactivado (crítico según SonarCloud, S4502)

- **Tipo:** vulnerabilidad — **Severidad:** crítica (SonarCloud) / alta (IA C7).
- **Ubicación:** `app.py:17` y todos los formularios POST.
- **Explicación:** sin token CSRF, un sitio malicioso puede hacer que el navegador de una
  sesión autenticada ejecute acciones (crear, editar, **eliminar** productos).
- **Corrección:** `CSRFProtect(app)` de Flask-WTF + campo oculto `csrf_token` en cada formulario.

### 5.5 Hallazgo 4: secreto y credenciales embebidos (alto)

- **Tipo:** vulnerabilidad — **Severidad:** alta (Bandit B105; IA C4-C5).
- **Ubicación:** `config.py:11`, `config.py:19-20`.
- **Explicación:** quien tenga el repositorio puede forjar cookies de sesión y conocer el acceso
  del admin por defecto.
- **Corrección:** `SECRET_KEY` desde variable de entorno; se eliminan las credenciales por defecto.

### 5.6 Hallazgo 5: servidor en modo debug (alto)

- **Tipo:** vulnerabilidad — **Severidad:** alta (Bandit B201; SonarCloud S8392+S4507; Semgrep).
- **Ubicación:** `app.py:44`.
- **Explicación:** `debug=True` y host `0.0.0.0` exponen el depurador de Werkzeug, que permite
  ejecución remota de código, y filtran información sensible en errores.
- **Corrección:** `host="127.0.0.1"` y `debug` controlado por variable de entorno.

### 5.7 Otros hallazgos corregidos

| # | Tipo | Severidad | Ubicación | Hallazgo | Corrección |
|---|---|---|---|---|---|
| 6 | Vulnerabilidad | Media | `productos.py:64,89` | NaN injection en precio/stock | Validar con `math.isfinite` y rangos |
| 7 | Error | Media | `auth.py:50` | Login exitoso redirigía al propio login | Redirigir a `productos.listar` |
| 8 | Mala práctica | Baja | `auth.py:72`, `productos.py:66,91` | `except Exception` genérico | Capturar `sqlite3.IntegrityError`/`ValueError` |
| 9 | Calidad | Baja | `productos.py:18` | Import `datetime` sin uso | Eliminar la línea |
| 10 | Calidad | Baja | `templates/listar.html:6` | Campo de búsqueda sin `label` (accesibilidad) | Añadir `label for` + `id` |

### 5.8 Falsos positivos (aprendizaje)
Semgrep reportó 4 avisos de "no-csrf-token" aplicando reglas **de Django** sobre plantillas de
**Flask**; tras la corrección CSRF, la app quedó protegida (con Flask-WTF) y esos avisos son
falsos positivos. Esto demuestra que **ninguna herramienta es infalible** y que conviene
contrastar varias antes de afirmar que algo es seguro.

---

## 6. Evidencia generada

Toda la evidencia está en la carpeta `evidencia/` del repositorio:

- `semgrep_scan.json` / `semgrep_scan_corregido.json` — reportes Semgrep (antes/después).
- `bandit_corregido.json` — Bandit tras corrección (0 hallazgos).
- `sonarcloud_issues.json` / `sonarcloud_issues_final.json` — issues de SonarCloud (antes/después).
- `revision_claude.md` — revisión asistida por IA con 14 hallazgos y su análisis.
- Capturas de pantalla del dashboard de SonarCloud, del Quality Gate y del repositorio
  (ver `guia_capturas.md`): se adicionan como imágenes adjuntas a este informe.

---

## 7. Conclusiones y aprendizajes

1. **El análisis estático encuentra lo que las pruebas funcionales no ven.** La app "funcionaba",
   pero tenía una inyección SQL que permitía entrar como *admin* sin contraseña.
2. **Las herramientas se complementan:** Bandit (seguridad Python), Semgrep (reglas), SonarCloud
   (calidad global + Quality Gate), pylint (estilo) y la revisión por IA (lógica de negocio)
   detectaron en conjunto **más problemas que cualquiera por separado**.
3. **Los falsos positivos existen** (reglas Django sobre plantillas Flask en Semgrep): es necesario
   interpretar los resultados, no copiarlos.
4. **La corrección es medible:** se pasó de 7 hallazgos de Bandit y 8 vulnerabilidades de SonarCloud
   a **0** en ambos, sin romper la funcionalidad (pruebas de humo verificadas).
5. **Automatizar el análisis** (SonarCloud en cada *push*) convierte la seguridad en un proceso
   continuo, no en una revisión puntual.
6. **Buena práctica aprendida:** nunca guardar secretos en el código, siempre parametrizar SQL y
   usar funciones de hash seguras con salt.

---

## 8. Referencias

- Bandit — PyCQA: https://bandit.readthedocs.io/ — https://github.com/PyCQA/bandit
- Semgrep: https://semgrep.dev/docs/ — reglas: https://semgrep.dev/explore
- SonarCloud (SonarQube Cloud): https://sonarcloud.io/ — https://www.sonarsource.com/
- Flask-WTF / CSRF: https://flask-wtf.readthedocs.io/
- Repositorio del trabajo: https://github.com/bgrez-lab/gestion-productos-seguridad