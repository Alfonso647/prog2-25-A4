from typing import Union
from TProd import Producto
from TTienda import Tienda


class Carrito:
    '''
    Clase que representa el carrito temporal de compra
    Atributos
    ---------
    nombre:str
        nombre que obtiene el carrito automático por la clase cliente
    carrito: dict
        contine el producto y su cantidad

    Métodos
    --------
    anyadir_producto(producto, cantidad)
        añade un producto con su respectiva cantidad al carrito, si existe,si hay stock,
    eliminar_producto(producto, cantidad)
        elimina la x unidades de un producto del carrito
    calcular_total()
        calcula en total y más el envío
    vaciar_carrito()
        vacía el carrito por completo
    '''

    def anyadir_producto(self, producto: Producto):
        '''Añade un producto al carrito

        Parámetros
        ----------
        producto: Producto
            el producto que se añade
            debe existir el producto en la tienda para añadirlo al carrito
        cantidad: int
            la cantidad debe ser positiva para que no salte un error
            además, debe haber stock de ese producto para que se pueda añadir
        '''
        #if cantidad <= 0:
            #print('Error: La cantidad debe ser positiva')
            #return

        if producto.nombre not in Tienda.productos
            print('Error: El producto no existe en la tienda')
            return

        stock_disponible = Tienda.productos[producto.nombre]

        if cantidad > stock_disponible:
            print(f'Error: No hay suficiente stock disponible. Stock actual: {stock_disponible}')
            return

        if producto in self.carrito:
            if self.carrito[producto] + cantidad > stock_disponible:
                print(f'Error: No puedes añadir más de {stock_disponible} unidades en total')
                return
            self.carrito[producto] += cantidad
        else:
            self.carrito[producto] = cantidad

        print(f'Se han añadido {cantidad} unidades de  {producto.nombre} al carrito.')

    def eliminar_producto(self, producto: Producto, cantidad: int = None):
        '''Elmina cierta cantidad de un producto en el carrito

        El producto debe exitir y la cantidad debe ser positiva
        Parámetros
        -----------
        producto: Producto
            el producto que se elimina
        cantidad: int = None
            si no se indica una cantidad, el producto se eliminará por completo
        '''
        if producto not in self.carrito:
            print('Error: Producto no encontrado')
            return

        if cantidad is None:
            del self.carrito[producto]
            print(f'Producto {producto.nombre} eliminado completamente')
        elif cantidad <= 0:
            print('Error: La cantidad debe ser positiva')
        elif cantidad >= self.carrito[producto]:
            del self.carrito[producto]
            print(f'Producto {producto.nombre} eliminado completamente')
        else:
            self.carrito[producto] -= cantidad
            print(f'Se redujo la cantidad de {producto.nombre} en {cantidad} unidades')

    def calcular_total(self) -> Union[int,float]:
        '''Calcula el total del carrito y en envío por separado

        Return
        -------
        total: float
            todos los productos por su precio
        envio: float
            un calculo que relaciona en peso y la medida del producto
        '''
        total = 0
        for clave,valor in self.carrito.items():
            total += clave.precio * valor

        envio = 0
        for producto in self.carrito.keys():
            envio += producto.peso * 0.001 + producto.volumen * 0.001

        return total, envio

    def vaciar_carrito(self):
        '''Vacía el diccionario carrito'''
        self.carrito.clear()  # Elimina todos los elementos del diccionario

    def __str__(self) -> str:
        resultado = f'{self.nombre} \n'
        for producto, cantidad in self.carrito.items():
            resultado += f'{producto.nombre} : {cantidad} x {producto.precio}€\n'

        total, envio = self.calcular_total()
        if self.carrito != False:
            resultado += f'El total a pagar es {round(total,2)}€.\n'
            resultado += f'El precio del envío es de {round(envio)}€'
        else:
            resultado += f'El carrito está vacío'

        return resultado

