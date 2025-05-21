'''
crear_db.py

Este archivo se usa para crear la base de datos de la tienda y
añadir productos, ya sea de prueba o desde un historial de compras.

Contiene:
- Una función para crear la base de datos y las tablas
- Una función para guardar productos desde un historial de compras
'''

from app import app, db
from models import Producto

def crear_base():
    '''Crea la base de datos y las tablas (borra si ya existían).'''
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("✔️ Base de datos creada.")

def guardar_compras_en_db(historial_compras):
    '''
    Guarda los productos comprados en la base de datos a partir del historial.
    Cada clave del diccionario es un objeto Producto, y el valor es la cantidad comprada.
    '''
    with app.app_context():
        for producto, cantidad in historial_compras.items():
            nuevo_producto = Producto(
                nombre=producto.nombre,
                precio=producto.precio,
                stock=cantidad,
                volumen=producto.volumen,
                peso=producto.peso,
                fragil=producto.fragil
            )
            db.session.add(nuevo_producto)

        db.session.commit()
        print("Compras guardadas en la base de datos.")