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
from crypt import methods
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from config import JWT_SECRET_KEY
from fpdf import FPDF

from TCarrito import Carrito
from TCliente import Cliente, Administrador
from TProd import Producto
from generar_facturas import FacturaPDF

ACCESS_EXPIRES = timedelta(hours=0.30)   #los token solo tienen media hora de validez
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'mi_clave_A4'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

#------------------------------------------------------------------------------------------------------#
@app.route("/")
def principal():
    return 'Api de Productos funcionando correctmente'
#-------------------------------------------------------------------------------------------------------#
@app.route('/singup', methods=['POST'])
#@jwt_required : no es necesario seguridad para crear una nueva cuenta
def singup(user,password):
    """
    Esta funcionalidad crea una nueva cuenta: nuevo usuario con su contraseña

    Toma los parámetros 'user' desde los argumentos de la petición (request.args).
    Comprueba que el parámetro 'user' no esté en la lista de usuarios de la app. Si el
    user ya es existente, crea una contraseña con el parámetro 'password' de la petición
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

#-------------------------------------------------------------------------------------#

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

#-------------------------------------------------------------------------#

#@app.route('/users', methods=['POST'])
#@jwt_required()
#def añadir_usuario():
#    """
#    Comprubea si eres administrador y añade un nuevo usuario al sistema.
#
#    Lee los datos del usuario para comprobar si es administrador (desde la petición
#    request.args : nombre, apellido1, apellido2, nombre_usuario, password). Si es un
#    administrador, este podrá crear un nuevo usuario (codigo 200) y si no lo és, no
##    podrá hacerlo (404)
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
#    if not isinstance(user.nombre_usuario, Administrador):   ####REVISAR####
#        return f'Solo los adminsitradores pueden realizar crear usuarios', 404
#    nombre = request.args.get('nombre')
#    apellido1 = request.args.get('apellido1')
#    apellido2 = request.args.get('apellido2')
#    password = request.args.get('password')
#    admin = request.args.get('administrador', 'no')
#
#    if administrador == 'si':
#        if usuario == '0':
#            ##hace una falta una clase que pueda añadir usuarios
#    #etc

#----------------------------------------------------------------------#

@jwt.token_in_blocklist_loader()
def comprobar_token():
    """
    Comprueba si el token ha sido eliminado

    :return:

    ->
    ->

    """

    jti = jwt_payload['jti']
    conn = sqlite3.connect((PATH_DB))
    cursor = conn.cursor()
    cursor.execute("Select jti From token WHERE jti = ?", (jti,))
    token = cursos.fetchone()
    conn.close()
    return token is not None

#-------------------------------------------------------------------#

@app.route("/logout", methods = ['DELETE'])
@jwt_required()
def cerrar_sesion()
    """
    Cierra sesión
    :return: 
    -> 
    -> 
    """
    jti = get_jwt()['jti']
    try:
        conn.commit()
        conn.close()
        return jsonify(msg='JWT revocado'), 200
    except sqlite3.IntegrityError:
        return 'Token ya añadido a la base de datos'

#----------------------------------------------------------------------#

@app.route('/carrito/add', methods=['POST'])   #añadir productos al carrito
@jwt_required() #solo los usuarios registrados pueden hacerlo
def añadir_producto_carrito(producto):
    """
    Añade un nuevo producto al carrito. Solo los usuarios que hayan iniciado sesión pueden
    realizar esta acción.

    Comprueba que el hay un usuario que ha iniciado sesión. Obtiene la informaión del
    producto (nombre, precio, stock, volumen, peso, frágil)

    :param producto:

    :return:

    -> Si el producto se ha añadido correctmaente, codigo de estado 202
    -> Si el producto ya estaba en el carrito, código de estado 409
    """

    carrito = Carrito()
    producto = Producto()
    if producto not in carrito:
        carrito[producto] = request.args.get('value','')
        carrito.anyadir_producto(producto)
        return f'Producto: {producto} añadido al carrito', 200
    else:
        return f'Prodcuto: {producto} ya incluido en el carrito', 409

#-------------------------------------------------------------------------------#

@app.route('/carrito/delete', methods=['DELETE'])  # elimina productos al carrito
@jwt_required()  # solo los usuarios registrados pueden hacerlo
def eliminar_producto_carrito(producto):
    """
    Elimina un producto al carrito. Solo los usuarios que hayan iniciado sesión pueden
    realizar esta acción

    Comprueba que el hay un usuario que ha iniciado sesión. Obtiene la informaión del
    producto (nombre, precio, stock, volumen, peso, frágil)

    :param producto: producto

    :return:

    -> Si el producto se ha eliminado correctamente, código de estado 202
    -> Si el producto no se encontraba en el carritio, deuvleve código 409
    """
    carrito = Carrito()
    producto = Producto()
    if producto in carrito:
        carrito[producto] = request.args.get('value', '')
        carrito.eliminar_producto(producto)
        return f'Dato {producto} eliminado del carrito', 200
    else:
        return f'Dato {producto} no exsiste en el carrito', 409

#-----------------------------------------------------------------------------------#

@app.route('/carrito', methods=['DELETE'])  #vacia el carrito
@jwt_required()  # solo los usuarios registrados pueden hacerlo
def vaciar_carrito():
    """
    AVacía el carrito. Solo los usuarios que hayan iniciado sesión pueden
    realizar esta acción

    Comprueba que el hay un usuario que ha iniciado sesión. Obtiene la informaión del
    producto (nombre, precio, stock, volumen, peso, frágil)

    :param producto: producto

    :return:

    -> Si el carrito se ha vaciado correctamente, códido estado 202

    """
    carrito = Carrito()
    if carrito is not None:
        carrito = request.args.get('value', '')
        carrito.vaciar_carrito()
        return f'Carrito vaciado: {carrito}', 200
    else:
        return f'El carrito ya está vacío', 409

#---------------------------------------------------------------------------------------#

@app.route('/factura', methods=['POST'])  #genera factura producto
def generar_factura_producto():
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

    user = request.args.get('user', '')

    data = request.get_json()
    carrito.data.get("carrito")

    factura = FacturaPDF(user,carrito)

    try:
        return factura.generar()
    except KeyError:
        return f'Producto no encontrado'

#------------------------------------------------------------------------------------------#

@app.route('/tienda', methods = ['POST'])
@jwt_required()
def añadir_producto_tienda():
    """
    Añade producto a la tienda. (falta agregar que solo los Administradires puedan realizar esta acción)

    :return:

    -> Si el producto se guardo correctamente, 202
    -> Si el producto ya estaba en la tienda
    """
    #COMPROBACIÓN ADMINSITRADOR

    tienda = Tienda()
    producto = Producto

    if producto not in tienda:
        return producto.guardar(producto, producto.productos_precio, producto.productos_stock), 202

    else:
        return f'El producto ya se encontraba en la tienda', 409

#------------------------------------------------------------------------------------------#

@app.route('/carrito/ver', methods = ['GET'])
@jwt_required()
def ver_carrito():
    """
    Muestra toda la información del carrito
    :return:
    ->
    ->
    """
    carrito = Carrito()
    return print(carrito)

#-----------------------------------------------------------------------------------------------#

@app.route('/tienda', methods = ['GET'])
@jwt_required()
def mostrar_catalogo():
    """
    Muestra todos los productos de la tienda

    :return:

    -> Si muestra los objetos, devuelve el código de estado 202
    -> Si la tienda esta vacía, devuelve el código 404

    """
    tienda = Tienda()
    tienda = request.args.get('tienda','')
    return print(tienda)

#--------------------------------------------------------------------------------------------#

@app.route('/producto/reseña', methods = ['POST'])
@jwt_required()
def añadir_reseña(producto,puntuación,comentario):
    """
    Añade una reseña a un producto

    :return:

    -> Si el producto existe, 202
    -> Si no se encuentra el producto, 404
    """
    return añadir_reseña(producto,puntuación,comentario)

#--------------------------------------------------------------------------------------------#

@app.route('/cliente', methods=['POST'])
@jwt_required()
def recargar_saldo(cantidad):
    """
    Recarga el saldo del cliente

    :return:

    """
    cliente = Cliente()
    cliente.recargar_saldo(cantidad)

if __name__ == '__main__':
    app.run(debug=True)

#---------------------------------------------------------------------------------------------#
