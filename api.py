from crypt import methods
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask import Flask, request, jsonify
import hashlib

'Datos almecenados de nuestra app'
users = {}
data = {}
app = Flask(__name__)


app.config['JWT_SECRET_KEY'] = 'A4'
jwt = JWTManager(app)

@app.route('/singup', methods=['POST'])    #Ininiar sesión
def singup():
    user = request.args.get('user', '')
    if user in users:
        return f'Usuario {user} ya registrado', 409
    else:
        password = request.args.get('password','')
        hashed = hash.lib.sha256(password.encode()).hexdigest()
        users[user] = hashed
        return f'Usuario {user} registrado', 200

###cerrar sesión

#...

@app.route('/singin', methods=['GET']) #Autentificación
def login():
    user = request.args.get('user','')
    password = request.args.get('password','')
    hashed = hashlib.sha256(password.encode()).hexdigest()
    if user in users and users[user] == hashed:
        return create_access_token(identity=user), 200
    else:
        return  f'Usuario o contraseña incorrectos', 401

@app.route("/")
def root():
    return 'Api de Productos'

@app.route('/data/<string:id>', methods=['POST'])   #añadir datos
def add_data(id):
    if id not in data:
        data[id] = request.args.get('value','')
        return f'Dato {id} añadido', 200
    else:
        return f'Dato {id} ya incluido', 409

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
