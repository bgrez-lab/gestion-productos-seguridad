"""Configuración global de la aplicación.

Corregido:
    - B105 (Bandit): la clave se lee de la variable de entorno, jamás del código.
    - Credenciales por defecto: eliminadas (el admin se crea en el primer uso).
"""

import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# La clave secreta se toma del entorno. Si no existe, se genera una
# aleatoria por sesión (solo recomendable para desarrollo).
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

# Ruta de la base de datos SQLite que usa la aplicación.
DB_PATH = os.path.join(BASE_DIR, "productos.db")

# True solo si la variable de entorno lo indica (nunca en producción).
DEBUG = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
