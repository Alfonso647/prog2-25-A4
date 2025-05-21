from crear_db import db

carrito_productos = db.Table('carrito_productos',
    db.Column('carrito_id', db.Integer, db.ForeignKey('carrito.id'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id'), primary_key=True)
)