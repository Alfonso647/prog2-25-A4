"""
Srcipt de prueba para probar la api de nuestra app

Proporciona un menú con diferentes opciones para poder probar
las funcionalidades de nuestra app

Funciones principales
---------------------
-> Iniciar y cerrar sesión de usuarios
-> Gestión de usuarios
-> Gestión de productos (crear, modificar, eliminar y leer especificaciones)
-> Gestión del carrito (visualizar elementos del carrito y añadir/eliminar productos)
-> Generar facturas

Librerias
---------
requests
flask

URL de la app
--------------
http://127.0.0.1:5000

Funciones del menu
-----------------
1. Testear server
2. etc
etc (acabar)

Ejemplo de uso
---------------

>> python api.cliente.py

"""
import requests
from flask import request
URL = 'http://127.0.0.1:5000'
token = ''

#---------------------------------------------------------------#

def test_server():
    """
    Comprubea el funciomento de la app. Lo hace usando la libreria
    requests para hacer una petición get a la dirección definida en
    la variable URL

    :return:

    -> Si la app se activa y está funcionandno correctamente,
       devuelve el código de estado 202
    -> Si la app no se ha iniciado, devuelve el código de estado 400

    """
    r = request.get(URL)
    print(r)
    print(r.status_code)
    print(r.text)

#----------------------------------------------------------------#

def leer_producto(producto):
    """
    Lee un dato de nuestra api (manda una solicitud GET).
    Muestra la información del producto

    :param producto: Prodcuto del que se va a mostrar su información
    :return:

    -> Si se ha encontrado el prodcuto y se ha leído correctamente, 202
    -> Si no se ha encontrado el producto, 400
    """
    global token
    r = requests.get(f'{URL}/producto/{producto}', headers= {'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)

#---------------------------------------------------------------------#

def vaciar_carrito(carrito):
    """
    Envía solicitud de un DELETE a la API. Vacía el carrito
    :param : Carrito
    :return:
    -> Si se ha eliminado correctamente, código 202
    -> El carrito ya estaba vacío, código 400

    """
    global token
    r = requests.delete(f'{URL}/carrito/{carrito}', headers= {'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)

#---------------------------------------------------------------------------#

def crear_cuenta(user,password):
    """
    Envia
    :param user:
    :param password:
    :return:
    """
    global token
    r = requests.post(f'{URL}/data/singup,user={user}&password={password}')
    print(r.status_code)
    print(r.text)

#----------------------------------------------------------------------------#

def inicar_sesión(user,password):
    """
    Inicia sesión en la api creando un token.

    :param user: Usuario
    :param password: Contraseña
    :return:

    -> Si el usuario este registrado y se ha iniciado sesión, devuelve el código 202
    -> Si  el usuairo no esta registrado, devuelve el código de estado 409
    """
    global token
    r = requests.post(f'{URL}/data/singup,user={user}&password={password}')
    print(r.status_code)
    print(r.text)
    token = r.text

#-------------------------------------------------------------------------#

def generar_factura():
    """
    Genera y descarga una factura de un prodcuto. Envia una solicitud
    de GET a nuestra API
    :return:

    -> Si se ha generado la factura correctamente, código 202
    -> Si no se ha podido generar la factura, devuelve el código 409
    """
    global token
    r = requests.get(f'{URL}/producto/{producto}', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)

#--------------------------------------------------------------------------#

def eliminar_producto_carrito():
    """
    Elimina un producto del carrito. Se envía una solicitud DELETE a nuestra api

    :return:
    -> Si verifica que el producto estaba en el carrito y se elimina, código 200
    -> Si no se encuentra ese prodcuto en el carrito, se devuelve el código de estado 400
    """
    global token
    r = requests.delete(f'{URL}/carrito/delete/{producto}', headers= {'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)

#--------------------------------------------------------------------------#

def añadir_prodcuto_carrito():
    """
    Añade un producto al carrito. Para hacerlo se envía una petición de POST a
    la API.

    :return:

    -> Si se añade correctamente, devuelve el código de estado 202
    -> Si no se ha podido añadir, devuelve el código de estado 400
    """
    global token
    r = requests.post(f'{URL}/carrito/add,producto={producto}')
    print(r.status_code)
    print(r.text)

#---------------------------------------------------------------------------#

def menu():
    while True:
        print("\n==MENU==")
        print("1.Comprobar Servidor")
        print("2.Iniciar Sesión")
        print("3.Crear cuenta")
        print("4.Ver producto")
        print("5.Ver carrito")
        print("6.Vaciar carrito")
        print("7.Añadir producto carrito")
        print("8.Eliminar producto carrito")
        print("9. Generar factura")

        choice = input('Enter your choice: ')

        if choice == '1':
            test_server()
        if choice == '2':
            usuario = input('Introduce tu usuario: ')
            password = input('Introduce tu contraseña: ')
            inicar_sesión()
        if choice == '3':
            x = 0
            while x == 0:
                usuario = input('Introduce su nuevo usuario: ')
                password1 = input('Introdice su nueva constraseña')
                password2 = input('Confirme su constraseña: ')
                if password1 == password2:
                    crear_cuenta(usuario,password1)
                    x = 1
        if choice == '4':
            info_producto()











def menu_log():
    print('1. Registrarse')
    print('2. Iniciar sesión')
    opc_log = 0
    try:
        while opc_log < 1 or opc_log > 2:
            opc_log = int(input('¿Tienes cuenta? '))
    except ValueError:
        print('Error. Introduce un número válido')
    return opc_log

def menu():
    print('1. Recargar saldo') 
    print('2. Pasarse a premium') # !!
    print('3. Ver carrito') # también tiene finalizar compra y borrar producto
    print('4. Catálogo de productos') # también tiene añadir producto
    print('5. Mostrar historial de compras') #!!
    print('6. Publicar producto en venta') # !!
    print('7. Añadir reseña a producto comprado') #!!
    print('8. Ver reseñas de un producto') #!!
    print('9. Cerrar sesión') #!!
    print('10. Salir')
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
                    print('Sigues como usuario no premium')
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
                    client.eliminar_producto(prod_elim, cant_elim)
                elif opc_car == 2:
                    client.finalizar_compra()
                else:
                    print('Has salido del carrito')
            except ValueError:
                print('Error. Introduce un número válido')
            print('\n')

        elif opc == 4:
            print('Ver catálogo de productos:')
            print(Tienda())
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
                    client.añadir_reseña(productos[seleccion], puntuacion, comentario)
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
                    for linea in p.mostrar_reseñas():
                        print(linea)
                    encontrado = True
            if not encontrado:
                print('No se encontraron reseñas o el producto no existe.')
            print('\n')

        elif opc == 9:
            print("Sesión cerrada.")
            client = None
            opc_log = menu_log()
            if opc_log == 1:
                nombre = input('Introduce tu nombre: ')
                ape1 = input('Introduce tu primer apellido: ')
                ape2 = input('Introduce tu segundo apellido: ')
                usuario = input('Introduce tu nombre de usuario: ')
                client = Cliente(nombre, ape1, ape2, usuario)
            elif opc_log == 2:
                usuario = input('Introduce tu nombre de usuario: ')
                client = Cliente("Nombre", "Apellido1", "Apellido2", usuario)
            print('\n')

        elif opc == 10:
            print("Hasta luego.")
            salir = True

main()


