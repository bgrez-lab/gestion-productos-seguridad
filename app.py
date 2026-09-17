"""Punto de entrada de la aplicación Flask.

Levanta el servidor, inicializa la base de datos y registra los
blueprints de autenticación y de CRUD de productos.

Correcciones aplicadas:
    - B201 (Bandit) / S4507 (Sonar): debug solo con FLASK_DEBUG=1.
    - S8392 (Sonar): host 127.0.0.1 (no expone el servidor).
    - S4502 (Sonar): protección CSRF global con Flask-WTF.
"""

from flask import Flask, redirect, session, url_for
from flask_wtf import CSRFProtect

from config import DEBUG, SECRET_KEY
from database import close_db, init_db
from auth import auth_bp
from productos import productos_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# Protección CSRF obligatoria en todo formulario POST.
csrf = CSRFProtect(app)

app.register_blueprint(auth_bp)
app.register_blueprint(productos_bp)

app.teardown_appcontext(close_db)


@app.route("/")
def index():
    """Redirige a la lista de productos si hay sesión activa, o al login."""
    if "usuario" in session:
        return redirect(url_for("productos.listar"))
    return redirect(url_for("auth.login"))


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=DEBUG)
