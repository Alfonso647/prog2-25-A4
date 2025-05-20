from flask import Blueprint, render_template, session, flash, redirect, url_for
from flask_login import login_required, current_user
from website.productos_db import Producto2
from TCarrito import Carrito


views = Blueprint('views',__name__)

def obtener_carrito():
    """
    Esta función te devuelve el carrito ACTUAL. Para usar la clase carrito con flask
    tenemos que guardar la información del carrito (__dict__) en la sesión actual
    Si lo hicieramos directamente, creariamos un carrito nuevo y no recuperaríamos
    el que estaba anteriomente.

    """
    if 'carrito' not in session:
        session['carrito'] = Carrito().__dict__
    carrito = Carrito()
    carrito.__dict__ = session['carrito']
    return carrito

def guardar_carrito(carrito):
    session['carrito'] = carrito.productos

@views.route('/')
@login_required
def home():
    productos = Producto2.query.all()
    return render_template("home.html", user = current_user, productos=productos)

@views.route('/producto/<int:producto_id>')
def producto_detalle(producto_id):
    producto = Producto2.query.get_or_404(producto_id)
    return render_template('producto_detalle.html', producto=producto)

@views.route('/anadir_carrito/<int:producto_id>', methods=['POST'])
@login_required
def anadir_carrito(producto_id):
    producto = Producto2.query.get(producto_id)
    if not producto:
        flash('Producto no encontrado.', category='error')
        return redirect(url_for('views.home'))

    carrito = obtener_carrito()
    carrito.anyadir_producto(producto_id)
    guardar_carrito(carrito)

    flash(f'{producto.nombre} añadido al carrito.', category='success')
    return redirect(url_for('views.mostrar_carrito'))

@views.route('/carrito')
@login_required
def mostrar_carrito():
    carrito = obtener_carrito()
    productos_carrito = []

    for prod_id, cantidad in carrito.mostrar().items():
        producto = Producto2.query.get(int(prod_id))
        if producto:
            productos_carrito.append({'producto': producto, 'cantidad': cantidad})

    return render_template("carrito.html", user=current_user, productos=productos_carrito)