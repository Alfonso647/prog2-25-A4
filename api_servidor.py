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

import os
import sqlite3
import hashlib
from crypt import methods
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from config import JWT_SECRET_KEY

from TCliente import Cliente, Administrador
from TCliente import Persona

ACCESS_EXPIRES = timedelta(hours=0.30)   #los token solo tienen media hora de validez
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = A4
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

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

@app.route('/users', methods=['POST'])
@jwt_required()
def añadir_usuario():
    """

    Comprubea si eres administrador y añade un nuevo usuario al sistema.

    Lee los datos del usuario para comprobar si es administrador (desde la petición
    request.args : nombre, apellido1, apellido2, nombre_usuario, password). Si es un
    administrador, este podrá crear un nuevo usuario (codigo 200) y si no lo és, no
    podrá hacerlo (404)

    :return:

     -> Si se crea un usuario nuevo: código de estado 202
     -> Si el usuario no es un administrador: código de estado 404
     -> Si el usuario que se intenta crear ya está registrado: código de error 409
    """

    usuario = get_jwt_identity()
    user = Administrador()
    if not isinstance(user.nombre_usuario, Administrador)   ####REVISAR####
        return f'Solo los adminsitradores pueden realizar crear usuarios', 404
    nombre = request.args.get('nombre')
    apellido1 = request.args.get('apellido1')
    apellido2 = request.args.get('apellido2')
    password = request.args.get('password')
    admin = request.args.get('administrador', 'no')

    if administrador == 'si':
        if usuario == '0':
            ##hace una falta una clase que pueda añadir usuarios
    #etc


@app.route('/carrito/<string:isbn>', methods=['POST'])   #añadir productos al carrito
@jwt_required() #solo los usuarios registrados pueden hacerlo
def añadir_producto_carrito(producto):
    """
    Añade un nuevo producto al carrito. Solo los usuarios que hayan iniciado sesión pueden
    realizar esta acción

    Comprueba que el hay un usuario que ha iniciado sesión. Obtiene la informaión del
    producto (nombre, precio, stock, volumen, peso, frágil)

    :param producto:

    :return:
    """
    if producto not in carrito:
        carrito[producto] = request.args.get('value','')
        return f'Dato {producto} añadido', 200
    else:
        return f'Dato {producto} ya incluido', 409


##HASTA AQUÍ








@app.route('/data(<id>', methods=['GET'])      #leer datos
def get_data_id(id):
    try:
        return data[id], 200
    except KeyError:
        return f'Dato no encontrado', 404

@app.route('/data/<id>', methods=['PUT'])    #actualizar datos
def update_data(id):
    if id in data:
        data[id] = request.args.get('value','')
        return f'Dato {id} actualizado', 200
    else:
        return f'dato {id} No encontrado, 404'

@app.route('/data/<id>', methods=['DELETE'])  #eliminar datos
def delete_data(id):
    if id in data:
        del data[id]
        return f'Dato {id} eliminado', 200
    else:
        return f'Dato {id} no encontrado'


if __name__ == '__main__':
    app.run(debug=True)