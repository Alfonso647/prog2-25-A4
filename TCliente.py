from TCarrito import Carrito
from TTienda import Tienda
from TResena import Resenya
from typing import Union
from TProducto import Producto
from TPersona import Persona


class Cliente(Persona):
    """
    Representa un cliente del sistema con funcionalidades
    de compra, venta y reseñas.
    """

    resenyas_realizadas = []
    def __init__(self, nombre: str, contrasenya: str, saldo: float = 0.0):
        super().__init__(nombre, contrasenya,saldo)
        self.saldo = saldo
        self.cuenta_premium = False
        self.historial_compras = {}
        self.carrito = Carrito(f'Carrito de {self.nombre}')
        self.productos_en_venta = []
        #self.resenyas_realizadas = []

    def __str__(self) -> str:
        return f'Usuario: {self.nombre}, saldo: {self.saldo}€'

    def cuenta_a_premium(self):
        """Convierte la cuenta del cliente en premium si tiene saldo suficiente."""
        if self.cuenta_premium:
            print(f'Tu cuenta ya es premium.')
        else:
            if self.saldo < 100:
                print('No tienes suficiente saldo para hacerte la cuenta premium')
            else:

                self.saldo -= 100
                self.cuenta_premium = True
                print(f'Tu cuenta ya es premium. Saldo: {self.saldo}€')


    def recargar_saldo(self, cantidad: Union[int, float]):
        """Recarga saldo del cliente si la cantidad es válida (>0)."""
        if cantidad > 0:
            self.saldo += cantidad

            print(f'Se han añadido {cantidad}€. Saldo total: {self.saldo}€')

        else:
            print('Error: La cantidad debe ser mayor que 0')

    def comprar_producto(self, producto: Producto, cantidad: int):
        """Anyade un producto al carrito."""
        self.carrito.anyadir_producto(producto, cantidad)

    def eliminar_producto(self, producto: Producto, cantidad: int = None):
        """Elimina un producto del carrito (parcial o totalmente)."""
        self.carrito.eliminar_producto(producto, cantidad)

    def finalizar_compra(self):
        """
        Finaliza la compra si hay suficiente saldo (considerando el envío
        en caso de no ser premium).
        """
        total, envio = self.carrito.calcular_total()
        total_final = total if self.cuenta_premium else total + envio

        if total_final > self.saldo:
            print('No tienes suficiente dinero para efectuar la compra')
            return

        self.saldo -= total_final
        for producto, cantidad in self.carrito.carrito.items():
            self.historial_compras[producto] = self.historial_compras.get(producto, 0) + cantidad
            Tienda.productos[producto.nombre] -= cantidad

        self.carrito.vaciar_carrito()
        print('Compra finalizada. El carrito ha sido vaciado y el stock actualizado.')
        print(f'Saldo: {round(self.saldo, 2)}€')

    def mostrar_historial_compras(self):
        """Muestra los productos comprados por el cliente."""
        if not self.historial_compras.items():
            print('No has hecho ninguna compra todavía')
        else:

            for producto, valor in self.historial_compras.items():
                print(f'{producto.nombre}, {valor} unidades compradas en total')

    def anyadir_resenya(self, producto: Producto, puntuacion: float, comentario: str):
        """
        Anyade una reseña a un producto comprado, valida puntuación (0-10)
        y la guarda en el historial del cliente.
        """
        try:
            if not (0 <= puntuacion <= 10):
                raise ValueError("La puntuación debe estar entre 0 y 10.")

            resenya = Resenya(self.nombre, puntuacion, comentario)
            producto.anyadir_resenya(self.nombre, puntuacion, comentario)
            type(self).resenyas_realizadas.append(resenya)
            print("Reseña añadida con éxito.")
        except Exception as e:
            print(f"Error al añadir reseña: {e}")


    def vender_producto(self, nombre, precio, stock, volumen, peso, estado):
        """
        Crea un producto y lo anyade tanto a la tienda como a los productos en venta del cliente.
        """
        producto = Producto(nombre, precio, stock, volumen, peso, estado='nuevo')
        Tienda.nuevo_producto(producto)
        self.productos_en_venta.append(producto)

        print(f"Producto {nombre} añadido a la venta.")


    def mostrar_productos_en_venta(self):
        """Muestra todos los productos que el cliente tiene puestos a la venta."""
        if not self.productos_en_venta:
            print("No tienes productos en venta.")
        else:
            print("Tus productos en venta:")
            for producto in self.productos_en_venta:
                print("-", producto)

    def mostrar_resenyas_realizadas(self):
        """Muestra todas las reseñas escritas por el cliente."""

        if not type(self).resenyas_realizadas:
            print("No has escrito ninguna reseña todavía.")
        else:
            print("Tus reseñas:")
            for resenya in type(self).resenyas_ralizadas:
                print("-", resenya)

