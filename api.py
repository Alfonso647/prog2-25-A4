from flask import Flask, jsonify
from models import db, Producto

app = Flask(__name__)

# Configuración para SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Ruta de prueba
@app.route('/')
def home():
    return "¡API de productos funcionando!"

# Ruta para obtener producto por ID
@app.route('/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    producto = Producto.query.get(id)
    if producto:
        return jsonify({
            "id": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "imagen": producto.imagen_url
        })
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
