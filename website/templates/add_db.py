from website import app, db
from website.productos_db import Producto2

# Crear contexto de aplicación para acceder a la base de datos
app = app()

with app.app_context():
    # Solo añadimos productos si aún no existen
    if Producto2.query.first() is None:
        producto1 = Producto2(
            nombre="Libro Python",
            precio=29.99,
            stock=16,
            volumen=10,
            peso=3,
            detalles='Muy chulo',
            fragil=False
        )

        producto2 = Producto2(
            nombre="Teclado",
            precio=22.25,
            stock=88,
            volumen=8,
            peso=14,
            detalles='Teclado que sirve para escribir',
            fragil=True
        )

        producto3 = Producto2(
            nombre="Ratón",
            precio=14,
            stock=12,
            volumen=1,
            peso=3,
            detalles='Económico',
            fragil=True
        )

        db.session.add_all([producto1, producto2, producto3])
        db.session.commit()
        print("Productos añadidos.")
