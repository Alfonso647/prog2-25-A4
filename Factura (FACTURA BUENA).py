import datetime
from typing import Dict
from TProducto import Producto
from TCliente import Cliente
from actual.TCarrito import Carrito


class Factura:
    @staticmethod
    def mostrar_factura(cliente: Cliente, productos: Carrito) -> None:
        """
        Muestra factura por pantalla Y la guarda en archivo
        Cambios:
        1. Genera contenido primero
        2. Lo muestra por pantalla
        3. Lo guarda en archivo
        """
        # Generar contenido (NUEVO)
        contenido = []
        contenido.append("\n========== FACTURA ==========")
        contenido.append(f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        contenido.append(f"Cliente: {cliente.nombre_usuario}")
        contenido.append("============================")

        # Productos
        contenido.append("Productos comprados:")
        total = 0
        for producto, cantidad in productos.items():
            subtotal = producto.precio * cantidad
            contenido.append(f"- {producto.nombre}: {cantidad} unidades x {producto.precio}€ = {subtotal}€")
            total += subtotal

        # Total
        contenido.append("============================")
        contenido.append(f"TOTAL A PAGAR: {round(total, 2)}€")
        contenido.append("============================")

        # Mostrar por pantalla (cambio mínimo)
        print('\n'.join(contenido))

        # Guardar en archivo (NUEVO)
        nombre_archivo = f"factura_{cliente.nombre_usuario}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write('\n'.join(contenido))
        print(f"\nFactura guardada como: {nombre_archivo}")


# Ejemplo de uso (igual que antes)
if __name__ == "__main__":
    cliente_ejemplo = Cliente("Juan", "Pérez", "Gómez", "juanpg")
    productos_ejemplo = {
        Producto("Camiseta básica", 15.99, 1, 0.3, 0.2): 2,
        Producto("Pantalón vaquero", 29.99, 1, 0.8, 0.5): 1
    }

    Factura.mostrar_factura(cliente_ejemplo, productos_ejemplo)