"""Punto de entrada de la aplicación Flask.

Levanta el servidor, inicializa la base de datos y registra los
blueprints de autenticación y de CRUD de productos.
"""

from flask import Flask, redirect, session, url_for

from config import SECRET_KEY
from database import close_db, init_db
from auth import auth_bp
from productos import productos_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(productos_bp)

app.teardown_appcontext(close_db)


@app.route("/")
def index():
    """Redirige a la lista de productos si hay sesión activa, o al login."""
    if "usuario" in session:
        return redirect(url_for("productos.listar"))
    return redirect(url_for("auth.login"))


@app.route("/logout")
def logout():
    """Cierra la sesión del usuario actual."""
    session.clear()
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
