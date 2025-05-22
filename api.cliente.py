
#Importa la librería requests para realizar peticiones HTTP al servidor Flask
import requests

#Importa las clases necesarias del proyecto
from TTienda import Tienda
from TCliente import Cliente
from TProducto import Producto
from TCarrito import Carrito
from TVentaProducto import poner_producto_en_venta
from TFactura import Factura

#URL base del servidor al que se harán las peticiones
URL = 'http://localhost:5000'

#Token JWT que se usará para autenticar al usuario en peticiones protegidas
token_actual = None

def registrarse():
    """Solicita al usuario un nombre y contraseña, y realiza una petición al servidor para registrar un nuevo usuario."""
    print("Registrarse")
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    respuesta = requests.post(f'{URL}/registrarse', json={
        'nombre_usuario': nombre,
        'contraseña': contraseña
    })

    print(respuesta.json().get('mensaje', 'Error desconocido'))

def iniciar_sesion():
    """Permite al usuario iniciar sesión, obtiene el token JWT del servidor y abre el menú de usuario autenticado."""
    global token_actual
    print("Iniciar sesión")
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    respuesta = requests.post(f'{URL}/iniciar_sesion', json={
        'nombre_usuario': nombre,
        'contraseña': contraseña
    })
    datos = respuesta.json()
    if respuesta.status_code == 200:
        token_actual = datos['token']
        print("Sesión iniciada con éxito.")
        client = Cliente(nombre, contraseña)
        menu_usuario_autenticado(client)
    else:
        print("Error:", datos.get('mensaje', 'Credenciales incorrectas'))

def cerrar_sesion():
    """Elimina el token actual y devuelve al usuario al menú principal."""
    global token_actual
    token_actual = None
    print("🔒 Sesión cerrada. Volviendo al menú principal.")

def menu_usuario_autenticado(cliente):
    """
    Muestra el menú de opciones disponibles para un usuario autenticado.

    Parameters
    ----------
    cliente : Cliente
        Instancia del cliente autenticado que ha iniciado sesión.
    """
    salir = False
    client = cliente
    while not salir:
        print("\n=== MENÚ DE USUARIO AUTENTICADO ===")
        print('1. Recargar saldo')
        print('2. Pasarse a premium')
        print('3. Ver carrito')
        print('4. Catálogo de productos')
        print('5. Mostrar historial de compras')
        print('6. Publicar producto en venta')
        print('7. Añadir reseña a producto comprado')
        print('8. Ver reseñas de un producto')
        print('9. Cerrar Sesión')

        opcion = input("Seleccione una opción (1-9): ")

        if opcion == '1':
            #Recarga saldo en la cuenta del cliente
            try:
                dinero = int(input('Introduce el dinero que quieres recargar: '))
                client.recargar_saldo(dinero)
            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opcion == '2':
            #Opción para convertir la cuenta a premium (si se dispone de saldo suficiente)
            print('1. Sí')
            print('2. No')
            try:
                opc_pre = int(input('Pasarse la cuenta a premium cuesta 100€. ¿Quieres hacerlo? '))
                if opc_pre == 1:
                    client.cuenta_a_premium()
                else:
                    prem = 'no' if not (client.cuenta_premium) else ''
                    print(f'Sigues como usuario {prem} premium')
            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opcion == '3':
            #Muestra el contenido del carrito y opciones relacionadas
            print(client.carrito)
            print('1. Eliminar producto')
            print('2. Ver factura')
            print('3. Finalizar compra')
            print('4. Volver')

            try:
                opc_car = int(input('Selecciona una opción: '))

                if opc_car == 1:
                    #Eliminar un producto del carrito
                    prod_elim = input('Introduce el nombre del producto a eliminar: ').lower()
                    try:
                        cant_elim = int(input('Introduce la cantidad de este producto a eliminar: '))
                    except ValueError:
                        print('Error. Introduce los datos correctamente')
                    else:
                        if prod_elim in Carrito.carrito.keys():
                            prod_elim = Tienda.producto_clase[prod_elim]
                            client.eliminar_producto(prod_elim, cant_elim)
                        else:
                            print('Error. Introduce un producto válido')

                elif opc_car == 2:
                    #Mostrar factura generada del carrito
                    print("\nFACTURA")
                    y = client.carrito.carrito
                    Factura.mostrar_factura(client, y)

                elif opc_car == 3:
                    #Finalizar compra y limpiar carrito
                    client.finalizar_compra()

                else:
                    print('Has salido del carrito')

            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opcion == '4':
            #Catálogo de productos disponibles en la tienda
            print('Ver catálogo de productos:')
            print(Tienda())
            print('1. Añadir producto')
            print('2. Volver')
            try:
                opc_tie = int(input('Selecciona una opción: '))
                if opc_tie == 1:
                    prod_any = str(input('Introduce el nombre del producto a añadir: ')).lower()
                    try:
                        cant_any = int(input('Introduce la cantidad de este producto a añadir: '))
                    except ValueError:
                        print('Error. Introduce los datos correctamente')
                    else:
                        if prod_any in Tienda.producto_clase.keys():
                            prod_any = Tienda.producto_clase[prod_any]
                            client.comprar_producto(prod_any, cant_any)
                        else:
                            print('Error. Introduce un producto válido')
                else:
                    print('Has salido del carrito')
            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opcion == '5':
            #Muestra el historial de compras del usuario
            client.mostrar_historial_compras()
            print('\n')

        elif opcion == '6':
            #Permite al cliente añadir un nuevo producto en venta
            print('Publicar producto en venta')
            nombre = input('Nombre del producto: ').lower()
            if nombre in Tienda.producto_clase.keys():
                try:
                    cant_extra = int(input(f'Este producto está en la tienda a {Tienda.productos_precio[nombre]}€ y hay un stock de {Tienda.productos[nombre]}. ¿Cuántos más deseas introducir? '))
                    if cant_extra > 0:
                        prod_extra = Tienda.producto_clase[nombre]
                        prod_extra.stock += cant_extra
                        Tienda.productos[nombre] = prod_extra.stock
                        print(f'Ahora hay {Tienda.productos[nombre]} unidades de {nombre} en la tienda.')
                    else:
                        print("Error: La cantidad debe ser positiva.")
                except ValueError:
                    print('Error. Introduce los datos correctamente')
            else:
                try:
                    precio = float(input('Precio (€): '))
                    stock = int(input('Cantidad en stock: '))
                    volumen = float(input('Volumen (cm³): '))
                    peso = float(input('Peso (g): '))
                    estado = input('Estado del producto (\"nuevo\" o \"segunda mano\"): ').lower()
                    if estado not in ["nuevo", "segunda mano"]:
                        raise ValueError("Estado inválido. Debe ser 'nuevo' o 'segunda mano'.")
                    client.vender_producto(nombre, precio, stock, volumen, peso, estado)
                except Exception as e:
                    print(f"Error al añadir producto: {e}")
                    print('\n')

        elif opcion == '7':
            #Permite al cliente añadir una reseña a un producto previamente comprado
            print('Añadir reseña a producto comprado')
            if not client.historial_compras:
                print('No has comprado ningún producto aún.')
            else:
                productos = list(client.historial_compras.keys())
                for i, p in enumerate(productos):
                    print(f"{i + 1}. {p.nombre}")
                try:
                    seleccion = int(input("Selecciona el número del producto: ")) - 1
                    if seleccion not in range(len(productos)):
                        raise ValueError("Selección no válida.")
                    puntuacion = float(input("Puntuación (0-10): "))
                    comentario = input("Comentario: ")
                    client.anyadir_resenya(productos[seleccion], puntuacion, comentario)
                except Exception as e:
                    print(f"Error al añadir reseña: {e}")
            print('\n')

        elif opcion == '8':
            #Muestra reseñas de un producto determinado (si lo ha comprado o lo vende)
            print('Ver reseñas de un producto')
            nombre = input("Introduce el nombre del producto: ")
            encontrado = False
            todos = list(client.historial_compras.keys()) + client.productos_en_venta
            for p in todos:
                if p.nombre.lower() == nombre.lower():
                    for linea in p.mostrar_resenyas():
                        print(linea)
                    encontrado = True
            if not encontrado:
                print('No se encontraron reseñas o el producto no existe.')
            print('\n')

        elif opcion == '9':
            #Sale del menú autenticado
            print("Hasta luego.")
            salir = True
        else:
            print("Opción inválida.")

def menu_principal():
    """Menú principal del programa, antes de iniciar sesión."""
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrarse()
        elif opcion == '2':
            iniciar_sesion()
        elif opcion == '3':
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")

if __name__ == '__main__':
    #Punto de entrada principal de la aplicación
    menu_principal()
=======
import requests

URL = 'http://127.0.0.1:5000'

# Funciones que ya no usan token de autenticación
def recargar_saldo(cantidad):
    response = requests.post(f'{URL}/saldo', json={'cantidad': cantidad})
    print(response.text)

def pasar_a_premium():
    response = requests.post(f'{URL}/premium')
    print(response.text)

def ver_carrito():
    response = requests.get(f'{URL}/carrito')
    print(response.text)

def eliminar_producto_carrito(nombre, cantidad):
    response = requests.delete(f'{URL}/carrito', json={'producto': nombre, 'cantidad': cantidad})
    print(response.text)

def finalizar_compra():
    response = requests.post(f'{URL}/compra/finalizar')
    print(response.text)

def ver_catalogo():
    response = requests.get(f'{URL}/productos')
    print(response.text)

def comprar_producto(nombre, cantidad):
    response = requests.post(f'{URL}/carrito', json={'producto': nombre, 'cantidad': cantidad})
    print(response.text)

def mostrar_historial():
    response = requests.get(f'{URL}/historial')
    print(response.text)

def publicar_producto(nombre, precio, stock, volumen, peso, estado):
    response = requests.post(f'{URL}/producto', json={
        'nombre': nombre,
        'precio': precio,
        'stock': stock,
        'volumen': volumen,
        'peso': peso,
        'estado': estado
    })
    print(response.text)

def añadir_reseña(producto, puntuacion, comentario):
    response = requests.post(f'{URL}/producto/{producto}/resenya', json={
        'puntuacion': puntuacion,
        'comentario': comentario
    })
    print(response.text)

def ver_reseñas(producto):
    response = requests.get(f'{URL}/producto/{producto}/resenyas')
    print(response.text)

# Función principal del menú
def menu():
    print('1. Recargar saldo')
    print('2. Pasarse a premium')
    print('3. Ver carrito')
    print('4. Catálogo de productos')
    print('5. Mostrar historial de compras')
    print('6. Publicar producto en venta')
    print('7. Añadir reseña a producto comprado')
    print('8. Ver reseñas de un producto')
    print('9. Salir')
    try:
        opc = 0
        while opc < 1 or opc > 9:
            opc = int(input('Selecciona una opción válida: '))
    except ValueError:
        print('Error. Introduce un número válido')
    return opc

def main():
    salir = False
    while not salir:
        opc = menu()

        if opc == 1:
            try:
                cantidad = float(input('Cantidad a recargar: '))
                recargar_saldo(cantidad)
            except ValueError:
                print('Introduce un número válido.')

        elif opc == 2:
            print('1. Sí\n2. No')
            try:
                opc_p = int(input('¿Pasarte a premium por 100€? '))
                if opc_p == 1:
                    pasar_a_premium()
            except ValueError:
                print('Introduce un número válido.')

        elif opc == 3:
            ver_carrito()
            print('1. Eliminar producto\n2. Finalizar compra\n3. Volver')
            try:
                opc_car = int(input('Opción: '))
                if opc_car == 1:
                    nombre = input('Producto a eliminar: ')
                    cantidad = int(input('Cantidad: '))
                    eliminar_producto_carrito(nombre, cantidad)
                elif opc_car == 2:
                    finalizar_compra()
            except ValueError:
                print('Error.')

        elif opc == 4:
            ver_catalogo()
            print('1. Añadir producto\n2. Volver')
            try:
                opc_cat = int(input('Opción: '))
                if opc_cat == 1:
                    nombre = input('Producto: ')
                    cantidad = int(input('Cantidad: '))
                    comprar_producto(nombre, cantidad)
            except ValueError:
                print('Error.')

        elif opc == 5:
            mostrar_historial()

        elif opc == 6:
            try:
                nombre = input('Nombre: ')
                precio = float(input('Precio: '))
                stock = int(input('Stock: '))
                volumen = float(input('Volumen: '))
                peso = float(input('Peso: '))
                estado = input('Estado (nuevo/segunda mano): ')
                publicar_producto(nombre, precio, stock, volumen, peso, estado)
            except Exception as e:
                print(f"Error: {e}")

        elif opc == 7:
            nombre = input('Producto a reseñar: ')
            try:
                puntuacion = float(input('Puntuación (0-10): '))
                comentario = input('Comentario: ')
                añadir_reseña(nombre, puntuacion, comentario)
            except ValueError:
                print('Error.')

        elif opc == 8:
            nombre = input('Nombre del producto: ')
            ver_reseñas(nombre)

        elif opc == 9:
            print('Hasta luego.')
            salir = True

if __name__ == '__main__':
    main()
