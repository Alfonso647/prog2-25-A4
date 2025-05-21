from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

# Configuración de la app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_de_datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'clave_super_secreta'

# Inicialización
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contrasenya = db.Column(db.String(120), nullable=False)
    saldo = db.Column(db.Float, default=0.0)


# Crear base de datos al iniciar
with app.app_context():
    db.create_all()

# Ruta para registrarse
@app.route('/registrarse', methods=['POST'])
def registrarse():
    datos = request.get_json()
    nombre = datos.get('nombre_usuario')
    contra = datos.get('contrasenya')

    if Usuario.query.filter_by(nombre_usuario=nombre).first():
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    nueva_contrasenya = generate_password_hash(contra)
    nuevo_usuario = Usuario(nombre_usuario=nombre, contrasenya=nueva_contrasenya)

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado correctamente'}), 201

# Ruta para iniciar sesión y obtener token JWT
@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    datos = request.get_json()
    nombre = datos.get('nombre_usuario')
    contra = datos.get('contrasenya')

    usuario = Usuario.query.filter_by(nombre_usuario=nombre).first()

    if not usuario or not check_password_hash(usuario.contrasenya, contra):
        return jsonify({'mensaje': 'Nombre de usuario o contraseña incorrectos'}), 401

    token = create_access_token(identity=str(usuario.id))
    return jsonify({'mensaje': 'Inicio de sesión exitoso', 'token': token}), 200

@app.route('/recargar_saldo', methods=['POST'])
@jwt_required()
def recargar_saldo():

    try:
        datos = request.get_json()
        cantidad = datos.get('cantidad')

        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            return jsonify({'mensaje': 'La cantidad debe ser un número mayor que 0'}), 400

        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(usuario_id)

        if not usuario:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        usuario.saldo += cantidad
        db.session.commit()

        return jsonify({'mensaje': f'Se han añadido {cantidad}€. Saldo actual: {usuario.saldo:.2f}€'}), 200

    except Exception as e:
        return jsonify({'mensaje': f'Error interno: {str(e)}'}), 500


# Ruta protegida: mostrar todos los usuarios
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    usuarios = Usuario.query.all()
    lista_usuarios = [{'id': u.id, 'nombre_usuario': u.nombre_usuario} for u in usuarios]
    return jsonify(lista_usuarios), 200

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
