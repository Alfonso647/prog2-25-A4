import requests
from TTienda import Tienda
from TCliente import Cliente
from TProducto import Producto
from TCarrito import Carrito
from TVentaProducto import poner_producto_en_venta
from TFactura import Factura

URL = 'http://localhost:5000'
token_actual = None  # Token JWT guardado después de iniciar sesión

def registrarse():
    print("📝 Registrarse")
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    respuesta = requests.post(f'{URL}/registrarse', json={
        'nombre_usuario': nombre,
        'contraseña': contraseña
    })

    print(respuesta.json().get('mensaje', 'Error desconocido'))

def iniciar_sesion():
    global token_actual
    print("🔐 Iniciar sesión")
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    respuesta = requests.post(f'{URL}/iniciar_sesion', json={
        'nombre_usuario': nombre,
        'contraseña': contraseña
    })
    datos = respuesta.json()
    if respuesta.status_code == 200:
        token_actual = datos['token']
        print("✅ Sesión iniciada con éxito.")
        client=Cliente(nombre,contraseña)
        menu_usuario_autenticado(client)
    else:
        print("❌ Error:", datos.get('mensaje', 'Credenciales incorrectas'))

def cerrar_sesion():
    global token_actual
    token_actual = None
    print("🔒 Sesión cerrada. Volviendo al menú principal.")

def menu_usuario_autenticado(cliente):
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
            try:
                dinero = int(input('Introduce el dinero que quieres recargar: '))
                client.recargar_saldo(dinero)
            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opcion == '2':
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

            print(client.carrito)

            print('1. Eliminar producto')

            print('2. Ver factura')

            print('3. Finalizar compra')

            print('4. Volver')

            try:

                opc_car = int(input('Selecciona una opción: '))

                if opc_car == 1:

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




                # Y en la opción 2 del carrito:

                elif opc_car == 2:

                    print("\n" + "FACTURA")

                    y = client.carrito.carrito

                    Factura.mostrar_factura(client, y)


                elif opc_car == 3:

                    client.finalizar_compra()


                else:

                    print('Has salido del carrito')

            except ValueError:

                print('Error. Introduce un número válido')

            print('\n')

        elif opcion == '4':
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
            client.mostrar_historial_compras()
            print('\n')

        elif opcion == '6':
            print('Publicar producto en venta')
            nombre = input('Nombre del producto: ').lower()
            if nombre in Tienda.producto_clase.keys():
                try:
                    cant_extra = int(input(f'Este producto está en la tienda a {Tienda.productos_precio[nombre]}'
                                           f'€ y hay un stock de {Tienda.productos[nombre]}. '
                                           f'¿Cuántos más deseas introducir? '))
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
            print("Hasta luego.")
            salir = True
        else:
            print("⚠️ Opción inválida.")

def menu_principal():
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
            print("👋 Hasta luego.")
            break
        else:
            print("⚠️ Opción inválida.")

if __name__ == '__main__':
    menu_principal()
