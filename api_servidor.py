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
