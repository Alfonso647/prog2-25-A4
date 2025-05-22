
from TResena import Resenya



class Producto:
    """
    Clase que representa un producto.

    Attributes
    ----------
    nombre : str
        Nombre del producto.
    precio : float
        Valor del producto en euros.
    stock : int
        Cantidad inicial de unidades del producto.
    volumen : float
        Volumen del producto en cm cúbicos.
    peso : float
        Peso del producto en gramos.
    fragil : bool
        Indica si el producto es frágil.
    estado : str
        "nuevo" o "segunda mano".
    reseñas : list
        Lista de objetos Reseña asociados a este producto.
    """

    productos_stock = {}
    productos_precio = {}


    def __init__(self, nombre: str, precio: float, stock: int, volumen: float, peso: float, fragil: bool = False,
                 estado: str = "nuevo"):
        self.nombre = nombre.lower()

        self.precio = precio
        self.stock = stock
        self.volumen = volumen
        self.peso = peso
        self.fragil = fragil
        self.estado = estado
        self.resenyas = []

        self.guardar(self.nombre, self.precio, self.stock)

        '''
        Este método guarda el stock y el precio de un producto, ya que luego lo utilizaremos
        '''

    @classmethod
    def guardar(cls, nombre: str, precio: float, stock: int):
        """
        Registra el producto en los diccionarios de stock y precio de clase.

        Parámetros
        ----------
        nombre : str
            Nombre del producto.
        precio : float
            Precio del producto.
        stock : int
            Stock disponible.
        """
        cls.productos_stock[nombre] = stock
        cls.productos_precio[nombre] = precio

    def anyadir_resenya(self, usuario: str, puntuacion: int, comentario: str, cliente=None):
        """
        Añade una reseña al producto. Si se proporciona un cliente, también se añade a su historial.

        Parameters
        ----------
        usuario : str
            Nombre del usuario que hace la reseña.
        puntuacion : int
            Valoración numérica entre 0 y 10.
        comentario : str
            Comentario textual sobre el producto.
        cliente : Cliente, optional

            Objeto cliente que hizo la reseña (si se desea guardar también en su historial)


       """
        try:
            resenya = Resenya(usuario, puntuacion, comentario)
            self.resenyas.append(resenya)
            if cliente and hasattr(cliente, "resenyas_realizadas"):
                cliente.resenyas_realizadas.append(resenya)
            return True
        except ValueError:

            return print('Error. Introduce un número válido')


    def mostrar_resenyas(self):
        """
        Devuelve las reseñas asociadas al producto.
        """

        if not self.resenyas:
            return ["Este producto no tiene reseñas aún."]

        return [str(r) for r in self.resenyas]  # MIRAR ESTO


    def __str__(self) -> str:
        sn = 'Sí' if self.fragil else 'No'
        return f'{self.nombre} ({self.estado}), {self.precio}€. Volumen: {self.volumen} cm³, Peso: {self.peso}g. ¿Frágil?: {sn}'




producto1 = Producto("Drone", 1499.99, 12, 0.04, 0.9, True)
producto2 = Producto("Smartwatch", 399.99, 35, 0.001, 0.05)
producto3 = Producto("Café", 19.99, 200, 0.003, 1.1)
producto4 = Producto("Vino", 29.99, 80, 0.0015, 1.5, True)
producto5 = Producto("Herramientas", 89.99, 25, 0.15, 8.2)
producto6 = Producto("Planta", 45.99, 40, 0.2, 3.8)
producto7 = Producto("Tienda de campaña", 129.99, 18, 0.6, 7.5)
producto8 = Producto("Balón", 49.99, 60, 0.01, 0.45)
producto9 = Producto("Chaqueta", 299.99, 15, 0.03, 1.8)
producto10 = Producto("Reloj", 199.99, 5, 0.002, 0.15, True)
producto11 = Producto("Lego", 159.99, 8, 0.1, 3.2)
producto12 = Producto("Puzzle", 24.99, 30, 0.02, 0.8)
producto13 = Producto("Pinturas", 59.99, 20, 0.01, 0.9)
producto14 = Producto("Lienzo", 39.99, 15, 0.008, 1.1)
producto15 = Producto("Piedra", 9.99, 500, 0.0005, 0.3)