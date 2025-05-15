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

from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from TCliente import Cliente
from TCarrito import Carrito
from TProd import Producto
from TTienda import Tienda
from generar_facturas import FacturaPDF

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "mi_clave_A4"
jwt = JWTManager(app)


@app.route("/")
def principal():
    return 'API de Productos funcionando correctamente'


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('usuario')
    password = data.get('contrasena')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    if Cliente.cargar(username):
        return jsonify({"error": "Usuario ya existe"}), 409

    nuevo = Cliente(nombre=username, contrasena=password)
    nuevo.guardar()
    return jsonify({"msg": f"Usuario {username} registrado correctamente"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('usuario')
    password = data.get('contrasena')

    cliente = Cliente.autenticar(username, password)
    if not cliente:
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


@app.route('/saldo', methods=['POST'])
@jwt_required()
def recargar_saldo():
    data = request.json
    cantidad = float(data.get('cantidad', 0))
    username = get_jwt_identity()
    cliente = Cliente.cargar(username)
    cliente.recargar_saldo(cantidad)
    return jsonify({"msg": "Saldo recargado"}), 200


@app.route('/premium', methods=['POST'])
@jwt_required()
def pasar_a_premium():
    username = get_jwt_identity()
    cliente = Cliente.cargar(username)
    resultado = cliente.cuenta_premium()
    return jsonify({"msg": resultado})


@app.route('/carrito', methods=['GET'])
@jwt_required()
def ver_carrito():
    username = get_jwt_identity()
    cliente = Cliente.cargar(username)
    carrito = cliente.carrito
    return jsonify(carrito.mostrar_productos())


@app.route('/carrito', methods=['POST'])
@jwt_required()
def comprar_producto():
    data = request.json
    nombre = data.get('producto')
    cantidad = data.get('cantidad')
    username = get_jwt_identity()

    cliente = Cliente.cargar(username)
    producto = Producto(nombre)
    producto.set_cantidad(cantidad)
    cliente.carrito.anyadir_producto(producto)
    return jsonify({"msg": "Producto añadido al carrito"}), 200


@app.route('/carrito', methods=['DELETE'])
@jwt_required()
def eliminar_producto_carrito():
    data = request.json
    nombre = data.get('producto')
    username = get_jwt_identity()

    cliente = Cliente.cargar(username)
    producto = Producto(nombre)
    cliente.carrito.eliminar_producto(producto)
    return jsonify({"msg": "Producto eliminado del carrito"}), 200


@app.route('/compra/finalizar', methods=['POST'])
@jwt_required()
def finalizar_compra():
    username = get_jwt_identity()
    cliente = Cliente.cargar(username)
    cliente.finalizar_compra()
    return jsonify({"msg": "Compra finalizada"}), 200


@app.route('/productos', methods=['GET'])
def ver_catalogo():
    tienda = Tienda()
    return jsonify(tienda.mostrar_productos())


@app.route('/producto', methods=['POST'])
@jwt_required()
def publicar_producto():
    data = request.json
    producto = Producto(
        data['nombre'], data['precio'], data['stock'],
        data['volumen'], data['peso'], data['estado']
    )
    producto.guardar(producto.precio, producto.stock)
    return jsonify({"msg": "Producto publicado"}), 201


@app.route('/producto/<string:nombre>/resenya', methods=['POST'])
@jwt_required()
def añadir_reseña(nombre):
    data = request.json
    puntuacion = data.get('puntuacion')
    comentario = data.get('comentario')
    Producto.anyadir_resenya(nombre, puntuacion, comentario)
    return jsonify({"msg": "Reseña añadida"}), 200


@app.route('/producto/<string:nombre>/resenyas', methods=['GET'])
def ver_reseñas(nombre):
    return jsonify(Producto.mostrar_resenyas(nombre)), 200


@app.route('/historial', methods=['GET'])
@jwt_required()
def mostrar_historial():
    username = get_jwt_identity()
    cliente = Cliente.cargar(username)
    return jsonify(cliente.mostrar_historial_compras()), 200


if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)