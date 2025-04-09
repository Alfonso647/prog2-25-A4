from TTienda import Tienda
from TCliente import Cliente
from TCarrito import Carrito
from TProd import Producto

#Este menú es lo primero que aparece y en el que introduces tu cuenta. Te registras si es nueva e inicias sesión si hay una con los mismos datos que la ya creada. Ambas te llevan al menú, 
def menu_log():
    print('1. Registrarse')
    print('2. Iniciar sesión')

    opc_log=0

    try:
        while opc_log<1 or opc_log>2:
            opc_log=int(input('¿Tienes cuenta? '))
    except ValueError:
        print('Error. Introduce un número válido')
    
    return opc_log

'''
En este segundo menú encontramos lo que puede hacerse en cada opción. 
La mayoría de las opciones hacen la función que dicen en sus nombres y 
están implementadas como métodos de clases.
'''
def menu():
    print('1. Recargar saldo')
    print('2. Pasarse a premium')
    print('3. Ver carrito') #Además de ver el carrito, permite eliminar productos o finalizar la compra
    print('4. Catálogo de productos')
    print('5. Mostrar historial de compras') 
    print('6. Cerrar sesión') #Esta opción redirige a menu_log
    print('7. Salir') 

    try:
        opc=0
        while opc<1 or opc>7:
            opc=int(input('Selecciona una opción válida: '))
    except ValueError:
        print('Error. Introduce un número válido')

    return opc


def main():
    opc_log=menu_log()
    print(opc_log)


    #Introduces los datos del cliente para que se cree el atributo "client", desde el que se ejecutarán las demás opciones
    if opc_log==1:
        nombre=input('Introduce tu nombre: ')
        ape1=input('Introduce tu primer apellido: ')
        ape2=input('Introduce tu segundo apellido: ')
        usuario=input('Introduce tu nombre de usuario: ')

        client = Cliente(nombre, ape1, ape2, usuario)

        print(client)
        print('\n')

    
    #Inicia un bucle hasta que la variable "salir" se ponga en "True" para poder ejecutar todas las funciones que queramos en una llamada
    salir=False
    while salir==False:
        opc=menu()
        #Introduces el dinero a recargar para poder comprar y ejecuta la función correspondiente
        if opc==1:

            try:

                dinero=int(input('Introduce el dinero que quieres recargar: '))

            except ValueError:
                print('Error. Introduce un número válido')

            else:
                client.recargar_saldo(dinero)
            print('\n')

        #Como pasarse a premium cuesta dinero, antes tienes que asegurar que es la acción que quieres hacer. Después puede llamarse a la función que te hace premium
        elif opc==2:
            print('1. Sí')
            print('2. No')
            opc_pre=0
            try:
                while opc_pre<1 or opc_pre>2:
                    opc_pre=int(input('Pasarse la cuenta a premium cuesta 100€. ¿Quieres hacerlo? '))
            except ValueError:
                print('Error. Introduce un número válido')
            else:
                if opc_pre==1:
                    client.cuenta_a_premium()
                else:
                    print('Sigues como usuario no premium')

            print('\n')

        
        
        #En esta opción hay tres "subopciones": puedes eliminar un producto eligiendo el producto y su cantidad, puedes acabar la compra o puedes volver al menú principal
        elif opc==3:
            print(client.carrito)
            print('1. Eliminar producto')
            print('2. Finalizar compra')
            print('3. Volver')
            opc_car=0
            try:
                while opc_car<1 or opc_car>3:
                    opc_car=int(input('Selecciona una opción: '))
            except ValueError:
                print('Error. Introduce un número válido')
            else:

                if opc_car==1:
                    prod_elim=input('Introduce el nombre del producto a eliminar: ')
                    try:
                        cant_elim=int(input('Introduce la cantidad de este producto a eliminar: '))
                    except ValueError:
                        print('Error. Introduce un número válido')

                    client.eliminar_producto(prod_elim,cant_elim)
                elif opc_car==2:
                    client.finalizar_compra()

                else:
                    print('Has salido del carrito')
            print('\n')

        
        elif opc==4:
            print('Ver catálogo de productos') #ponerlo bien !! para esto igual se necesita la api no estoy seguro
            print('\n')
        
        #Esta opción simplemente muestra el historial de compras
        elif opc==5:
            client.mostrar_historial_compras()
            print('\n')

        elif opc==6:
            print('m')
            print('\n')

        #Esta última opción marca la variable "salir" como verdadera, lo que hace que se termine el bucle
        else:
            salir=True
        
main()

