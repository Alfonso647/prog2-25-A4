'''
models.py

Este archivo define la estructura de la base de datos.

Aquí está el modelo "Producto", que representa los productos que se venden en la tienda.

Cada producto tiene:
- un id
- un nombre
- una descripción
- un precio
- una imagen (enlace a una foto)

Usamos SQLAlchemy para que Python pueda trabajar con la base de datos.
'''

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen_url = db.Column(db.String(200), nullable=True)
