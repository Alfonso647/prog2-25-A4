import random
from TProducto import Producto

class Tienda:
    '''
    Clase que representa la tienda online

    Atributos
    ---------
    productos: dict
        Diccionario con el nombre del producto y su stock
    productos_precio: dict
        Diccionario con el nombre del producto y su precio

    Métodos
    --------
    nuevo_producto(producto): método de clase
        Añade un nuevo producto a la tienda
    reponer_stock(): método de clase
        Añade a todos los productos un número aleatorio de unidades
    '''

    productos = {}
    productos_precio = {}
    producto_clase = {}

    @classmethod
    def nuevo_producto(cls, producto):

        cls.productos[producto.nombre] = producto.stock
        cls.productos_precio[producto.nombre] = producto.precio
        cls.producto_clase[producto.nombre] = producto

    @classmethod
    def reponer_stock(cls):
        for nombre in cls.productos:
            cls.productos[nombre] += random.randint(25, 40)
        print('Se han repuesto unidades')

    def __str__(self) -> str:
        res = ''
        for nombre, precio in self.__class__.productos_precio.items():
            stock = self.__class__.productos[nombre]
            res += f'{nombre}: {precio}€, Stock: {stock}\n'
        return res

