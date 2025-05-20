from flask import Blueprint, render_template
from flask_login import login_required, current_user

from website.productos_db import Producto2

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    productos = Producto2.query.all()
    return render_template("home.html", user = current_user, productos=productos)

@views.route('/producto/<int:producto_id>')
def producto_detalle(producto_id):
    producto = Producto2.query.get_or_404(producto_id)
    return render_template('producto_detalle.html', producto=producto)

@views.route('/carrito')
@login_required
def mostrar_carrito():
    return render_template("home.html", user = current_user)