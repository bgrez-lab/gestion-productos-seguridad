"""Capa de acceso a datos sobre SQLite.

Provee la conexión (reutilizada por request vía Flask ``g``), su cierre
y la inicialización del esquema con datos de ejemplo.

Hallazgos incluidos a propósito:
    - B324 (Bandit): uso de MD5 para sembrar la contraseña del admin.
"""

import hashlib
import sqlite3

from flask import g

from config import DB_PATH


def get_db():
    """Devuelve una conexión a SQLite reutilizada dentro de la request."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exc=None):
    """Cierra la conexión a la base de datos al finalizar la request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Crea las tablas si no existen y agrega datos de ejemplo.

    VULNERABILIDAD / Hallazgo B324 (Bandit), K0703 (OWASP): la clave del
    admin se siembra con MD5, algoritmo criptográficamente roto.
    """
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            hash_clave TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    cur = db.cursor()
    if cur.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0] == 0:
        # B324 (Bandit): MD5 prohibido para almacenar contraseñas.
        db.execute(
            "INSERT INTO usuarios (usuario, hash_clave) VALUES (?, ?)",
            ("admin", hashlib.md5(b"admin123").hexdigest()),
        )
    if cur.execute("SELECT COUNT(*) FROM productos").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            [
                ("Laptop Dell 15", 1249.99, 8),
                ("Mouse inalámbrico", 29.90, 30),
                ("Teclado mecánico", 89.00, 20),
                ("Monitor 24 pulgadas", 209.99, 12),
            ],
        )
    db.commit()
    db.close()
