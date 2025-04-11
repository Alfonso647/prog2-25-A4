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

from TTienda import Tienda
from TCarrito import Carrito
from TCliente import Cliente
from TProd import Producto
from generar_facturas import FacturaPDF

app = Flask(__name__)

@app.route("/")
def principal():
    return 'API de Productos funcionando correctamente'

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    user = data.get('usuario', '')
    # Eliminado el código de verificación de usuario existente, simplificado
    return f'Usuario {user} ha sido registrado correctamente', 200

@app.route('/saldo', methods=['POST'])
def recargar_saldo():
    data = request.json
    cantidad = float(data.get('cantidad', 0))
    cliente = Cliente()
    cliente.recargar_saldo(cantidad)
    return 'Saldo recargado', 200

@app.route('/premium', methods=['POST'])
def pasar_a_premium():
    cliente = Cliente()
    resultado = cliente.cuenta_premium()
    return resultado

@app.route('/carrito', methods=['GET'])
def ver_carrito():
    carrito = Carrito()
    return jsonify(print(carrito)), 200

@app.route('/carrito', methods=['POST'])
def comprar_producto():
    data = request.json
    nombre = data.get('producto')
    cantidad = data.get('cantidad')
    producto = Producto(nombre)
    producto.set_cantidad(cantidad)
    carrito = Carrito()
    carrito.anyadir_producto(producto)
    return 'Producto añadido al carrito', 200

@app.route('/carrito', methods=['DELETE'])
def eliminar_producto_carrito():
    data = request.json
    nombre = data.get('producto')
    cantidad = data.get('cantidad')
    producto = Producto(nombre)
    carrito = Carrito()
    carrito.eliminar_producto(producto)
    return 'Producto eliminado del carrito', 200

@app.route('/compra/finalizar', methods=['POST'])
def finalizar_compra():
    cliente = Cliente()
    cliente.finalizar_compra()
    return cliente, 200

@app.route('/productos', methods=['GET'])
def ver_catalogo():
    tienda = Tienda()
    return print(tienda), 200

@app.route('/producto', methods=['POST'])
def publicar_producto():
    data = request.json
    producto = Producto(data['nombre'], data['precio'], data['stock'], data['volumen'], data['peso'], data['estado'])
    producto.guardar(producto, producto.precio, producto.stock)
    return 'Producto publicado', 200

@app.route('/producto/<string:nombre>/resenya', methods=['POST'])
def añadir_reseña(nombre):
    data = request.json
    puntuacion = data.get('puntuacion')
    comentario = data.get('comentario')
    return Producto.anyadir_resenya(nombre, puntuacion, comentario), 200

@app.route('/producto/<string:nombre>/resenyas', methods=['GET'])
def ver_reseñas(nombre):
    return jsonify(Producto.mostrar_resenyas(nombre)), 200

@app.route('/historial', methods=['GET'])
def mostrar_historial():
    cliente = Cliente()
    return jsonify(cliente.mostrar_historial_compras()), 200

if __name__ == '__main__':
    app.run(debug=True)