"""
Srcipt para la aplicación de la gestión de la tienda

Este script proporciona una API RESTFul para gesstionar productos, el carrito y visualización de estos.
Usamos JWT para proporcionarle seguridad a la aplicación Flask (identificación y autentificación)

Funciones principales de la API:
-------------------------------
-> Iniciar y cerrar sesión de usuarios
-> Gestión de usuarios
-> Gestión de productos (crear, modificar, eliminar y leer especificaciones)
-> Gestión del carrito (visualizar elementos del carrito y añadir/eliminar productos)
-> Generar facturas

Librerias:
----------
-> Flask
-> Flask_JWT_Extended

Configuraciones:
---------------
->JWT_SECRET_KEY : 'mi_clave_A4'
---------------

Para inicializar la API:

>> python api.py

"""

import os
import sqlite3
import hashlib
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, get_jwt
)
from fpdf import FPDF
from datetime import timedelta
from TTienda import Tienda
from TCarrito import Carrito
from TCliente import Cliente
from TProducto import Producto
# from TAdmin import Administrador   # Suponiendo que exista
# from TFactura import FacturaPDF   # Suponiendo que exista
# from TTienda import Tienda        # Suponiendo que exista
users = {}

ACCESS_EXPIRES = timedelta(minutes=30)  # los tokens solo tienen media hora de validez

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'mi_clave_A4'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

#------------------------------------------------------------------------------------------------------#
@app.route("/")
def principal():
    return 'API de Productos funcionando correctamente'

#-------------------------------------------------------------------------------------------------------#
@app.route('/signup', methods=['POST'])
def signup():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    if user in users:
        return f'Usuario {user} ya se encuentra registrado', 409
    else:
        hashed = hashlib.sha256(password.encode()).hexdigest()
        users[user] = hashed
        return f'Usuario {user} ha sido registrado correctamente', 200

#-------------------------------------------------------------------------------------#
@app.route('/login', methods=['GET'])
def login():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cliente = Cliente()

    if user in cliente.nombre_usuario() and cliente.password() == hashed:
        token = create_access_token(identity=user)
        return jsonify(token=token), 200
    else:
        return 'Usuario o contraseña incorrectos', 401

#-------------------------------------------------------------------------#
@jwt.token_in_blocklist_loader
def comprobar_token(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    conn = sqlite3.connect('db.sqlite3')  # Ajusta la ruta a la BD
    cursor = conn.cursor()
    cursor.execute("SELECT jti FROM token WHERE jti = ?", (jti,))
    token = cursor.fetchone()
    conn.close()
    return token is not None

#-------------------------------------------------------------------#
@app.route("/logout", methods=['DELETE'])
@jwt_required()
def cerrar_sesion():
    jti = get_jwt()['jti']
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO token (jti) VALUES (?)", (jti,))
        conn.commit()
        conn.close()
        return jsonify(msg='JWT revocado'), 200
    except sqlite3.IntegrityError:
        return 'Token ya añadido a la base de datos', 409

#----------------------------------------------------------------------#
@app.route('/carrito/add', methods=['POST'])
@jwt_required()
def añadir_producto_carrito():
    carrito = Carrito()
    producto = Producto()  # Aquí falta la lógica de creación a partir de los datos
    if producto not in carrito:
        carrito.anyadir_producto(producto)
        return f'Producto añadido al carrito', 202
    else:
        return f'Producto ya incluido en el carrito', 409

#-------------------------------------------------------------------------------#
@app.route('/carrito/delete', methods=['DELETE'])
@jwt_required()
def eliminar_producto_carrito():
    carrito = Carrito()
    producto = Producto()  # Igual, debe construirse desde los datos recibidos
    if producto in carrito:
        carrito.eliminar_producto(producto)
        return f'Producto eliminado del carrito', 202
    else:
        return f'Producto no existe en el carrito', 409

#-----------------------------------------------------------------------------------#
@app.route('/carrito', methods=['DELETE'])
@jwt_required()
def vaciar_carrito():
    carrito = Carrito()
    if carrito:
        carrito.vaciar_carrito()
        return 'Carrito vaciado', 202
    else:
        return 'El carrito ya está vacío', 409

'''

#---------------------------------------------------------------------------------------#
@app.route('/factura', methods=['GET'])
@jwt_required()
def generar_factura_producto():
    factura = FacturaPDF()
    try:
        return factura.generar(), 202
    except KeyError:
        return 'Producto no encontrado', 409

'''
#------------------------------------------------------------------------------------------#
@app.route('/tienda', methods=['POST'])
@jwt_required()
def añadir_producto_tienda():
    tienda = Tienda()
    producto = Producto()  # Debería crearse con los datos recibidos

    if producto not in tienda:
        tienda.guardar(producto, producto.precio, producto.stock)
        return 'Producto guardado correctamente', 202
    else:
        return 'El producto ya se encontraba en la tienda', 409

#------------------------------------------------------------------------------------------#
@app.route('/carrito/ver', methods=['GET'])
@jwt_required()
def ver_carrito():
    carrito = Carrito()
    return jsonify(carrito.mostrar())

#-----------------------------------------------------------------------------------------------#
@app.route('/tienda', methods=['GET'])
@jwt_required()
def mostrar_catalogo():
    tienda = Tienda()
    productos = tienda.listar_productos()
    if productos:
        return jsonify(productos), 202
    else:
        return 'La tienda está vacía', 404

#--------------------------------------------------------------------------------------------#
@app.route('/producto/reseña', methods=['POST'])
@jwt_required()
def añadir_reseña():
    producto = request.args.get('producto')
    puntuacion = request.args.get('puntuacion')
    comentario = request.args.get('comentario')
    return Producto.añadir_reseña(producto, puntuacion, comentario)

#--------------------------------------------------------------------------------------------#
@app.route('/cliente', methods=['POST'])
@jwt_required()
def recargar_saldo():
    cantidad = float(request.args.get('cantidad', 0))
    cliente = Cliente()
    cliente.recargar_saldo(cantidad)
    return 'Saldo recargado', 200

#---------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True)