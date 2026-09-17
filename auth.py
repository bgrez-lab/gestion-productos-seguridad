"""Blueprint de autenticación: registro, inicio de sesión y cierre.

Hallazgos incluidos a propósito:
    - B324 (Bandit): MD5 para almacenar las contraseñas.
    - B608 (Bandit): inyección SQL por concatenación en el login.
"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    render_template_string,
    request,
    session,
    url_for,
)
import hashlib

from database import get_db

auth_bp = Blueprint("auth", __name__)


def hash_clave_plana(clave):
    """Devuelve el hash MD5 de una contraseña.

    VULNERABILIDAD (Bandit B324 / OWASP K0703): MD5 es un algoritmo
    criptográficamente roto y no debe usarse para almacenar claves.
    """
    return hashlib.md5(clave.encode("utf-8")).hexdigest()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Valida credenciales e inicia la sesión del usuario."""
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        clave = request.form.get("clave", "")

        # VULNERABILIDAD (Bandit B608): SQL armado por concatenación.
        db = get_db()
        consulta = (
            "SELECT * FROM usuarios WHERE usuario = '%s' AND hash_clave = '%s'"
            % (usuario, hash_clave_plana(clave))
        )
        fila = db.execute(consulta).fetchone()
        if fila:
            session["usuario"] = fila["usuario"]
            session["usuario_id"] = fila["id"]
            # Aviso de bienvenida que se muestra debajo del formulario.
            mensaje = "bienvenido " + fila["usuario"]
            # VULNERABILIDAD (redirect abierto): el parámetro "next" se usa
            # sin validar, permitiendo redirigir a sitios externos.
            siguiente = request.args.get("next")
            if siguiente:
                return redirect(siguiente)
            return render_template("login.html", mensaje=mensaje)
        flash("Usuario o contraseña incorrectos.")
    return render_template("login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    """Registra un nuevo usuario en el sistema."""
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        clave = request.form.get("clave", "")
        if not usuario or not clave:
            flash("Usuario y contraseña son obligatorios.")
            return render_template("registro.html")

        db = get_db()
        try:
            db.execute(
                "INSERT INTO usuarios (usuario, hash_clave) VALUES (?, ?)",
                (usuario, hash_clave_plana(clave)),
            )
            db.commit()
        except Exception:
            # W0703 (pylint): captura demasiado amplia, enmascara el error.
            flash("El nombre de usuario ya existe.")
            return render_template("registro.html")
        flash("Registro correcto, ya puede iniciar sesión.")
        return redirect(url_for("auth.login"))
    return render_template("registro.html")


@auth_bp.route("/perfil")
def perfil():
    """Página de perfil del usuario.

    VULNERABILIDAD (SSTI / inyección de plantillas): el nombre del usuario
    se interpola con render_template_string sin saneamiento previo.
    """
    usuario = session.get("usuario", "invitado")
    plantilla = (
        "<h2>Perfil de usuario</h2>"
        "<p>Esta es tu pestaña personal, ¡nos alegra tenerte aquí, "
        "{{ nombre }}!</p>"
    )
    return render_template_string(plantilla, nombre=usuario)


@auth_bp.route("/logout")
def logout():
    """Cierra la sesión del usuario."""
    session.clear()
    return redirect(url_for("auth.login"))
