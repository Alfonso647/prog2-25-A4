import requests

URL = 'http://localhost:5000'
token_actual = None  # Variable global para guardar el token JWT

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
        menu_usuario_autenticado()
    else:
        print("❌ Error:", datos.get('mensaje', 'Credenciales incorrectas'))


def cerrar_sesion():
    global token_actual
    token_actual = None
    print("🔒 Sesión cerrada. Volviendo al menú principal.")

def menu_usuario_autenticado():
    while True:
        print("\n=== MENÚ DE USUARIO AUTENTICADO ===")
        print("1. Nada")
        print("2. Nada")
        print("3. Nada")
        print("4. Nada")
        print("5. Nada")
        print("6. Nada")
        print("7. Nada")
        print("8. Nada")
        print("9. Cerrar sesión")

        opcion = input("Seleccione una opción (1-9): ")

        if opcion == '9':
            cerrar_sesion()
            break
        elif opcion in map(str, range(1, 9)):
            print(f"👉 Has seleccionado la opción {opcion}, aún no implementada.")
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