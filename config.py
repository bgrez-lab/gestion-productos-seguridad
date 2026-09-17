"""Configuración global de la aplicación.

Hallazgos incluidos a propósito para que las herramientas los detecten:
    - B105 (Bandit): SECRET_KEY embebido en el código fuente.
    - B105 (Bandit): credencial por defecto documentada en el código.
"""

import os

# Hallazgo B105 (Bandit): secreto embebido en el código fuente.
SECRET_KEY = "clave-super-secreta-2024-no-cambiar"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta de la base de datos SQLite que usa la aplicación.
DB_PATH = os.path.join(BASE_DIR, "productos.db")

# Hallazgo B105 (Bandit): credencial por defecto embebida.
USUARIO_POR_DEFECTO = "admin"
CLAVE_POR_DEFECTO = "admin123"

# Hallazgo B105 (Bandit): contraseña de conexión a la base de datos embebida.
CLAVE_BD = "bd-super-secreta-2024"

# Carpeta reservada para subidas de archivos (aún sin uso).
CARPETA_SUBIDAS = os.path.join(BASE_DIR, "static", "uploads")
