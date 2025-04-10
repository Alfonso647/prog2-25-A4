from TProducto import Producto
from TTienda import Tienda
from TCliente import Cliente

def poner_producto_en_venta(cliente: Cliente, nombre: str, precio: float, stock: int,
                            volumen: float, peso: float, fragil: bool = False,
                            estado: str = "nuevo") -> Producto:
    """
    Permite a un cliente publicar un nuevo producto en venta.

    El producto creado se añade al listado de productos en venta del cliente
    y también se registra en el catálogo global de la tienda.

    Parámetros
    ----------
    cliente : Cliente
        Objeto cliente que pone el producto en venta.
    nombre : str
        Nombre del producto.
    precio : float
        Precio por unidad del producto.
    stock : int
        Número de unidades disponibles.
    volumen : float
        Volumen del producto en centímetros cúbicos.
    peso : float
        Peso del producto en gramos.
    fragil : bool, optional
        Si el producto es frágil. Por defecto es False.
    estado : str, optional
        Indica si el producto es "nuevo" o "segunda mano". Por defecto es "nuevo".
    """

    producto = Producto(nombre, precio, stock, volumen, peso, fragil, estado)
    cliente.productos_en_venta.append(producto)
    Tienda.nuevo_producto(producto)
    print(f"Producto '{nombre}' ({estado}) publicado con éxito por {cliente.nombre_usuario}.")
    return producto
