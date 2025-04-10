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
->JWT_SECRET_KEY : A4
---------------

Para incializar la API:

>> python api.py

"""

from TProd import Producto
from generar_facturas import FacturaPDF
from TTienda import Tienda
from TCliente import Cliente, Administrador
from TCarrito import Carrito
from fpdf import FPDF

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
import hashlib

ACCESS_EXPIRES = timedelta(hours=0.30)   #los token solo tienen media hora de validez
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'mi_clave_A4'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)
users = {}

@app.route("/")
def principal():
    return 'Api de Productos funcionando correctmente'

@app.route('/singup', methods=['POST'])
#@jwt_required : no es necesario seguridad para crear una nueva cuenta
def singup():
    """
    Esta funcionalidad crea una nueva cuenta: nuevo usuario con su contraseña

    Toma los parámetros 'user' desde los argumentos de la petición (request.args).
    Comprueba que el parámetro 'user' no esté en la lista de usuarios de la app. Si el
    user no es existente, crea una contraseña con el parámetro 'password' de la petición
    (request.args), la codifica y la guarda en el usuario correspondiente.

    :return:

    -> Si el usuario ya esta registrado, devuelve mensaje de error (409)
    -> Si el usuario se ha registrado correctamente, devuelve la confirmación (200)
    """
    user = request.args.get('user', '')
    if user in users:
        return f'Usuario {user} ya se encuentra registrado', 409
    else:
        password = request.args.get('password','')
        hashed = hash.lib.sha256(password.encode()).hexdigest()
        users[user] = hashed
        return f'Usuario {user} ha sido registrado correctamente', 200

@app.route('/login', methods=['GET']) #inicio sesión
def login():
    """
    Inicia sesión de un usuario y genera su token (valido por media hora)

    Obtiene los paráḿetros 'user', 'password' de la petición (request.args).
    Después, decodifica la constraseña (parámetro 'password'). Una vez que
    se tiene la identificación del usuario, se comorueba si se comprueba que es
    correcta. Si las creedenciales son correctas, se genera un token y el
    código de estado 200. En el caso contrario, devuelve un mensaje de error
    junto con el código de estado 404

    :return:

    -> Identificación válida: token JWT + el código de estado 200
    -> Identificación no válida: mensaje error + el código de error 404

    """
    user = request.args.get('user','')
    password = request.args.get('password','')
    hashed = hashlib.sha256(password.encode()).hexdigest()
    credenciales = Cliente()
    nombre_usuario = credenciales.nombre_usuario()
    if user in nombre_usuario and credenciales.password() == hashed:
        return create_access_token(identity=nombre_usuario), 200
    else:
        return  f'Usuario o contraseña incorrectos', 401

#@app.route('/users', methods=['POST'])
#@jwt_required()
#def añadir_usuario():
#    """
#
#    Comprubea si eres administrador y añade un nuevo usuario al sistema.
#
#    Lee los datos del usuario para comprobar si es administrador (desde la petición
#    request.args : nombre, apellido1, apellido2, nombre_usuario, password). Si es un
#    administrador, este podrá crear un nuevo usuario (codigo 200) y si no lo és, no
#    podrá hacerlo (404)
#
#    :return:
#
#     -> Si se crea un usuario nuevo: código de estado 202
#     -> Si el usuario no es un administrador: código de estado 404
#     -> Si el usuario que se intenta crear ya está registrado: código de error 409
#    """
#
#    usuario = get_jwt_identity()
#    user = Administrador()
#    if not isinstance(user.nombre_usuario, Administrador):  #REVISAR
#        return f'Solo los adminsitradores pueden realizar crear usuarios', 404
#    nombre = request.args.get('nombre')
#    apellido1 = request.args.get('apellido1')
#    apellido2 = request.args.get('apellido2')
#    password = request.args.get('password')
#    admin = request.args.get('administrador', 'no')

#    if administrador == 'si':
#        if usuario == '0':
#            ##hace una falta una clase que pueda añadir usuarios
#    #etc


@app.route('/carrito/add', methods=['POST'])   #añadir productos al carrito
@jwt_required() #solo los usuarios registrados pueden hacerlo
def añadir_producto_carrito():
    """
    Añade un nuevo producto al carrito. Solo los usuarios que hayan iniciado sesión pueden
    realizar esta acción

    Comprueba que el hay un usuario que ha iniciado sesión. Obtiene la informaión del
    producto (nombre, precio, stock, volumen, peso, frágil)

    :param producto:

    :return:

    -> Si el producto se ha añadido correctamente: 202
    -> Si el producto ya estaba en el carrito: 409
    """
    carrito = Carrito()
    producto = Producto()
    if producto not in carrito:
        carrito[producto] = request.args.get('value','')
        carrito.anyadir_producto(producto)
        return f'Producto: {producto} añadido', 200
    else:
        return f'Prodcuto: {producto} ya incluido', 409


@app.route('/carrito/delete', methods=['POST'])  #eliminar productos del carrito
@jwt_required()  # solo los usuarios registrados pueden hacerlo
def eliminar_producto_carrito():
    """
    Elimina un producto del carrito. Solo los usuarios que hayan iniciado sesión pueden
    realizar esta acción

    Comprueba que el hay un usuario que ha iniciado sesión. Obtiene la informaión del
    producto (nombre, precio, stock, volumen, peso, frágil)

    :param producto:

    :return:

    -> Si el producto se ha eliminado correctamente: 202
    -> Si el producto no estaba en el carrito: 409
    """
    carrito = Carrito()
    producto = Producto()
    if producto in carrito:
        carrito[producto] = request.args.get('value', '')
        carrito.eliminar_producto(producto)
        return f'Producto: {producto} eliminado del carrito', 200
    else:
        return f'Producto: {producto} no está en el carrito', 409


@app.route('/carrito', methods=['DELETE'])  #vaciar el carrito
@jwt_required()  # solo los usuarios registrados pueden hacerlo
def vaciar_carrito():
    """
    Vacía completamente el carrito. Solo los usuarios que hayan iniciado sesión pueden
    realizar esta acción

    Comprueba que el hay un usuario que ha iniciado sesión y obtiene la
    inforomación del carrito

    :param producto:

    :return:

    -> Si el producto se ha vaciado correctamente: 202
    -> Si el carrito ya estaba vacio: 409

    """
    carrito = Carrito()
    if carrito is not None:
        carrito = request.args.get('value', '')
        carrito.vaciar_carrito(producto)
        return f'Carrito vaciado: {carrito}', 200
    else:
        return f'Tu carrito ya se está vacio: {carrito}', 409


@app.route('/producto', methods=['GET'])  #genera factura producto
def generar_factura_producto(producto):
    """
    Genera una factura del producto. Solo los usuarios que hayan iniciado sesión pueden
    realizar esta acción

    Comprueba que el usuario que ha iniciado sesión. Obtiene la informaión del
    producto (nombre, precio, stock, volumen, peso, frágil)

    :param producto:

    :return:

    -> Si la factura se ha generado exitosamente: 202
    -> Si no se ha encontrado el producto: 409
    """
    factura = FacturaPDF()
    producto = Producto()
    try:
        return factura.generar()
    except KeyError:
        return f'Producto no ecnonctrado'



@app.route('/tienda', methods = ['POST'])
@jwt_required()
def añadir_producto_tienda():
    """
    Añade producto a la tienda.

    :return:
    """
    tienda = Tienda()
    producto = Producto

    if producto not in tienda:
        return producto.guardar(producto, producto.productos_precio, producto.productos_stock), 202

    else:
        return f'El producto ya se encontraba en la tienda', 409


if __name__ == '__main__':
    app.run(debug=True)