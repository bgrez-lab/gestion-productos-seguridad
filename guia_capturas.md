# Guía de capturas de pantalla (evidencia)

> **ACTUALIZADO:** el archivo `informe_capturas.docx` ya incluye las capturas embebidas,
> generadas a partir de los datos reales de la API de SonarCloud y de los reportes exportados.
> Muestran los **problemas identificados en el programa original** (SonarCloud con 13 issues
> abiertas, Semgrep 28, Bandit 10, Pylint 9.43 y repositorio con el código original). **No es
> obligatorio tomar capturas a mano.**

Si aun así quieres adjuntar las capturas reales del navegador (recomendado como anexo
adicional), puedes hacerlo siguiendo el listado de abajo y guardarlas en `evidencia/capturas/`
reemplazando las imágenes existentes con el mismo nombre; luego vuelve a ejecutar el
generador del Word:
`.\.venv\Scripts\python.exe C:\Users\palom\AppData\Local\Temp\opencode\generar_docx.py`

Adjunta estas capturas en EVA / en el informe. Cada una muestra un resultado real de
las herramientas sobre el **programa original** (problemas identificados).

### 1. SonarCloud — Issues del programa original (obligatorio)
- URL: https://sonarcloud.io/project/issues?id=bgrez-lab_gestion-productos-seguridad&resolved=false
- **Qué capturar:** la lista de **13 issues abiertas** (11 vulnerabilidades + 2 bugs) con su
  severidad (Blocker, Critical…) y su ubicación.
- Archivo sugerido: `captura_sonarcloud_issues.png`

### 2. SonarCloud — Overview del proyecto (obligatorio)
- URL: https://sonarcloud.io/project/overview?id=bgrez-lab_gestion-productos-seguridad
- **Qué capturar:** el panel con las métricas (Security / Reliability / Maintainability) y
  el contador de issues abiertas del análisis del código original.
- Archivo sugerido: `captura_sonarcloud_overview.png`

### 3. SonarCloud — Calidad / Quality Gate (recomendado)
- Dentro del Overview, despliega "Quality Gate" o entra a
  https://sonarcloud.io/project/quality_gate?id=bgrez-lab_gestion-productos-seguridad
- **Qué capturar:** las condiciones actuales (el gate evalúa el código nuevo; las issues del
  programa quedan abiertas como problemas pendientes).
- Archivo sugerido: `captura_quality_gate.png`

### 4. GitHub — repositorio (recomendado)
- URL: https://github.com/bgrez-lab/gestion-productos-seguridad
- **Qué capturar:** la página principal del repo con la rama `main` (código original).
- Archivo sugerido: `captura_github_repo.png`

### 5. Semgrep — terminal (opcional)
- Puedes re-ejecutar y capturar el terminal:
  ```
  semgrep scan --config auto
  ```
  *(sobre el programa original: 28 hallazgos)*

> Sugerencia: con la tecla **Impr Pant** o con **Win+Shift+S** en Windows; guarda las
> imágenes en la carpeta `evidencia/` del proyecto y súbelas como anexos en EVA.

## Cómo agregarlas al informe HTML
Deja las imágenes junto a `informe.html` (o dentro de `evidencia/`) y súbelas en EVA
en la misma entrega; el informe en Word o PDF puede incluirlas insertadas manualmente.