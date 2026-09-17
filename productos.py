"""Blueprint con el CRUD de productos sobre SQLite.

Correcciones aplicadas:
    - B608 (Bandit): búsqueda con LIKE parametrizado (sin concatenación).
    - W0611 (pylint): import `datetime` eliminado.
    - W0703 (pylint): se captura solo `ValueError`.
    - NaN injection: se valida que precio/stock sean finitos y positivos.
"""

import math

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import get_db

productos_bp = Blueprint("productos", __name__)


def sesion_activa():
    """Devuelve True si existe una sesión iniciada."""
    return "usuario" in session


def _validar_importes(precio_str, stock_str):
    """Convierte y valida precio/stock. Devuelve (precio, stock) o None."""
    try:
        precio = float(precio_str)
        stock = int(stock_str)
    except ValueError:
        return None
    if not (math.isfinite(precio) and precio > 0 and stock >= 0):
        return None
    return precio, stock


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
    """Busca productos por nombre usando LIKE parametrizado."""
    if not sesion_activa():
        return redirect(url_for("auth.login"))
    termino = request.args.get("q", "").strip()
    db = get_db()
    # Parámetro ? en lugar de concatenar: se elimina la inyección SQL.
    sql = "SELECT * FROM productos WHERE nombre LIKE ? ESCAPE '\\'"
    patron = (
        "%"
        + termino.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        + "%"
    )
    productos = db.execute(sql, (patron,)).fetchall()
    return render_template("listar.html", productos=productos, termino=termino)


@productos_bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    """Crea un nuevo producto."""
    if not sesion_activa():
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        if not nombre:
            flash("El nombre es obligatorio.")
            return render_template("formulario.html")
        importes = _validar_importes(
            request.form.get("precio", "0"), request.form.get("stock", "0")
        )
        if importes is None:
            flash("Precio o stock inválidos.")
            return render_template("formulario.html")
        precio, stock = importes
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
        nombre = request.form.get("nombre", "").strip()
        if not nombre:
            flash("El nombre es obligatorio.")
            return render_template("formulario.html")
        importes = _validar_importes(
            request.form.get("precio", "0"), request.form.get("stock", "0")
        )
        if importes is None:
            flash("Precio o stock inválidos.")
            return render_template("formulario.html")
        precio, stock = importes
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
