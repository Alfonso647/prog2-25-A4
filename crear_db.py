from api import app, db
from models import Producto

with app.app_context():
    db.drop_all()
    db.create_all()

    producto1 = Producto(nombre="Auriculares Bluetooth", descripcion="Auriculares con cancelación de ruido", precio=49.99, imagen_url="https://ejemplo.com/auriculares.jpg")
    producto2 = Producto(nombre="Teclado Mecánico", descripcion="Teclado RGB para gaming", precio=89.99, imagen_url="https://ejemplo.com/teclado.jpg")

    db.session.add_all([producto1, producto2])
    db.session.commit()

    print("Base de datos creada con productos de prueba.")
