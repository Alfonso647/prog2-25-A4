from TCarrito import Carrito
from TTienda import Producto, Tienda
from typing import Union

class Persona:
    '''
    Clase Persona Genérica
    Atributos
    ---------
    nombre: str
        El nombre de la persona
    apellido1 y apellido2: str
        Los apellidos de la persona
    nombre_usuario: str
        El nombre de usuario de la persona
    '''

    def __init__(self, nombre: str, apellido1: str, apellido2: str, nombre_usuario: str):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.nombre_usuario = nombre_usuario



class Cliente(Persona):
    '''
    Clase que constituye a un cliente
    Atributos
    ---------
    nombre, apellido1, apellido2, nombre_usuario: str
        Heredados de Persona
    saldo: float = 0.0
        Dinero de la persona, inicialmente 0 si no se indica
    cuenta_premium: bool = False
        Cuenta empieza en estado 'no premium'
    historial_compras: dict
        Historial de todas las compras que se ha hecho el cliente, con el producto y su cantidad
    carrito: dict
        Carrito de la compra para almacenar antes de realizar la compra, contiene el producto y la cantidad

    Métodos
    ---------
    cuenta_a_premium()
        convierte la cuenta a premium pagando 100€
    regargar_saldo(cantidad)
        recarga x cantidad de € al saldo
    comprar_producto(producto,cantidad)
        añade el producto con su cantidad al carrito
    eliminar_producto(producto,cantidad)
        elimina la cantidad de unidades del producto del carrito
    finalizar_compra()
        añade las compras al historial, actualiza el saldo y los productos de la tienda, y vacía el carrito para la siguiente compra
    mostrar_historial_compras()
        muestra el historial de las compras con sus cantidades efectuadas en su totalidad

    '''
    def __init__(self, nombre: str, apellido1: str, apellido2: str, nombre_usuario: str, saldo: float = 0.0):
        super().__init__(nombre, apellido1, apellido2, nombre_usuario)
        self.saldo = saldo
        self.cuenta_premium = False
        self.historial_compras = {}  # historial inicialmente vacío
        self.carrito = Carrito(f'Carrito de {self.nombre_usuario}')  # carrito inical vacío
        #self.historial_ventas = []
        #self.productos_en_venta = []

    def __str__(self) ->str:
        texto = f'Usuario: {self.nombre_usuario}, saldo: {self.saldo}€'
        return texto

    def cuenta_a_premium(self):
        '''Cambia el estado de la cuenta a premium por el precio de 100€

        Si no hay saldo suficiente lo manifestará'''
        if self.saldo - 100 < 0:
            print('No tienes suficiente saldo para hacerte la cuenta premium')
            return

        self.saldo -= 100
        self.cuenta_premium = True
        print(f'Tu cuenta ya es premium, por 100€ ya no tendrás que pagar envíos nunca más. Saldo: {self.saldo}')

    def recargar_saldo(self, cantidad: Union[int, float]):
        '''Recarga x cantidad de saldo a la cuenta

        Si el saldo que se desea reponer es menor que 0, saltará un error
        Parámetros
        ----------
        cantidad : int o float
            la cantidad que se desea reponer
        '''

        if cantidad > 0:
            self.saldo += cantidad
            print(f'Se han añadido {cantidad}€. Saldo total: {self.saldo}€')
        else:
            print('Error: La cantidad debe ser mayor que 0')

    def comprar_producto(self,producto: Producto,cantidad: int):#'producto' será el nombre del producto
        self.carrito.anyadir_producto(producto,cantidad)

    def eliminar_producto(self,producto: Producto, cantidad: int= None):
        self.carrito.eliminar_producto(producto,cantidad)

    def finalizar_compra(self):
        '''Realiza el proceso del pago

        Comprobará que haya suficiente saldo para procesar el pago
        , si la cuenta es premium, no se cobrará el envío

        Se actualiza el historial de compras del cliente
        , y también el stock de la tienda

        Se vacía el carrito para la próxima compra
        '''
        total, envio = self.carrito.calcular_total()

        if self.cuenta_premium == False:
            if total + envio > self.saldo:
                print('No tienes suficiente dinero para efectuar la compra, deberás recargar tu saldo o eliminar productos '
                  'hasta que tu saldo te lo permita')
                return
            else:
                self.saldo -= total + envio
                print(f'Pagas un extra de {round(envio)}€ por el envío por no tener la cuenta premium')

        if self.cuenta_premium == True:
            if total > self.saldo:
                print('No tienes suficiente dinero para efectuar la compra, deberás recargar tu saldo o eliminar productos '
                  'hasta que tu saldo te lo permita')
                return
            else:
                self.saldo -= total
                print(f'Se te ha descontado {round(envio)}€ de envío por tener la cuenta premium')

            # Actualizar historial de compras
        for producto, cantidad in self.carrito.carrito.items():
            if producto in self.historial_compras:
                self.historial_compras[producto] += cantidad
            else:
                self.historial_compras[producto] = cantidad

            # Actualizar stock en Tienda
        for producto, cantidad in self.carrito.carrito.items():
            Tienda.productos[producto.nombre] -= cantidad

        self.carrito.vaciar_carrito() #se vacía el carrito ya que ya se ha pagado
        print('Compra finalizada con éxito. El carrito ha sido vaciado y el stock ha sido actualizado.')
        print(f'Saldo: {round(self.saldo,2)}€')


    def mostrar_historial_compras(self):

        if not self.historial_compras.items():
            print('No has hecho ninguna compra todavía')
        else:

            for producto, valor in self.historial_compras.items():
                print(f'{producto.nombre}, {valor} unidades compradas en total')




