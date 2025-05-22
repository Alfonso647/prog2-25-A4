class Persona:
    """
    Clase base para representar a una persona del sistema.
    """
    def __init__(self, nombre: str, contrasenya: str, saldo: float) -> None:
        self.nombre = nombre
        self.contrasenya = contrasenya
        self.saldo = saldo