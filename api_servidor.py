from carrito_prodcutos import carrito
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
    contraseña = db.Column(db.String(120), nullable=False)
    premium = db.Column(db.Boolean, default = False)

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.Foreign('usuario.id'),nullable=False)
    productos = db.relationship('Productos', secondary=carrito_productos, backref= 'carritos')

# Crear base de datos al iniciar
with app.app_context():
    db.create_all()

# Ruta para registrarse
@app.route('/registrarse', methods=['POST'])
def registrarse():
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

# Ruta para iniciar sesión y obtener token JWT
@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    datos = request.get_json()
    nombre = datos.get('nombre_usuario')
    contra = datos.get('contraseña')

    usuario = Usuario.query.filter_by(nombre_usuario=nombre).first()

    if not usuario or not check_password_hash(usuario.contraseña, contra):
        return jsonify({'mensaje': 'Nombre de usuario o contraseña incorrectos'}), 401

    token = create_access_token(identity=usuario.id)
    return jsonify({'mensaje': 'Inicio de sesión exitoso', 'token': token}), 200

# Ruta protegida: mostrar todos los usuarios
@app.route('/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    usuarios = Usuario.query.all()
    lista_usuarios = [{'id': u.id, 'nombre_usuario': u.nombre_usuario} for u in usuarios]
    return jsonify(lista_usuarios), 200

@app.route('/premium', methods=['POST'])
@jwt_required()
def hacer_premium():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)

    if usuario is None:
        return jsonify(({'mensaje': 'Usuario no encontrado'})), 404

    if usuario.premium:
        return jsonify(({'mensaje': 'Ya eres usuario premium'})), 200

    usuario.premium = True
    db.session.commit()
    return jsonify({'mensaje': 'Ahora eres usuario premium'})

@app.route('/carrito', methods = ['GET'])
@jwt_required()
def mostrar_carrito():
    usuario_id = get_jwt_identity()
    carrito = Carrito.query.filter_by(usuario_id = usuario_id).first()

    if not carrito or not carrito.productos:
        return jsonify({'carrito:'[], 'mensaje': 'El carrito está vacío'})

    productos = [{
        'id': p.id,
        'nombre': p.nombre,
        'precio': p.precio,
        'descripción': p.descripcion
    } for p in carrito.productos]

    return jsonify({'carrito': productos})



# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
