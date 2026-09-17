# Guía de exposición (5–10 minutos)

Seleccionan estudiantes al azar; prepárate para contar TÚ lo que hiciste.
El trabajo **identifica y registra los problemas del programa original** (no los corrige).

## Estructura sugerida (approx.)

| Min | Qué decir |
|---|---|
| 0:00–1:30 | **Qué hice:** aplicación Flask+SQLite con CRUD de productos, login y base de datos, subida a GitHub. **Por qué:** mostrar que "funciona" no basta. |
| 1:30–3:30 | **Herramientas usadas (3):** Bandit (SAST Python), Semgrep (SAST reglas), SonarCloud (nube, análisis automático + Quality Gate). Menciona la revisión por IA (Claude) como complemento. |
| 3:30–6:00 | **Qué encontré (muestra 3 hallazgos):** 1) contraseñas MD5 (Bandit/SonarCloud/IA), 2) inyección SQL en login, búsqueda y borrado (payload `' OR '1'='1`), 3) `eval()`, inyección de comandos y XSS en el código. |
| 6:00–7:30 | **Registro completo:** los números por herramienta — Bandit 10, Semgrep 28 (≈12 problemas reales), SonarCloud 13 issues abiertas, IA/Claude 21. En el informe está la tabla con tipo, severidad, archivo:línea, explicación y corrección recomendada. |
| 7:30–9:30 | **Evidencia:** capturas del SonarCloud (13 issues abiertas: 11 vulnerabilidades + 2 bugs) y del repositorio con el código original. SonarCloud reabrió las issues al volver a publicar el código (reproducible). |
| 9:30–10 | **Aprendizaje + conclusión en 1 frase.** |

## Frase de cierre sugerida

> "Las pruebas funcionales demuestran que la app funciona; el análisis estático demuestra
> por qué puede **no ser segura**. Este trabajo registra los problemas del programa original:
> 10 hallazgos de Bandit, 13 issues en SonarCloud, 28 de Semgrep y 21 de la IA, todos
> localizados y explicados en el informe."

## Respuestas típicas del profesor

- **¿Y cuáles son los problemas más graves?** → La criptografía rota (MD5 para contraseñas), la
  inyección de comandos y el `eval()` (ejecución de código arbitrario), y las tres
  inyecciones SQL explotables: la de login permite entrar como *admin* sin conocer la clave con
  `' OR '1'='1`.
- **¿El programa quedó como estaba o lo arreglaste?** → No lo corregí; el objetivo era identificarlos y
  registrarlos. El código de `main` es el original, con los hallazgos señalizados en comentarios.
- **¿Falsos positivos?** → Sí, Semgrep marcó reglas de Django sobre plantillas Flask y varias reglas
  señalaron la misma línea (28 hallazgos ≈ 12 problemas); por eso conviene cruzar herramientas e interpretar.
- **¿Cómo sabes que los problemas son reales?** → Son reproducible: al volver a publicar el código
  original, SonarCloud reabrió exactamente las mismas 13 issues.
- **¿Por qué SonarCloud y no SonarQube local?** → No tenía Docker/Java 17; SonarCloud es la versión en
  nube, gratuita para repos públicos, e integra análisis automático con GitHub.

## No olvides
- Tener abiertas el navegador (SonarCloud + GitHub) por si quieres proyectarlas.
- Decir claramente: herramientas → problemas identificados (severidad y ubicación) → evidencia.