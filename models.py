'''
models.py

Este archivo define la estructura de la base de datos.

Aquí está el modelo "Producto", que representa los productos que se venden en la tienda.

Cada producto tiene:
- nombre: nombre del producto
- precio: valor del producto en euros (€)
- stock: cuántas unidades hay disponibles
- volumen: volumen del producto en cm³
- peso: peso del producto en gramos
- fragil: indica si el producto es frágil (sí o no)

Usamos SQLAlchemy para que Python pueda trabajar con la base de datos de forma fácil.
'''

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    volumen = db.Column(db.Float, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    fragil = db.Column(db.Boolean, nullable=False)
