class Persona:
    """
    Clase base para representar a una persona del sistema.
    """
    def __init__(self, nombre: str, apellido1: str, apellido2: str, nombre_usuario: str):
        self.nombre = nombre
        self.apellido1 = apellido1
        self.apellido2 = apellido2
        self.nombre_usuario = nombre_usuario


