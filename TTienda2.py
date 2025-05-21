'''

import random
from TProd import Producto


class Tienda:

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

    def __str__(self) ->str:
        res = ''
        for nombre, precio in self.__class__.productos_precio.items():
            stock = self.__class__.productos[nombre]
            res += f'{nombre}: {precio}€, Stock: {stock}\n'
        return res

    @classmethod
    def reponer_stock(cls):
        for nombre, stock in cls.productos.items():
            cls.productos[nombre] += random.randint(25,40)

        print('Se han repuesto unidades')
'''