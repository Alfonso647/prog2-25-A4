#Importa SQLAlchemy para la gestión de la base de datos y Flask para crear la aplicación web
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#Inicializa la aplicación Flask
app = Flask(__name__)

#Configura la URI para usar una base de datos SQLite local llamada 'base_de_datos.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base_de_datos.db'

#Desactiva el seguimiento de modificaciones de SQLAlchemy (mejora el rendimiento)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Crea una instancia de SQLAlchemy con la aplicación
db = SQLAlchemy(app)

class Usuario(db.Model):
    """
    Modelo de datos que representa un usuario en la base de datos.

    Attributes
    ----------
    id : int
        Identificador único del usuario (clave primaria).
    nombre_usuario : str
        Nombre único del usuario.
    contraseña : str
        Contraseña cifrada del usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)

#Crea las tablas en la base de datos (si no existen ya)
with app.app_context():
    db.create_all()
    print("Base de datos creada correctamente.")
