# Guía de exposición (5–10 minutos)

Seleccionan estudiantes al azar; prepárate para contar TÚ lo que hiciste.

## Estructura sugerida (approx.)

| Min | Qué decir |
|---|---|
| 0:00–1:30 | **Qué hice:** aplicación Flask+SQLite con CRUD de productos, login y base de datos, subida a GitHub. **Por qué:** mostrar que "funciona" no basta. |
| 1:30–3:30 | **Herramientas usadas (3):** Bandit (SAST Python), Semgrep (SAST reglas), SonarCloud (nube + Quality Gate). Menciona también la revisión por IA (Claude). |
| 3:30–6:00 | **Qué encontré (muestra 3 hallazgos):** 1) contraseñas MD5, 2) inyección SQL en login/búsqueda (payload `' OR '1'='1`), 3) secreto/credenciales en código y `debug=True`. |
| 6:00–7:30 | **Cómo lo corregí:** PBKDF2 (werkzeug), SQL parametrizado, CSRF (Flask-WTF), claves por variables de entorno, validaciones. Muestra el **antes/después** (tabla del informe). |
| 7:30–9:30 | **Evidencia:** captura del Quality Gate de SonarCloud (verde) y de los 9 issues cerrados. |
| 9:30–10 | **Aprendizaje + conclusión en 1 frase.** |

## Frase de cierre sugerida

> "Las pruebas funcionales demuestran que la app funciona; el análisis estático demuestra
> por qué puede **no ser segura**. Combinando varias herramientas pasé de 7 hallazgos
> de Bandit y 8 vulnerabilidades en SonarCloud a cero, sin romper la aplicación."

## Respuestas típicas del profesor

- **¿Y cómo sabes que quedó seguro?** → Porque re-ejecuté las herramientas (0 hallazgos) y
  probé los ataques (la inyección SQL ya no devuelve datos). La seguridad es continua:
  SonarCloud re-analiza cada push.
- **¿Falsos positivos?** → Sí, Semgrep marcó reglas de Django sobre plantillas Flask; por eso
  conviene cruzar varias herramientas e interpretar.
- **¿Por qué SonarCloud y no SonarQube local?** → No tenía Docker/Java 17; SonarCloud es la
  versión en nube, gratuita para repos públicos, e integra análisis automático con GitHub.

## No olvides
- Tener abiertas el navegador (SonarCloud + GitHub) por si quieres proyectarlas.
- Decir claramente: herramientas → hallazgos → corrección → evidencia.