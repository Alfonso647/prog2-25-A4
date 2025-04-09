from crypt import methods
from flask import Flask, request
from flask
'Datos almecenados de nuestra app'
users = {}
data = {}
app = Flask(__name__)


@app.route("/")
def root():
    return 'hello world!'

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
