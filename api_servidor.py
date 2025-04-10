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
from datetime import timedelta

from TTienda import Tienda
from TCarrito import Carrito
from TCliente import Cliente
from TProd import Producto
from generar_facturas import FacturaPDF

users = {}
ACCESS_EXPIRES = timedelta(minutes=30)

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'mi_clave_A4'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

@app.route("/")
def principal():
    return 'API de Productos funcionando correctamente'

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    user = data.get('usuario', '')
    if user in users:
        return f'Usuario {user} ya se encuentra registrado', 409
    hashed = hashlib.sha256(user.encode()).hexdigest()
    users[user] = hashed
    return f'Usuario {user} ha sido registrado correctamente', 200

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = data.get('usuario', '')
    password = hashlib.sha256(user.encode()).hexdigest()
    cliente = Cliente()
    if user in cliente.nombre_usuario() and cliente.password() == password:
        token = create_access_token(identity=user)
        return jsonify(token=token), 200
    return 'Usuario o contraseña incorrectos', 401

@jwt.token_in_blocklist_loader
def comprobar_token(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT jti FROM token WHERE jti = ?", (jti,))
    token = cursor.fetchone()
    conn.close()
    return token is not None

@app.route("/logout", methods=['DELETE'])
@jwt_required()
def cerrar_sesion():
    jti = get_jwt()['jti']
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO token (jti) VALUES (?)", (jti,))
    conn.commit()
    conn.close()
    return jsonify(msg='JWT revocado'), 200

@app.route('/saldo', methods=['POST'])
@jwt_required()
def recargar_saldo():
    data = request.json
    cantidad = float(data.get('cantidad', 0))
    cliente = Cliente()
    cliente.recargar_saldo(cantidad)
    return 'Saldo recargado', 200

@app.route('/premium', methods=['POST'])
@jwt_required()
def pasar_a_premium():
    cliente = Cliente()
    resultado = cliente.cuenta_premium()
    return resultado

@app.route('/carrito', methods=['GET'])
@jwt_required()
def ver_carrito():
    carrito = Carrito()
    return jsonify(carrito.mostrar()), 200

@app.route('/carrito', methods=['POST'])
@jwt_required()
def comprar_producto():
    data = request.json
    nombre = data.get('producto')
    cantidad = data.get('cantidad')
    producto = Prod(nombre)
    producto.set_cantidad(cantidad)
    carrito = Carrito()
    carrito.anyadir_producto(producto)
    return 'Producto añadido al carrito', 200

@app.route('/carrito', methods=['DELETE'])
@jwt_required()
def eliminar_producto_carrito():
    data = request.json
    nombre = data.get('producto')
    cantidad = data.get('cantidad')
    producto = Prod(nombre)
    producto.set_cantidad(cantidad)
    carrito = Carrito()
    carrito.eliminar_producto(producto)
    return 'Producto eliminado del carrito', 200

@app.route('/compra/finalizar', methods=['POST'])
@jwt_required()
def finalizar_compra():
    cliente = Cliente()
    cliente.finalizar_compra()
    return cliente, 200

@app.route('/productos', methods=['GET'])
@jwt_required()
def ver_catalogo():
    tienda = Tienda()
    return print(tienda), 200

@app.route('/producto', methods=['POST'])
@jwt_required()
def publicar_producto():
    data = request.json
    producto = Prod(data['nombre'], data['precio'], data['stock'], data['volumen'], data['peso'], data['estado'])
    producto = Producto()
    producto.guardar(producto, producto.precio, producto.stock)
    return 'Producto publicado', 200

@app.route('/producto/<string:nombre>/resenya', methods=['POST'])
@jwt_required()
def añadir_reseña(nombre):
    data = request.json
    puntuacion = data.get('puntuacion')
    comentario = data.get('comentario')
    return Producto.anyadir_resenya(nombre, puntuacion, comentario), 200

@app.route('/producto/<string:nombre>/resenyas', methods=['GET'])
def ver_reseñas(nombre):
    return jsonify(Producto.mostrar_resenyas(nombre)), 200

@app.route('/historial', methods=['GET'])
@jwt_required()
def mostrar_historial():
    cliente = Cliente()
    return jsonify(cliente.mostrar_historial_compras()), 200

if __name__ == '__main__':
    app.run(debug=True)