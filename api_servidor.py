
#Importación de librerías necesarias
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

#Configuración principal de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_de_datos.db'  #Ruta del archivo de base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  #Desactiva el seguimiento de cambios innecesario
app.config['JWT_SECRET_KEY'] = 'clave_super_secreta'  #Clave secreta para firmar los tokens JWT

#Inicialización de la base de datos y el gestor JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)

class Usuario(db.Model):
    """
    Clase que representa a un usuario en la base de datos.

    Attributes
    ----------
    id : int
        Identificador único del usuario (clave primaria).
    nombre_usuario : str
        Nombre de usuario único utilizado para iniciar sesión.
    contraseña : str
        Contraseña cifrada del usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)

#Crea las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

@app.route('/registrarse', methods=['POST'])
def registrarse():
    """
    Ruta para registrar un nuevo usuario.

    Recibe un JSON con nombre_usuario y contraseña.
    Valida si el usuario ya existe, y si no, lo guarda en la base de datos
    con la contraseña cifrada.
    """
    datos = request.get_json()
    nombre = datos.get('nombre_usuario')
    contra = datos.get('contraseña')

    if Usuario.query.filter_by(nombre_usuario=nombre).first():
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    nueva_contraseña = generate_password_hash(contra)
    nuevo_usuario = Usuario(nombre_usuario=nombre, contraseña=nueva_contraseña)

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado correctamente'}), 201

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    """
    Ruta para iniciar sesión y generar un token JWT.

    Recibe un JSON con nombre_usuario y contraseña.
    Verifica las credenciales, y si son correctas, genera un token JWT.
    """
    datos = request.get_json()
    nombre = datos.get('nombre_usuario')
    contra = datos.get('contraseña')

    usuario = Usuario.query.filter_by(nombre_usuario=nombre).first()

    if not usuario or not check_password_hash(usuario.contraseña, contra):
        return jsonify({'mensaje': 'Nombre de usuario o contraseña incorrectos'}), 401

    token = create_access_token(identity=usuario.id)
    return jsonify({'mensaje': 'Inicio de sesión exitoso', 'token': token}), 200

@app.route('/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    """
    Ruta protegida que devuelve la lista de todos los usuarios registrados.

    Requiere token JWT válido en la cabecera Authorization.
    """
    usuarios = Usuario.query.all()
    lista_usuarios = [{'id': u.id, 'nombre_usuario': u.nombre_usuario} for u in usuarios]
    return jsonify(lista_usuarios), 200

#Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)
=======
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

