class Producto:
    '''
    Clase que representa un producto
    Atributos
    ----------
    nombre: str
        nombre del producto
    precio: float
        valor del producto en €
    stock: int
        cantidad inicial de unidades del producto
    volumen: float
        volumen del procucto en cm cúbicos
    peso: float
        peos del producto en gramos
    fragil: bool
        indica si el producto es frágil

    Métodos
    --------
    __init__
        inicializa la clase y además añade el producto creado a la tienda online, de manera que siempre que se
        cree un producto de añadira a la tienda

    '''
    
    productos_stock={}
    productos_precio={}

    def __init__(self, nombre: str,precio: float,stock: int, volumen: float, peso: float, fragil: bool = False):
        self.nombre = nombre
        self.volumen = volumen
        self.peso = peso
        self.precio = precio
        self.fragil = fragil
        self.stock = stock

        self.guardar(self.nombre, self.precio, self.stock)
        '''
        Este método guarda el stock y el precio de un producto, ya que luego lo utilizaremos
        '''
        
    def guardar(cls, nombre, precio, stock):
        cls.productos_stock[nombre] = stock
        cls.productos_precio[nombre] = precio

        # Tienda().nuevo_producto(self) #cada vez que se crea un producto se guarda en tienda

    def __str__(self) -> str:
        sn = 'Sí' if self.fragil==True else 'No'
        cad = f'{self.nombre},{self.precio}€. Tiene un volumen de {self.volumen} centímetros cúbicos y pesa {self.peso} gramos. '
        cad += f'{sn} es frágil'

        return cad
