"""Blueprint con el CRUD de productos sobre SQLite.

Hallazgos incluidos a propósito para que las herramientas los detecten:
    - B608 (Bandit): inyección SQL en la búsqueda por concatenación.
    - W0611 (pylint): import sin uso (datetime).
    - W0703 (pylint): captura de excepción demasiado genérica en crear()/editar().
"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import datetime  # W0611 (pylint): import declarado pero nunca utilizado.

from database import get_db

productos_bp = Blueprint("productos", __name__)


def sesion_activa():
    """Devuelve True si existe una sesión iniciada."""
    return "usuario" in session


@productos_bp.route("/")
def listar():
    """Lista todos los productos del catálogo."""
    if not sesion_activa():
        return redirect(url_for("auth.login"))
    db = get_db()
    productos = db.execute("SELECT * FROM productos").fetchall()
    return render_template("listar.html", productos=productos)


@productos_bp.route("/buscar")
def buscar():
    """Busca productos por nombre.

    VULNERABILIDAD (Bandit B608): el término se concatena directamente en
    la consulta SQL. Payload de ejemplo:  x' OR '1'='1
    """
    if not sesion_activa():
        return redirect(url_for("auth.login"))
    termino = request.args.get("q", "")
    db = get_db()
    sql = "SELECT * FROM productos WHERE nombre LIKE '%" + termino + "%'"
    productos = db.execute(sql).fetchall()
    return render_template("listar.html", productos=productos, termino=termino)


@productos_bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    """Crea un nuevo producto."""
    if not sesion_activa():
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        nombre = request.form.get("nombre", "")
        try:
            precio = float(request.form.get("precio", "0"))
            stock = int(request.form.get("stock", "0"))
        except Exception:
            # W0703 (pylint): captura demasiado amplia, enmascara el error.
            flash("Precio o stock inválidos.")
            return render_template("formulario.html")
        db = get_db()
        db.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            (nombre, precio, stock),
        )
        db.commit()
        return redirect(url_for("productos.listar"))
    return render_template("formulario.html")


@productos_bp.route("/<int:producto_id>/editar", methods=["GET", "POST"])
def editar(producto_id):
    """Edita un producto existente."""
    if not sesion_activa():
        return redirect(url_for("auth.login"))
    db = get_db()
    if request.method == "POST":
        nombre = request.form.get("nombre", "")
        try:
            precio = float(request.form.get("precio", "0"))
            stock = int(request.form.get("stock", "0"))
        except Exception:
            # W0703 (pylint): captura demasiado amplia.
            flash("Precio o stock inválidos.")
            return render_template("formulario.html")
        db.execute(
            "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
            (nombre, precio, stock, producto_id),
        )
        db.commit()
        return redirect(url_for("productos.listar"))
    producto = db.execute(
        "SELECT * FROM productos WHERE id = ?", (producto_id,)
    ).fetchone()
    return render_template("formulario.html", producto=producto)


@productos_bp.route("/<int:producto_id>/eliminar", methods=["POST"])
def eliminar(producto_id):
    """Elimina un producto por su identificador."""
    if not sesion_activa():
        return redirect(url_for("auth.login"))
    db = get_db()
    db.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    db.commit()
    return redirect(url_for("productos.listar"))
