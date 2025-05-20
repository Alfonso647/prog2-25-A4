from website import db  # o el nombre donde tengas el objeto db

class Producto2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    volumen = db.Column(db.Float, nullable=True)  # Por ejemplo en m3
    peso = db.Column(db.Float, nullable=True)     # Por ejemplo en kg
    detalles = db.Column(db.Text, nullable=True)  # Descripción larga
    fragil = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Producto {self.nombre} - Precio: {self.precio}€>"

    def __str__(self):
        return f"{self.nombre} - Precio: {self.precio}€, Stock: {self.stock}"

    # Método opcional para mostrar detalles más extensos
    def mostrar_detalles(self):
        fragil_str = "Sí" if self.fragil else "No"
        return (f"Nombre: {self.nombre}\n"
                f"Precio: {self.precio}€\n"
                f"Stock: {self.stock}\n"
                f"Volumen: {self.volumen} m3\n"
                f"Peso: {self.peso} kg\n"
                f"Fragil: {fragil_str}\n"
                f"Detalles: {self.detalles}")

