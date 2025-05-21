import requests

URL = 'http://localhost:5000'
token_actual = None  # Token JWT guardado después de iniciar sesión

def registrarse():
    print("📝 Registrarse")
    nombre = input("Nombre de usuario: ")
    contrasenya = input("Contraseña: ")

    respuesta = requests.post(f'{URL}/registrarse', json={
        'nombre_usuario': nombre,
        'contrasenya': contrasenya
    })

    print(respuesta.json().get('mensaje', 'Error desconocido'))

def iniciar_sesion():
    global token_actual
    print("🔐 Iniciar sesión")
    nombre = input("Nombre de usuario: ")
    contrasenya = input("Contraseña: ")

    respuesta = requests.post(f'{URL}/iniciar_sesion', json={
        'nombre_usuario': nombre,
        'contrasenya': contrasenya
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

def recargar_saldo():
    if not token_actual:
        print("⚠️ Debe iniciar sesión primero.")
        return

    try:
        cantidad = float(input("💰 Ingrese la cantidad a recargar: "))
    except ValueError:
        print("❌ Error: Debe ingresar un número válido.")
        return

    headers = {'Authorization': f'Bearer {token_actual}'}
    respuesta = requests.post(f"{URL}/recargar_saldo", json={'cantidad': cantidad}, headers=headers)

    try:
        mensaje = respuesta.json().get('mensaje', 'Respuesta inesperada')
        print(mensaje)
    except Exception:
        print("❌ El servidor no devolvió JSON. Detalles:")
        print("Código:", respuesta.status_code)
        print("Texto:", respuesta.text)


def menu_usuario_autenticado():
    while True:
        print("\n=== MENÚ DE USUARIO AUTENTICADO ===")
        print("1. Recargar saldo")
        print("2. Nada")
        print("3. Nada")
        print("4. Nada")
        print("5. Nada")
        print("6. Nada")
        print("7. Nada")
        print("8. Nada")
        print("9. Cerrar sesión")

        opcion = input("Seleccione una opción (1-9): ")

        if opcion == '1':
            recargar_saldo()
        elif opcion == '9':
            cerrar_sesion()
            break
        elif opcion in map(str, range(2, 9)):
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
