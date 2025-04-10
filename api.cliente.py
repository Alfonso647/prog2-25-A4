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

def mostrar_catalogo():
    """
    Muestra los productos de la tienda

    :return:

    -> Si se muestran todos los prodcutos de la tienda, 202
    -> Si la tienda esta vacía, 400

    """
    global token
    r = requests.get(f'{URL}/tienda/{producto}', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)

#-------------------------------------------------------------------------#

def añadir_reseña():
    """
    Añade una reseña a un producto
    :return:
    ->
    ->
    """
    global token
    r = requests.get(f'{URL}/producto/reseña/{producto}', headers={'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)


#---------------------------------------------------------------------------3

def cerrar_sesion():
    """
    Cierre de la sesión (elimina el token)
    :return:
    -> Cierro de sesión exitoso (token removido), 202
    -> Token ya esta en la base de datos, 400
    """
    global token
    r = requests.delete(f'{URL}/logout/{jti}', headers= {'Authorization': 'Bearer ' + token})
    print(r.status_code)
    print(r.text)

#--------------------------------------    -------------------------------------#

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
        print("9.Generar factura")

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

if __name__ = __'main__'
    menu()


