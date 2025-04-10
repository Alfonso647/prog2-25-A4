'''
crear_db.py

Este archivo se usa para crear la base de datos de la tienda.

Cuando se ejecuta:
- Borra la base de datos anterior (si existe)
- Crea una nueva base de datos con la tabla de productos
- Añade algunos productos de prueba para poder usar la API desde el principio

Se ejecuta solo una vez al inicio, porque cada vez que ejecuteis se reincia la base de datos (borra all), o sino quitadle la linea de db.dropall.
'''


from app import app, db
from models import Producto

with app.app_context():
    db.drop_all()  # ⚠ Esto borra all si ya existía, útil para reiniciar limpio
    db.create_all()

    # Productos de prueba
    producto1 = Producto(
        nombre="Auriculares Bluetooth",
        descripcion="Auriculares con cancelación de ruido",
        precio=49.99,
        imagen_url="https://ejemplo.com/auriculares.jpg"
    )

    producto2 = Producto(
        nombre="Teclado Mecánico",
        descripcion="Teclado con luces RGB para gaming",
        precio=89.99,
        imagen_url="https://ejemplo.com/teclado.jpg"
    )

    producto3 = Producto(
        nombre="Monitor 24 pulgadas",
        descripcion="Monitor Full HD con entrada HDMI",
        precio=149.99,
        imagen_url="https://ejemplo.com/monitor.jpg"
    )

    # Guardamos en la base de datos
    db.session.add_all([producto1, producto2, producto3])
    db.session.commit()

    print("✔️ Base de datos creada con productos de prueba.")
