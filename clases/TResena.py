
class Resenya:
    """
    Clase que representa una reseña de un producto.

    Atributos
    ----------
    usuario : str
        Nombre de usuario que realiza la reseña.
    puntuacion : int or float
        Valoración numérica del producto, entre 0 y 10.
    comentario : str
        Comentario escrito por el usuario.

    Métodos
    -------

    comprobar_puntuacion(puntuacion)
        Verifica que la puntuación esté entre 0 y 10.

    """

    def __init__(self, usuario: str, puntuacion, comentario: str):
        """
        Inicializa una nueva reseña con validación de puntuación.

        Parameters
        ----------
        usuario : str
            Nombre de usuario que hace la reseña.
        puntuacion : int or float
            Puntuación entre 0 y 10.
        comentario : str
            Comentario que acompaña la puntuación.

        """
        self.comprobar_puntuacion(puntuacion)
        self.usuario = usuario
        self.puntuacion = puntuacion
        self.comentario = comentario

    def comprobar_puntuacion(self, puntuacion):
        """
        Verifica que la puntuación esté entre 0 y 10.

        """

        if not isinstance(puntuacion, (int, float)):
            raise ValueError("La puntuación debe ser un número (int o float)")
        if not (0 <= puntuacion <= 10):
            raise ValueError("La puntuación debe estar entre 0 y 10")

    def __str__(self):

        return f"{self.usuario} valoró con {self.puntuacion}/10: {self.comentario}"