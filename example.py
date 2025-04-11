from TTienda import Tienda
from TCliente import Cliente
from TCarrito import Carrito
from TProducto import Producto
from TVentaProducto import poner_producto_en_venta
#from api_cliente import generar_factura

def menu_log():
    print('1. Registrarse')
    opc_log = 0
    try:
        while opc_log !=1:
            opc_log = int(input('Regístrate '))
    except ValueError:
        print('Error. Introduce un número válido')
    return opc_log

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
        while opc < 1 or opc > 10:
            opc = int(input('Selecciona una opción válida: '))
    except ValueError:
        print('Error. Introduce un número válido')
    return opc

def main():
    opc_log = menu_log()
    client = None

    if opc_log == 1:
        nombre = input('Introduce tu nombre: ')
        ape1 = input('Introduce tu primer apellido: ')
        ape2 = input('Introduce tu segundo apellido: ')
        usuario = input('Introduce tu nombre de usuario: ')
        client = Cliente(nombre, ape1, ape2, usuario)
        print(client)
        print('\n')

    elif opc_log == 2:
        usuario = input('Introduce tu nombre de usuario: ')
        client = Cliente("Nombre", "Apellido1", "Apellido2", usuario)
        print(f'Se ha iniciado sesión como {usuario}')
        print('\n')

    salir = False
    while not salir:
        opc = menu()

        if opc == 1:
            try:
                dinero = int(input('Introduce el dinero que quieres recargar: '))
                client.recargar_saldo(dinero)
            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opc == 2:
            print('1. Sí')
            print('2. No')
            try:
                opc_pre = int(input('Pasarse la cuenta a premium cuesta 100€. ¿Quieres hacerlo? '))
                if opc_pre == 1:
                    client.cuenta_a_premium()
                else:
                    prem = 'no' if not(client.cuenta_premium) else ''
                    print(f'Sigues como usuario {prem} premium')
            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opc == 3:
            print(client.carrito)
            print('1. Eliminar producto')
            print('2. Finalizar compra')
            print('3. Volver')
            try:
                opc_car = int(input('Selecciona una opción: '))
                if opc_car == 1:
                    prod_elim = input('Introduce el nombre del producto a eliminar: ')
                    cant_elim = int(input('Introduce la cantidad de este producto a eliminar: '))
                    prod_elim = Tienda.producto_clase[prod_elim]
                    client.eliminar_producto(prod_elim, cant_elim)
                elif opc_car == 2:
                    #He modificado esta parte para agregar la funcionalidad de generar factura
                    factura=client.finalizar_compra()
                    if factura == 's':
                        generar_factura(client.carrito)

                else:
                    print('Has salido del carrito')
            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opc == 4:
            print('Ver catálogo de productos:')

            print(Tienda())

            print('1. Añadir producto')
            print('2. Volver')
            try:
                opc_tie = int(input('Selecciona una opción: '))
                if opc_tie == 1:
                    prod_any = str(input('Introduce el nombre del producto a añadir: '))
                    cant_any = int(input('Introduce la cantidad de este producto a añadir: '))
                    prod_any = Tienda.producto_clase[prod_any]
                    client.comprar_producto(prod_any, cant_any)
                else:
                    print('Has salido del carrito')

            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')


            print('\n')

        elif opc == 5:
            client.mostrar_historial_compras()
            print('\n')

        elif opc == 6:
            print('--- Publicar producto en venta ---')
            try:
                nombre = input('Nombre del producto: ')
                precio = float(input('Precio (€): '))
                stock = int(input('Cantidad en stock: '))
                volumen = float(input('Volumen (cm³): '))
                peso = float(input('Peso (g): '))
                estado = input('Estado del producto ("nuevo" o "segunda mano"): ').lower()
                if estado not in ["nuevo", "segunda mano"]:
                    raise ValueError("Estado inválido. Debe ser 'nuevo' o 'segunda mano'.")
                client.vender_producto(nombre, precio, stock, volumen, peso, estado)
            except Exception as e:
                print(f"Error al añadir producto: {e}")
            print('\n')

        elif opc == 7:
            print('--- Añadir reseña a producto comprado ---')
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

        elif opc == 8:
            print('--- Ver reseñas de un producto ---')
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

        elif opc == 9:
            print("Hasta luego.")
            salir = True

main()

