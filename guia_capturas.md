# Guía de capturas de pantalla (evidencia)

> **ACTUALIZADO:** el archivo `informe_capturas.docx` ya incluye las 8 capturas embebidas
> (generadas a partir de los datos reales de la API de SonarCloud y de los reportes
> exportados: dashboard, issues cerradas, Semgrep antes/después, Bandit antes/después,
> Pylint y repositorio GitHub). **No es obligatorio tomar capturas a mano.**

Si aun así quieres adjuntar las capturas reales del navegador (recomendado como anexo
adicional), puedes hacerlo siguiendo el listado de abajo y guardarlas en `evidencia/capturas/`
reemplazando las imágenes existentes con el mismo nombre; luego vuelve a ejecutar el
generador del Word:
`.\.venv\Scripts\python.exe C:\Users\palom\AppData\Local\Temp\opencode\generar_docx.py`

Adjunta estas capturas en EVA / en el informe. Cada una muestra un resultado real de
las herramientas sobre TU código.

### 1. SonarCloud — Overview del proyecto (obligatorio)
- URL: https://sonarcloud.io/project/overview?id=bgrez-lab_gestion-productos-seguridad
- **Qué capturar:** el panel con Security / Reliability / Maintainability, el recuadro
  "Quality Gate" (debe decir **Passed**) y la línea duplications.
- Archivo sugerido: `captura_sonarcloud_overview.png`

### 2. SonarCloud — Issues (obligatorio)
- URL: https://sonarcloud.io/project/issues?id=bgrez-lab_gestion-productos-seguridad&resolved=false
- **Qué capturar:** la lista de issues (debe estar vacía tras corregir, o bien un issue
  abierto con su detalle). Si quieres la versión "antes", filtra por `resolved=true`.
- Archivo sugerido: `captura_sonarcloud_issues.png`

### 3. SonarCloud — Quality Gate (recomendado)
- Dentro del Overview, despliega "Quality Gate" o entra a
  https://sonarcloud.io/project/quality_gate?id=bgrez-lab_gestion-productos-seguridad
- Archivo sugerido: `captura_quality_gate.png`

### 4. GitHub — repositorio (recomendado)
- URL: https://github.com/bgrez-lab/gestion-productos-seguridad
- **Qué capturar:** la página principal del repo (commit log con 5 commits).
- Archivo sugerido: `captura_github_repo.png`

### 5. SonarCloud — pestaña Security Hotspots (opcional)
- Muestra que no quedaron "security hotspots" sin revisar.

### 6. Semgrep — terminal (opcional)
- Puedes re-ejecutar y capturar el terminal:
  ```
  semgrep scan --config auto
  ```
  *(con el código corregido: 4 findings, todos falsos positivos)*

> Sugerencia: con la tecla **Impr Pant** o con **Win+Shift+S** en Windows; guarda las
> imágenes en la carpeta `evidencia/` del proyecto y súbelas como anexos en EVA.

## Cómo agregarlas al informe HTML
Deja las imágenes junto a `informe.html` (o dentro de `evidencia/`) y súbelas en EVA
en la misma entrega; el informe en Word o PDF puede incluirlas insertadas manualmente.