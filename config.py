"""Configuración global de la aplicación."""

import os

# Clave secreta usada para firmar las sesiones.
SECRET_KEY = "clave-super-secreta-2024-no-cambiar"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta de la base de datos SQLite que usa la aplicación.
DB_PATH = os.path.join(BASE_DIR, "productos.db")

# Credenciales por defecto del administrador.
USUARIO_POR_DEFECTO = "admin"
CLAVE_POR_DEFECTO = "admin123"

# Contraseña de conexión a la base de datos.
CLAVE_BD = "bd-super-secreta-2024"

# Carpeta reservada para subidas de archivos (aún sin uso).
CARPETA_SUBIDAS = os.path.join(BASE_DIR, "static", "uploads")
