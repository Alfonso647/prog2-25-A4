# prog2-25-A4

# Tienda Online (Amazon)
[//]: #  Nuestra aplicación trata de emular una web de compra/venta de productos. Cumple distitnas funcionalidades
de este tipo de web como ver productos, añadir productos a un carrito... La aplicación cuenta con una base de datos
usando API Flask para guardar los usuarios actuales

## Autores

* (Coordinador) [Alfonso Íñiguez Cortés](https://github.com/Alfonso647)
* [Lucía González Mandler ](https://github.com/luciagm06)
* [Marcos Hernández Juárez ](https://github.com/marcoshj8)
* [Linxi Jiang ](https://github.com/Linxi_Jiang)
* [Darío Marimón Sánchez ](https://github.com/dariomarimonn)

## Profesor
[Miguel A. Teruel](https://github.com/materuel-ua)

## Requisitos
[//]: Requisitos de nuestra página:
* Permitirá darse de alta/baja, acceso y tipo de usuarios (Marcos)
* Se creará una base de datos de productos y tipos de productos (Alfonso)
* Se implementará un sistema de reseñas para valorar cada producto (Lucía) 
* Los productos contendrán una imagen acorde con su descripción (Darío) 
* Al hacer la compra se generará la factura/recibo en PDF (Linxi)
* Habrá una recomendación basada en la consulta de productos (Marcos) 
* Usar una API para obtener información detallada sobre un producto (Linxi) 
* Habrá una búsqueda filtrada por atributos que pueda tener un producto, como precio, ofertas, reseñas o el tipo de este (Alfonso)
* Posibilidad de poner productos a la venta (depende del tipo de usuario en una categoría “nuevo” o “segunda mano”) (Lucía)
* Antes de iniciar la búsqueda filtrada tendrás la opción de ver los productos más populares (Darío) 


## Instrucciones de instalación y ejecución
[//]: # Instalar librerías usando el fichero requirements.txt y ejecutar example.py

## Resumen de la API
[//]: # Llamadas de la API (breve descripción)
-> SingUp (permite registrarse con nombre y contraseña usando una base de datos)
-> SingIn (permite iniciar sesión)
-> LogOut (permite cerrar la sesión del usuario actual)
[//]: # Opciones del menu textual (todas las opciones son llamadas de la API)
-> Registrarse (comprueba si ya existe el usuario/contraseña y los añade a la base de datos)
-> Iniciar sesión (comprueba si el usuario y contraseña dados por el usuario existen en la base de datos)
-> Hacer Premium (hace premium al cliente (0$ por gastos de envío))
-> Añadir al carrito (añade productos al carrito del cliente que se encuentre en la sesión actual)
-> Ver carrito (muestra todos los objetos del carrito del cliente actual)
-> Añadir saldo (añade saldo ($) al cliente de la sesión)

