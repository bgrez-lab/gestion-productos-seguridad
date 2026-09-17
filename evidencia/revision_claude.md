# Revisión de código asistida por IA (Claude)

**Herramienta:** Claude (asistente de IA para análisis de código, tipo "AI code review")
**Fecha de revisión:** 17/09/2026
**Proyecto:** Gestión de productos (Flask + SQLite)
**Método:** Revisión línea a línea del código fuente buscando vulnerabilidades,
errores de programación, malas prácticas y problemas de calidad.

## Resumen ejecutivo

Se revisaron 5 módulos Python (app, config, database, auth, productos) y 5 plantillas
HTML. Se identificaron **14 hallazgos**: 8 vulnerabilidades/fallas de seguridad,
2 errores de programación y 4 malas prácticas/calidad.

---

## Hallazgos

### VULNERABILIDADES

| # | Hallazgo | Severidad | Ubicación | Explicación | Corrección propuesta |
|---|----------|-----------|-----------|-------------|----------------------|
| C1 | Contraseñas con **MD5 sin sal** | Crítica | `auth.py:24-30`, `database.py:59-62` | MD5 está roto criptográficamente: permite ataques de diccionario/rainbow tables y colisiones. | Usar `werkzeug.security.generate_password_hash()` (PBKDF2) y `check_password_hash()`. |
| C2 | **Inyección SQL** en login | Crítica | `auth.py:40-46` | La consulta se arma concatenando `usuario` del usuario. Payload `' OR '1'='1` para evadir el login. | Parametrizar: `db.execute("SELECT * FROM usuarios WHERE usuario=? AND hash_clave=?", (usuario, hash)).fetchone()`. |
| C3 | **Inyección SQL** en búsqueda | Alta | `productos.py:49-52` | `termino` (query string) se concatena a la consulta `LIKE`. | Uso de `LIKE ?` con parámetro y escaping de `%`/`_`. |
| C4 | **SECRET_KEY embebida** en código | Alta | `config.py:11` | Cualquiera con acceso al repo puede forjar cookies de sesión. | Leer de variable de entorno (`os.environ["SECRET_KEY"]`). |
| C5 | Credenciales **por defecto** | Alta | `config.py:19-20`, `database.py:60-62` | `admin/admin123` documentado y sembrado. | Eliminar el seed; primer registro crea el admin; forzar claves fuertes. |
| C6 | `debug=True` + host `0.0.0.0` | Alta | `app.py:42-44` | El debugger de Werkzeug expone una consola interactiva (RCE) y los errores filtran datos. | `debug=False` en producción y host `127.0.0.1`; usar variable de entorno. |
| C7 | **CSRF** ausente en formularios | Media | `templates/*.html`, `productos.py:107`, `auth.py:33-52` | Los POST (crear, editar, eliminar, login, registro) no validan token CSRF: un sitio malicioso puede forzar acciones en nombre del usuario (p. ej., eliminar productos). | Activar `CSRFProtect` de Flask-WTF o añadir token CSRF manual en cada formulario. |
| C8 | **NaN injection** en precio/stock | Media | `productos.py:64,89` | `float("nan")` e `int("1e999")` aceptados desde el formulario corrompen valores y permiten operaciones aritméticas anómalas. | Validar con `math.isfinite()` y rangos; usar tipos con check. |

Inyección SQL en login: payload real (C2) — una sesión atacante que envía
`usuario=admin' OR '1'='1` loguea como admin sin conocer la clave.

### ERRORES DE PROGRAMACIÓN

| # | Hallazgo | Severidad | Ubicación | Explicación | Corrección propuesta |
|---|----------|-----------|-----------|-------------|----------------------|
| C9 | Login exitoso redirige a... login | Media-baja | `auth.py:50` | Tras validar credenciales redirige a `url_for("auth.login")`: el usuario "entra" pero vuelve a ver el formulario. Debe enviar al listado. | `return redirect(url_for("productos.listar"))`. |
| C10 | Excepción demasiado amplia | Baja | `auth.py:72`, `productos.py:66,91` | `except Exception` enmascara errores reales (p. ej., un fallo de la BD se muestra como "usuario ya existe"). | Capturar solo `ValueError`; loguear el resto. |

### MALAS PRÁCTICAS / CALIDAD

| # | Hallazgo | Categoría | Ubicación | Explicación | Corrección propuesta |
|---|----------|-----------|-----------|-------------|----------------------|
| C11 | Import sin uso | Calidad | `productos.py:18` | `import datetime` declarado y nunca usado (pylint W0611). | Eliminar la línea. |
| C12 | Sin validación de entrada | Calidad | `productos.py:61-64`, `auth.py:58-60` | Se aceptan nombre vacío y claves triviales; sin longitud mínima. | Validaciones con mensajes claros (nombres 3-100, clave >= 8). |
| C13 | Sesión sin renovación/Secure | Seguridad defensiva | `auth.py:48-49` | No se fija `session.permanent`, ni banderas `Secure`/`SameSite` de la cookie. | Configurar `SESSION_COOKIE_SAMESITE="Lax"`, terminar con cookie `Secure` en producción, y regenerar `session` tras login (anti-fijación). |
| C14 | Sin límite de intentos de login | Seguridad defensiva | `auth.py:33-52` | Permite fuerza bruta sin throttling ni bloqueo. | Roteo/delay entre intentos (p. ej. Flask-Limiter) y registrar intentos fallidos. |

---

## Lo que la IA puede y no puede hacer en análisis de código

**Puede:** leer el código completo, entender la lógica de negocio, detectar
vulnerabilidades lógicas (como C9), cruzar contextos (config + uso), explicar el
"por qué" y proponer correcciones concretas.

**No garantiza:** ser exhaustiva ni estándar (no reemplaza SAST como Semgrep/SonarQube,
que tienen reglas auditadas y cobertura sistemática), y puede equivocarse. Lo correcto
es combinar IA + SAST + revisión humana, como se hace en este trabajo.