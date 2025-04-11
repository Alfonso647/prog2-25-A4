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