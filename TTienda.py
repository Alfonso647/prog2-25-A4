import random


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
    def __init__(self, nombre: str,precio: float,stock: int, volumen: float, peso: float, fragil: bool = False):
        self.nombre = nombre
        self.volumen = volumen
        self.peso = peso
        self.precio = precio
        self.fragil = fragil
        self.stock = stock

        Tienda().nuevo_producto(self) #cada vez que se crea un producto se guarda en tienda

    def __str__(self) -> str:
        sn = 'Sí' if self.fragil==True else 'No'
        cad = f'{self.nombre},{self.precio}€. Tiene un volumen de {self.volumen} centímetros cúbicos y pesa {self.peso} gramos. '
        cad += f'{sn} es frágil'

        return cad



class Tienda:
    '''
    Clase que representa la tienda online
    Atributos
    ---------
    productos: dict
        diccionario con el nombre del producto y su stock
    productos_precio: dict
        diccionario con el nombre del producto y su precio

    Métodos
    --------
    nuevo_producto(producto)  méodo de clase
        añade un nuevo producto a la tienda
    reponer_stock() metodo de clase
        añade a todos los productos un número aletorio de unidades
    '''
    productos = {}    # {nombre: stock}
    productos_precio = {}   # {nombre: precio}

    @classmethod
    def nuevo_producto(cls, producto: Producto):
        cls.productos[producto.nombre] = producto.stock
        cls.productos_precio[producto.nombre] = producto.precio

    def __str__(self) ->str:
        res = ""
        for nombre, precio in self.__class__.productos_precio.items():
            stock = self.__class__.productos[nombre]
            res += f"{nombre}: {precio}€, Stock: {stock}\n"
        return res

    @classmethod
    def reponer_stock(cls):
        for nombre, stock in cls.productos.items():
            cls.productos[nombre] += random.randint(25,40)

        print('Se han repuesto unidades')
