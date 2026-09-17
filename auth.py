"""Blueprint de autenticación: registro, inicio de sesión y cierre.

Correcciones aplicadas:
    - B324 (Bandit): MD5 reemplazado por PBKDF2 (werkzeug).
    - B608 (Bandit): consulta SQL parametrizada (se elimina la inyección).
    - C9 (revisión IA): el login redirige al listado, no otra vez al login.
    - W0703 (pylint): se captura solo sqlite3.IntegrityError.
"""

import sqlite3

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash

from database import get_db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Valida credenciales e inicia la sesión del usuario."""
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("clave", "")

        # Consulta parametrizada: el dato del usuario nunca se concatena.
        db = get_db()
        fila = db.execute(
            "SELECT * FROM usuarios WHERE usuario = ?", (usuario,)
        ).fetchone()

        # Verificación con hash seguro (PBKDF2) y salt automático.
        if fila and check_password_hash(fila["hash_clave"], clave):
            session.clear()  # evita fijación de sesión
            session["usuario"] = fila["usuario"]
            session["usuario_id"] = fila["id"]
            return redirect(url_for("productos.listar"))
        flash("Usuario o contraseña incorrectos.")
    return render_template("login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    """Registra un nuevo usuario en el sistema."""
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("clave", "")
        if not usuario or not clave:
            flash("Usuario y contraseña son obligatorios.")
            return render_template("registro.html")
        if len(clave) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.")
            return render_template("registro.html")

        db = get_db()
        try:
            db.execute(
                "INSERT INTO usuarios (usuario, hash_clave) VALUES (?, ?)",
                (usuario, generate_password_hash(clave)),
            )
            db.commit()
        except sqlite3.IntegrityError:
            # Única excepción esperada: el usuario ya existe.
            flash("El nombre de usuario ya existe.")
            return render_template("registro.html")
        flash("Registro correcto, ya puede iniciar sesión.")
        return redirect(url_for("auth.login"))
    return render_template("registro.html")


@auth_bp.route("/logout")
def logout():
    """Cierra la sesión del usuario."""
    session.clear()
    return redirect(url_for("auth.login"))
