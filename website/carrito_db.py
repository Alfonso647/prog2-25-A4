class CarritoWeb:
    def __init__(self, carrito_dict=None):
        """
        carrito_dict es un diccionario con el formato:
        {id_producto: cantidad, ...}
        """
        self.carrito = carrito_dict if carrito_dict else {}

    def anyadir_producto(self, id_producto):
        """
        Añade una unidad del producto al carrito.
        """
        id_producto = str(id_producto)  # Aseguramos que la clave sea str (por compatibilidad con JSON)
        if id_producto in self.carrito:
            self.carrito[id_producto] += 1
        else:
            self.carrito[id_producto] = 1

    def eliminar_producto(self, id_producto):
        """
        Elimina completamente un producto del carrito.
        """
        id_producto = str(id_producto)
        if id_producto in self.carrito:
            del self.carrito[id_producto]

    def vaciar(self):
        """
        Vacia completamente el carrito.
        """
        self.carrito.clear()

    def obtener_productos(self):
        """
        Devuelve el diccionario de productos actual.
        """
        return self.carrito.copy()

    def calcular_total(self, productos_db):
        """
        Recibe un diccionario {id_producto: Producto2} y calcula el total del carrito.
        """
        total = 0.0
        for id_prod, cantidad in self.carrito.items():
            producto = productos_db.get(int(id_prod))
            if producto:
                total += producto.precio * cantidad
        return total
