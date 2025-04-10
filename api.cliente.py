"""
Cliente de prueba para la API de la tienda.

Permite probar funcionalidades como:
- Iniciar/cerrar sesión
- Gestión de usuarios y productos
- Gestión del carrito
- Generar facturas

Librerías necesarias:
---------------------
- requests

URL base de la API:
-------------------
http://127.0.0.1:5000

Uso:
----
>> python api_cliente.py
"""

import requests

URL = 'http://127.0.0.1:5000'
token = ''


def test_server():
    r = requests.get(URL)
    print(r.status_code)
    print(r.text)


def leer_producto(producto):
    global token
    payload={'carrito':carrito}
    r = requests.post(f'{URL}/factura/', json=payload, headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


def vaciar_carrito(carrito):
    global token
    r = requests.delete(f'{URL}/carrito/{carrito}', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


def crear_cuenta(user, password):
    r = requests.post(f'{URL}/signup', json={'username': user, 'password': password})
    print(r.status_code)
    print(r.text)


def iniciar_sesion(user, password):
    global token
    r = requests.post(f'{URL}/login', json={'username': user, 'password': password})
    print(r.status_code)
    print(r.text)
    if r.status_code == 202:
        token = r.json().get('access_token', '')


def generar_factura():
    global token
    r = requests.get(f'{URL}/factura', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


def eliminar_producto_carrito(producto):
    global token
    r = requests.delete(f'{URL}/carrito/delete/{producto}', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


def añadir_producto_carrito(producto):
    global token
    r = requests.post(f'{URL}/carrito/add', json={'producto': producto}, headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


def mostrar_catalogo():
    global token
    r = requests.get(f'{URL}/tienda', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


def añadir_resena(producto, texto):
    global token
    r = requests.post(f'{URL}/producto/reseña/{producto}', json={'texto': texto}, headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


def cerrar_sesion():
    global token
    r = requests.delete(f'{URL}/logout', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)
    token = ''


def menu():
    while True:
        print("\n=== MENÚ DE LA TIENDA ===")
        print("1. Comprobar servidor")
        print("2. Iniciar sesión")
        print("3. Crear cuenta")
        print("4. Ver producto")
        print("5. Ver catálogo")
        print("6. Vaciar carrito")
        print("7. Añadir producto al carrito")
        print("8. Eliminar producto del carrito")
        print("9. Generar factura")
        print("10. Añadir reseña")
        print("11. Cerrar sesión")
        print("0. Salir")

        choice = input('Opción: ')

        if choice == '1':
            test_server()
        elif choice == '2':
            usuario = input('Usuario: ')
            contraseña = input('Contraseña: ')
            iniciar_sesion(usuario, contraseña)
        elif choice == '3':
            while True:
                usuario = input('Nuevo usuario: ')
                pass1 = input('Contraseña: ')
                pass2 = input('Confirmar contraseña: ')
                if pass1 == pass2:
                    crear_cuenta(usuario, pass1)
                    break
                else:
                    print("Las contraseñas no coinciden.")
        elif choice == '4':
            producto = input('Nombre del producto: ')
            leer_producto(producto)
        elif choice == '5':
            mostrar_catalogo()
        elif choice == '6':
            carrito = input('ID del carrito: ')
            vaciar_carrito(carrito)
        elif choice == '7':
            producto = input('Producto a añadir: ')
            añadir_producto_carrito(producto)
        elif choice == '8':
            producto = input('Producto a eliminar: ')
            eliminar_producto_carrito(producto)
        elif choice == '9':
            generar_factura()
        elif choice == '10':
            producto = input('Producto para reseñar: ')
            texto = input('Escribe tu reseña: ')
            añadir_resena(producto, texto)
        elif choice == '11':
            cerrar_sesion()
        elif choice == '0':
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")


if __name__ == '__main__':
    menu()
