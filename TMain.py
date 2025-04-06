from TTienda import Tienda, Producto
from TCliente import Cliente
from TCarrito import Carrito

mi_tienda = Tienda()

producto1 = Producto("PlayStation 5", 499.99, 15, 3900, 4500, True)
producto2 = Producto("iPhone 15 Pro", 1099.00, 8, 200, 187, True)
producto3 = Producto("Zapatillas Nike Air", 129.95, 30, 3500, 800)
producto4 = Producto("Portátil Gaming", 1499.00, 5, 3800, 2400, True)
producto5 = Producto("Smart TV 65", 799.50, 12, 25000, 18200, True)
producto6 = Producto("Cafetera Nespresso", 99.99, 25, 1500, 2100)
producto7 = Producto("Reloj Casio G-Shock", 89.90, 40, 500, 72)
producto8 = Producto("Altavoz JBL", 129.00, 18, 1200, 1100, True)
producto9 = Producto("Mochila North Face", 79.95, 35, 10000, 950)
producto10 = Producto("Teclado Mecánico", 59.50, 22, 800, 620)


print(producto9) #__str__ de producto
print()
print(mi_tienda) #muestra tienda
mi_tienda.reponer_stock() #repone stock
print(mi_tienda)#comprobamos


yo = Cliente('Pepe','Pérez','LLopis','Pepito50') #cliente yo
print(yo)
yo.comprar_producto(producto1,100) #mas stock del que hay
print()
print(yo.carrito)#carrito vacío
print()

yo.comprar_producto(producto1,1)
yo.comprar_producto(producto1,70)#sobrepasa el stock
yo.comprar_producto(producto2,1)
yo.comprar_producto(producto4,1)
yo.comprar_producto(producto3,2)
yo.comprar_producto(producto10,4)
yo.eliminar_producto(producto10,3)#probar a eliminar
print()
print(yo.carrito)
yo.eliminar_producto(producto10,1)
print()
print(yo.carrito) # ver el carrito
print()
yo.finalizar_compra() #finalizar compra, no hay dinero
print()
yo.recargar_saldo(-500)#no es poesible el valor
yo.recargar_saldo(5000)
print()
yo.finalizar_compra()#finalizar la compra
print()
print(mi_tienda)#comprobar que se ha reducido el stock
print()
yo.mostrar_historial_compras()#se muestra el historial de compras

yo.recargar_saldo(3378)
print()

yo.cuenta_a_premium()


