
'''

import sqlite3
from TCarrito import Carrito
from TTienda import Producto, Tienda
from typing import Union

class Persona:
    def __init__(self, nombre: str, apellido1: str, apellido2: str, nombre_usuario: str, password: str):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.nombre_usuario = nombre_usuario
        self.password = password


class Cliente(Persona):
    def __init__(self, nombre: str, apellido1: str, apellido2: str, nombre_usuario: str, password: str, saldo: float = 0.0):
        super().__init__(nombre, apellido1, apellido2, nombre_usuario, password)
        self.saldo = saldo
        self.cuenta_premium = False
        self.historial_compras = {}
        self.carrito = Carrito(nombre)

    def __str__(self) -> str:
        return f'Usuario: {self.nombre_usuario}, saldo: {self.saldo}€'

    def cuenta_a_premium(self):
        if self.saldo - 100 < 0:
            print('No tienes suficiente saldo para hacerte la cuenta premium')
            return

        self.saldo -= 100
        self.cuenta_premium = True
        print(f'Tu cuenta ya es premium. Saldo: {self.saldo}')

    def recargar_saldo(self, cantidad: Union[int, float]):
        if cantidad > 0:
            self.saldo += cantidad
            print(f'Se han añadido {cantidad}€. Saldo total: {self.saldo}€')
        else:
            print('Error: La cantidad debe ser mayor que 0')

    def comprar_producto(self, producto: Producto, cantidad: int):
        self.carrito.anyadir_producto(producto, cantidad)

    def eliminar_producto(self, producto: Producto, cantidad: int = None):
        self.carrito.eliminar_producto(producto, cantidad)

    def finalizar_compra(self):
        total, envio = self.carrito.calcular_total()

        if not self.cuenta_premium:
            if total + envio > self.saldo:
                print('No tienes suficiente dinero.')
                return
            else:
                self.saldo -= total + envio
                print(f'Pagas {round(envio)}€ de envío')
        else:
            if total > self.saldo:
                print('No tienes suficiente dinero.')
                return
            else:
                self.saldo -= total

        for producto, cantidad in self.carrito.carrito.items():
            if producto in self.historial_compras:
                self.historial_compras[producto] += cantidad
            else:
                self.historial_compras[producto] = cantidad
            Tienda.productos[producto.nombre] -= cantidad

        self.carrito.vaciar_carrito()
        print('Compra finalizada.')

    def mostrar_historial_compras(self):
        if not self.historial_compras:
            print('No has hecho ninguna compra todavía')
        else:
            for producto, valor in self.historial_compras.items():
                print(f'{producto.nombre}, {valor} unidades')

    @staticmethod
    def cargar(nombre_usuario: str):
        conn = sqlite3.connect('tienda.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, apellido1, apellido2, nombre_usuario, contrasena, saldo, premium FROM clientes WHERE nombre_usuario = ?", (nombre_usuario,))
        row = cursor.fetchone()
        conn.close()
        if row:
            nombre, apellido1, apellido2, usuario, contrasena, saldo, premium = row
            cliente = Cliente(nombre, apellido1, apellido2, usuario, contrasena, saldo)
            cliente.cuenta_premium = bool(premium)
            return cliente
        else:
            return None

    @staticmethod
    def autenticar(nombre_usuario: str, password: str):
        cliente = Cliente.cargar_cliente(nombre_usuario)
        if cliente and cliente.password == password:
            return cliente
        else:
            return None
'''