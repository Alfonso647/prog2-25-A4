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

    def __init__(self, nombre: str, precio: float, stock: int, volumen: float, peso: float, fragil: bool = False, estado: str = "nuevo"):
        self.nombre = nombre
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

    def añadir_resenya(self, usuario: str, puntuacion: int, comentario: str, cliente=None):
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
            Objeto cliente que hizo la reseña (si se desea guardar también en su historial).

       """
        try:
            resenya = Resenya(usuario, puntuacion, comentario)
            self.resenyas.append(resenya)
            if cliente and hasattr(cliente, "resenyas_realizadas"):
                cliente.resenyas_realizadas.append(resenya)
            return True
        except ValueError as e:
            return str(e) 

    def mostrar_resenyas(self):
        """
        Devuelve las reseñas asociadas al producto.
        """

        if not self.resenyas:
            return ["Este producto no tiene reseñas aún."]
        return [str(r) for r in self.resenyas] # MIRAR ESTO

    def __str__(self) -> str:
        sn = 'Sí' if self.fragil else 'No'
        return f'{self.nombre} ({self.estado}), {self.precio}€. Volumen: {self.volumen} cm³, Peso: {self.peso}g. ¿Frágil?: {sn}'
