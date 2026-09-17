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

El objetivo de este trabajo es **investigar y aplicar al menos tres herramientas de análisis
de código y registrar los problemas que presenta el programa original**. Para ello se desarrolló
una aplicación web propia (CRUD de productos con autenticación y base de datos SQLite) que incluye,
deliberadamente, defectos clásicos de las aplicaciones reales, y se analizó **sin corregir nada**:
el código entregado es la versión original tal como fue analizada. El informe registra cada
problema detectado por **Bandit, Semgrep, SonarCloud** y una revisión asistida por IA (Claude),
indicando tipo, severidad, ubicación, explicación y la corrección recomendada.

---

## 2. Herramientas investigadas

### 2.1 Bandit — SAST orientado a seguridad para Python
- **Qué es:** analizador estático de seguridad para Python, oficial de PyCQA; recorre el AST
  buscando patrones de riesgo conocidos (B-series: B201 debug, B324 MD5, B608 SQL inyección, B105 secretos).
- **Uso:** `bandit -r . -x .venv -f json -o evidencia/bandit_antes.json`.
- **Resultado sobre el programa original:** **10 hallazgos** (4 High, 5 Medium, 1 Low).

### 2.2 Semgrep — SAST de reglas (gratuito/open source)
- **Qué es:** analizador por *patrones* multiplataforma; busca código con reglas YAML
  (estilo grep con sintaxis de programación). Corre cientos de reglas de seguridad de la comunidad.
- **Uso:** `semgrep scan --config auto --json -o evidencia/semgrep_scan.json`.
- **Resultado sobre el programa original:** **28 hallazgos** en 10 archivos (15 error / 13 warning);
  varias familias de reglas (django/flask/sqlalchemy) coinciden sobre la misma línea, por lo que el
  número de problemas reales es menor.

### 2.3 SonarCloud — Plataforma integral de calidad de código (SAST en la nube)
- **Qué es:** la versión cloud de SonarQube. Clasifica issues en *Vulnerability / Bug / Code Smell*
  con severidad, calcula **Quality Gates** y detecta problemas de mantenibilidad, duplicación y cobertura.
- **Uso:** cuenta en sonarcloud.io conectada al repositorio GitHub; análisis automático en cada push
  (integración vía GitHub App). No requirió Docker ni Java 17 (necesarios para SonarQube local).
- **Resultado sobre el programa original:** **13 issues abiertas** (11 vulnerabilidades + 2 bugs).

### 2.4 Revisión por IA (Claude) — herramienta complementaria
- **Qué es:** revisión línea a línea del código asistida por un modelo de lenguaje
  ("AI code review"), que además de patrones detecta problemas de lógica de negocio.
- **Resultado sobre el programa original:** **21 hallazgos** (15 de seguridad, 2 errores,
  4 malas prácticas/calidad), documentados en `evidencia/revision_claude.md`.

### 2.5 Cuadro comparativo

| Criterio | Bandit | Semgrep | SonarCloud |
|---|---|---|---|
| Categoría | SAST (seguridad) | SAST (reglas) | Plataforma calidad + SAST |
| Instalación | `pip install bandit` | `pip install semgrep` | Nube + GitHub App |
| Lenguajes | Python | 64+ lenguajes | 30+ lenguajes |
| Detección principal | Patrones de riesgo Python | Reglas personalizables (YAML) | Bugs, vulns, code smells, duplicación |
| Quality Gate | No | No | **Sí** (rojo/verde) |
| Alertas por severidad | Sí (low/medium/high) | Sí (warning/error) | Sí (info…blocker) |
| Integración CI/CD | Script | Script | Automática en cada push |
| Cobertura de pruebas | No | No | Sí |
| Ventajas | Simple, rápido, enfocado en seguridad Python | Multilenguaje, reglas a medida, gratuito | Dashboard completo, Quality Gate, análisis continuo |
| Desventajas | Solo Python, sin reglas propias | Falsos positivos si se aplican reglas de otros frameworks | Depende de la nube; plan gratuito exige repo público |

---

## 3. Descripción del programa analizado (versión original)

Aplicación web **Flask + SQLite** que gestiona productos de un catálogo:

- **CRUD completo** sobre la entidad *producto* (crear, listar/buscar, editar, eliminar).
- **Autenticación** con registro, inicio y cierre de sesión, sobre la entidad *usuario*.
- **Base de datos relacional** SQLite conectada (`productos.db`, tablas `usuarios` y `productos`).
- **Funciones extra de tipo estudiantil:** cálculo de precio con impuesto (`/impuesto`, acepta una
  expresión), importación de lotes por línea de comandos (`/importar`) y página de perfil (`/perfil`).

Esquema:

```
app.py            → arranque y configuración de la aplicación
auth.py           → registro, login, logout
productos.py      → CRUD de productos
database.py       → conexión SQLite e inicialización del esquema
config.py         → configuración (clave, credenciales)
templates/        → plantillas Jinja2 (base, login, registro, listar, formulario)
```

El código entregado en la rama `main` es la **versión original, sin correcciones**; los hallazgos
están además señalizados con comentarios en el propio código (p. ej. `# Hallazgo B201 (Bandit)`)
para facilitar su revisión. Este trabajo **no corrige el programa**: su alcance es identificar y
registrar los problemas detectados.

---

## 4. Metodología

1. **Publicación del proyecto:** se inicializó Git, se configuró `.gitignore` y se publicó el
   proyecto en GitHub (`bgrez-lab/gestion-productos-seguridad`).
2. **Análisis SAST/Bandit:** ejecución de Bandit sobre los módulos Python del programa original.
3. **Análisis Semgrep:** ejecución con `--config auto`, guardando el reporte JSON.
4. **Análisis SonarCloud:** conexión del repositorio y análisis automático; registro de las issues abiertas.
5. **Revisión por IA:** lectura del código con Claude, con 21 hallazgos documentados.
6. **Registro:** para cada hallazgo se documentó tipo, severidad, ubicación exacta (archivo:línea),
   explicación del riesgo y corrección recomendada.
7. **Verificación de reproducibilidad:** el código original se volvió a publicar en `main` y
   SonarCloud reabrió las issues, confirmando que los problemas registrados existen y son reproducibles.

---

## 5. Registro de problemas detectados en el programa original

### 5.1 Resumen por herramienta

| Herramienta | Hallazgos | Severidades destacadas | Reporte |
|---|---|---|---|---|
| Bandit | **10** | 4 High · 5 Medium · 1 Low | `evidencia/bandit_antes.json` |
| Semgrep | **28** | 15 error / 13 warning | `evidencia/semgrep_scan.json` |
| SonarCloud | **13** | 6 Blocker · 3 Critical · 1 Minor · 3 Major | `evidencia/sonarcloud_issues.json` |
| IA (Claude) | **21** | 5 crítica · 6 alta · 4 media · 6 baja | `evidencia/revision_claude.md` |

### 5.2 Bandit — 10 hallazgos

| # | Test | Severidad | CWE | Ubicación | Problema detectado |
|---|---|---|---|---|---|
| B1 | B201 `flask_debug_true` | High | CWE-94 | `app.py:44` | `debug=True` expone el depurador Werkzeug (ejecución de código arbitrario) |
| B2 | B104 `hardcoded_bind_all_interfaces` | Medium | CWE-605 | `app.py:44` | Host `0.0.0.0`: la app queda accesible desde toda la red |
| B3 | B324 `hashlib` | High | CWE-327 | `auth.py:31` | Hash MD5 para contraseñas (criptografía rota) |
| B4 | B608 `hardcoded_sql_expressions` | Medium | CWE-89 | `auth.py:44` | Consulta SQL por concatenación (login) |
| B5 | B105 `hardcoded_password_string` | Low | CWE-259 | `config.py:11` | Secreto embebido en el código fuente |
| B6 | B324 `hashlib` | High | CWE-327 | `database.py:61` | Seed del admin con MD5 |
| B7 | B608 `hardcoded_sql_expressions` | Medium | CWE-89 | `productos.py:52` | Consulta SQL por concatenación (búsqueda `LIKE`) |
| B8 | B307 `eval_used` | Medium | CWE-95 | `productos.py:119` | `eval()` sobre expresión controlada por el usuario (`/impuesto`) |
| B9 | B608 `hardcoded_sql_expressions` | Medium | CWE-89 | `productos.py:131` | Consulta SQL por concatenación (eliminar: `DELETE ... WHERE id = " + id`) |
| B10 | B605 `start_process_with_shell` | High | CWE-78 | `productos.py:148` | `os.system()` con el nombre de archivo del usuario (`/importar`) → inyección de comandos |

### 5.3 Semgrep — 28 hallazgos

| # | Severidad | Regla | Ubicación | Problema detectado |
|---|---|---|---|---|
| S1 | warning | `python.flask.security.audit.app-run-param-conf` | `app.py:44` | Servidor expuesto públicamente (`host=0.0.0.0`) |
| S2 | warning | `python.flask.security.audit.debug-enabled` | `app.py:44` | `debug=True` en producción |
| S3 | error | `python.django.security.injection.tainted-sql-string` | `auth.py:43` | SQL construido con datos del usuario (login) |
| S4 | error | `python.flask.security.injection.tainted-sql-string` | `auth.py:43` | Ídem (regla Flask) |
| S5 | warning | `python.django.security.injection.sql.sql-injection` | `auth.py:38` | Dato del request llega a `execute()` |
| S6 | warning | `python.lang.security.audit.formatted-sql-query` | `auth.py:47` | Posible SQL formateado |
| S7 | error | `python.sqlalchemy.security.sqlalchemy-execute-raw` | `auth.py:47` | Concatenación con entrada no confiable |
| S8 | error | `python.django.security.injection.tainted-sql-string` | `productos.py:52` | SQL construido en búsqueda |
| S9 | error | `python.flask.security.injection.tainted-sql-string` | `productos.py:52` | Ídem (regla Flask) |
| S10 | error | `python.sqlalchemy.security.sqlalchemy-execute-raw` | `productos.py:53` | Concatenación en `execute()` |
| S11 | error | `python.flask.security.injection.tainted-sql-string` | `productos.py:131` | SQL construido en el borrado (`DELETE`) |
| S12 | error | `python.sqlalchemy.security.sqlalchemy-execute-raw` | `productos.py:131` | Concatenación del `id` en `execute()` |
| S13 | error | `python.flask.security.injection.nan-injection` | `productos.py:65` | Entrada del usuario a `float()` (NaN injection) |
| S14 | error | `python.flask.security.injection.nan-injection` | `productos.py:90` | Entrada del usuario a `float()`/`int()` |
| S15 | error | `python.flask.security.open-redirect` | `auth.py:55` | Redirección a `?next=` sin validar (open redirect) |
| S16 | error | `python.flask.security.injection.user-eval` | `productos.py:119` | `eval()` con entrada del usuario (`/impuesto`) |
| S17 | warning | `python.django.security.injection.user-eval` | `productos.py:117` | Ídem (regla Django) |
| S18 | warning | `python.lang.security.audit.eval-detected` | `productos.py:119` | Uso de `eval()` detectado |
| S19 | error | `python.django.security.injection.command-injection-os-system` | `productos.py:146` | Comando shell con entrada del usuario (`/importar`) |
| S20 | error | `python.flask.security.injection.os-system-injection` | `productos.py:148` | `os.system()` con datos del usuario |
| S21 | error | `python.lang.security.audit.dangerous-system-call` | `productos.py:148` | Llamada peligrosa al sistema |
| S22 | warning | `python.flask.security.audit.directly-returned-format-string` | `productos.py:120` | Cadena formateada devuelta directamente |
| S23 | warning | `python.flask.security.audit.render-template-string` | `auth.py:102` | `render_template_string` (posible SSTI) |
| S24 | warning | `python.django.security.django-no-csrf-token` | `formulario.html:4` | Formulario sin token CSRF |
| S25 | warning | `python.django.security.django-no-csrf-token` | `listar.html:15` | Formulario sin token CSRF (importar lote) |
| S26 | warning | `python.django.security.django-no-csrf-token` | `listar.html:31` | Formulario sin token CSRF (eliminar) |
| S27 | warning | `python.django.security.django-no-csrf-token` | `login.html:4` | Formulario sin token CSRF |
| S28 | warning | `python.django.security.django-no-csrf-token` | `registro.html:4` | Formulario sin token CSRF |

Nota: S3–S12 son las tres inyecciones SQL reales (login `auth.py:44`, búsqueda `productos.py:52` y
borrado `productos.py:131`) vistas por varias familias de reglas (django/flask/sqlalchemy);
S16–S18 y S19–S21 son respectivamente el mismo `eval()` y el mismo `os.system()` reportados por
distintas familias de reglas. Los avisos `django-no-csrf-token` aplican reglas de Django sobre
plantillas de Flask (falso positivo parcial: el programa original no tiene protección CSRF).

### 5.4 SonarCloud — 13 issues abiertas

| # | Regla | Severidad | Tipo | Ubicación | Problema detectado |
|---|---|---|---|---|---|
| Q1 | `python:S4502` | Critical | Vulnerabilidad | `app.py:17` | Protección CSRF desactivada |
| Q2 | `python:S8392` | Blocker | Vulnerabilidad | `app.py:44` | Aplicación vinculada a todas las interfaces |
| Q3 | `python:S4507` | Minor | Vulnerabilidad | `app.py:44` | Depuración (`debug`) habilitada |
| Q4 | `python:S4790` | Critical | Vulnerabilidad | `auth.py:31` | Hashing de datos inseguro (MD5) |
| Q5 | `python:S4790` | Critical | Vulnerabilidad | `database.py:61` | Hashing de datos inseguro (MD5) |
| Q6 | `pythonsecurity:S5146` | Blocker | Vulnerabilidad | `auth.py:57` | Redirección controlada por el usuario (`?next=`) sin validar |
| Q7 | `pythonsecurity:S5334` | Blocker | Vulnerabilidad | `productos.py:119` | Evaluación de código del usuario (`eval`) |
| Q8 | `pythonsecurity:S5131` | Blocker | Vulnerabilidad | `productos.py:120` | Salida formateada devuelta directamente al navegador |
| Q9 | `pythonsecurity:S2076` | Blocker | Vulnerabilidad | `productos.py:148` | Inyección de comandos del sistema (`os.system`) |
| Q10 | `Web:InputWithoutLabelCheck` | Major | Bug (accesibilidad) | `listar.html:6` | Campo de búsqueda sin `label` |
| Q11 | `Web:S5247` | Major | Vulnerabilidad | `listar.html:10` | XSS reflejado por `{{ termino|safe }}` |
| Q12 | `pythonsecurity:S5131` | Blocker | Vulnerabilidad | `listar.html:10` | Contenido del usuario incrustado sin escapar |
| Q13 | `Web:InputWithoutLabelCheck` | Major | Bug (accesibilidad) | `listar.html:17` | Campo "archivo" sin `label` |

Nota: en un análisis anterior la plataforma reportó además 3 issues de tipo `githubactions` relativas
al workflow de CI (pin de acciones, versionado de dependencias); dicho archivo se retiró del repositorio
(la integración usa la GitHub App de SonarCloud) y, por tanto, el código del programa registra las
**13 issues** de la tabla, que quedan **abiertas** en el análisis del código entregado.

### 5.5 Revisión por IA (Claude) — 21 hallazgos

Vulnerabilidades (15):

| # | Hallazgo | Severidad | Ubicación |
|---|---|---|---|
| C1 | Contraseñas con MD5 sin sal | Crítica | `auth.py:31`, `database.py:61` |
| C2 | Inyección SQL en login | Crítica | `auth.py:40-47` |
| C3 | Inyección SQL en búsqueda | Alta | `productos.py:50-53` |
| C4 | SECRET_KEY embebida en código | Alta | `config.py:11` |
| C5 | Credenciales por defecto (`admin/admin123`) | Alta | `config.py:19-20`, `database.py:60-62` |
| C6 | `debug=True` + host `0.0.0.0` | Alta | `app.py:42-44` |
| C7 | CSRF ausente en formularios | Media | `templates/*.html` |
| C8 | NaN injection en precio/stock | Media | `productos.py:65,90` |
| C15 | `eval()` en `/impuesto` → ejecución de código | Crítica | `productos.py:117-120` |
| C16 | Inyección de comandos en `/importar` (`os.system`) | Crítica | `productos.py:146-148` |
| C17 | Inyección SQL en el borrado (`DELETE`) | Alta | `productos.py:131` |
| C18 | XSS reflejado en la búsqueda (`{{ termino\|safe }}`) | Alta | `listar.html:10` |
| C19 | SSTI en `/perfil` (`render_template_string`) | Alta | `auth.py:99-104` |
| C20 | Open redirect por `?next=` sin validar | Media | `auth.py:53-59` |
| C21 | Contraseña de BD embebida (`CLAVE_BD`) | Media | `config.py:22` |

Errores de programación (2): C9 login exitoso redirige al propio login y muestra el aviso de
bienvenida (`auth.py:50-59`); C10 excepción demasiado amplia (`auth.py:80`, `productos.py:67,92`).

Malas prácticas / calidad (4): C11 import sin uso (`productos.py:18`); C12 sin validación de
entrada (nombres vacíos, claves triviales); C13 sesión sin renovación ni cookie `Secure`/`SameSite`;
C14 sin límite de intentos de login (fuerza bruta).

---

## 6. Evidencia generada (capturas de las fuentes reales)

Las capturas se tomaron de la **página oficial** de SonarCloud (URL pública del proyecto) y del
repositorio en **GitHub**, además de las **salidas reales** de las herramientas locales ejecutadas
sobre el código original:

| Captura | Fuente (dónde se ejecuta) | Muestra |
|---|---|---|
| `evidencia/capturas/captura_sonar_overview.png` | sonarcloud.io (página oficial) | Overview del proyecto: el programa original con 13 issues abiertas |
| `evidencia/capturas/captura_sonar_issues.png` | sonarcloud.io (página oficial) | Lista de las 13 issues abiertas (`resolved=false`) |
| `evidencia/capturas/captura_quality_gate.png` | sonarcloud.io (página oficial) | Condiciones del Quality Gate |
| `evidencia/capturas/captura_github_repo.png` | github.com (página oficial) | Repositorio con el código original en `main` |
| `evidencia/capturas/captura_semgrep_antes.png` | Ejecución local (terminal) | Salida real de `semgrep scan` sobre el código original (28 hallazgos) |
| `evidencia/capturas/captura_bandit_antes.png` | Ejecución local (terminal) | Salida real de `bandit` sobre el código original (10 hallazgos) |
| `evidencia/capturas/captura_pylint.png` | Ejecución local (terminal) | Salida real de `pylint` (9.43/10) |

URLs oficiales:

- https://sonarcloud.io/project/overview?id=bgrez-lab_gestion-productos-seguridad
- https://sonarcloud.io/project/issues?id=bgrez-lab_gestion-productos-seguridad&resolved=false
- https://github.com/bgrez-lab/gestion-productos-seguridad

---

## 7. Análisis de los problemas registrados

Agrupando los hallazgos de las cuatro fuentes (se contó cada problema real una sola vez):

| Categoría | CWE/OWASP | Problemas | Herramientas que lo detectaron |
|---|---|---|---|---|
| Criptografía rota (MD5 sin sal) | CWE-327 | 1 | Bandit, SonarCloud, IA |
| Inyección SQL | CWE-89 / A03 | 3 (login, búsqueda y borrado) | Bandit, Semgrep, SonarCloud, IA |
| Ejecución de código (eval) | CWE-95 | 1 | Bandit, Semgrep, SonarCloud, IA |
| Inyección de comandos | CWE-78 / A03 | 1 | Bandit, Semgrep, SonarCloud, IA |
| XSS reflejado / SSTI | CWE-79 | 2 (`termino\|safe`, `render_template_string`) | SonarCloud, Semgrep, IA |
| Open redirect | CWE-601 | 1 | SonarCloud, Semgrep, IA |
| Configuración peligrosa (debug, 0.0.0.0, CSRF off) | CWE-605/A05, A07 | 3 | Bandit, Semgrep, SonarCloud, IA |
| Secretos en el código | CWE-259 | 2 (SECRET_KEY, CLAVE_BD) + credenciales admin | Bandit, IA |
| CSRF sin token en formularios | A01 | 5 formularios | Semgrep, SonarCloud, IA |
| NaN injection | CWE-20 | 1 | Semgrep, IA |
| Errores de programación | — | 2 | IA, Pylint |
| Accesibilidad / calidad | WCAG | 2 | SonarCloud, Pylint |

**Conclusión del registro:** el programa original presenta problemas en 7 de las 10 categorías
principales de OWASP (A01-A07), siendo los más graves la criptografía rota, tres inyecciones SQL
explotables (acceso como *admin* con `' OR '1'='1` sin contraseña), la evaluación de código con
`eval()`/`os.system` y los XSS reflejados. Ninguna prueba funcional "normal" los detectaría; solo
el análisis estático y la revisión sistemática.

---

## 8. Reflexión sobre las herramientas (aprendizaje)

1. **Se complementan:** Bandit detectó los 10 problemas de seguridad Python de un vistazo;
   Semgrep amplió con NaN injection, open redirect y CSRF; SonarCloud dio el mapa completo con
   severidades y calidad; la IA explicó el "porqué" y detectó errores lógicos (C9) que los SAST no ven.
2. **Los falsos positivos existen:** el aviso `django-no-csrf-token` de Semgrep aplica reglas de
   Django sobre plantillas de Flask. Hay que interpretar y contrastar, no copiar reportes.
3. **Varias reglas marcan lo mismo:** Semgrep reportó 28 hallazgos que corresponden a ~12 problemas
   reales (duplicación django/flask/sqlalchemy); la deduplicación requiere criterio.
4. **Es reproducible:** al ampliar el código con más defectos típicos y volver a publicarlo,
   SonarCloud reanalizó y abrió exactamente las 13 issues esperadas, confirmando la validez del registro.

---

## 9. Conclusiones

1. **El análisis estático encuentra lo que las pruebas funcionales no ven.** El programa "funcionaba",
   pero contenía criptografía rota y dos inyecciones SQL explotables (acceso como *admin* sin clave).
2. **El objetivo del trabajo se cumplió:** se investigaron y aplicaron 3+ herramientas y se **registró
   el problema que presenta el programa original** (10 + 28 + 13 + 21 hallazgos), con tipo, severidad,
   ubicación, explicación y corrección recomendada.
3. **Ninguna herramienta es infalible ni total:** cruzando varias (SAST + SonarCloud + IA) se logra
   cobertura y contexto; también aparecen falsos positivos que exigen criterio profesional.
4. **El alcance fue solo la identificación:** no se modificó el programa original; las soluciones
   recomendadas quedan documentadas en el registro como siguiente paso del ciclo de desarrollo.
5. **Automatizar el análisis** (SonarCloud en cada push) convierte la seguridad en un proceso continuo.

---

## 10. Referencias

- Bandit — PyCQA: https://bandit.readthedocs.io/ — https://github.com/PyCQA/bandit
- Semgrep: https://semgrep.dev/docs/ — reglas: https://semgrep.dev/explore
- SonarCloud (SonarQube Cloud): https://sonarcloud.io/ — https://www.sonarsource.com/
- Flask-WTF / CSRF: https://flask-wtf.readthedocs.io/
- OWASP Top 10: https://owasp.org/www-project-top-ten
- Repositorio del trabajo: https://github.com/bgrez-lab/gestion-productos-seguridad