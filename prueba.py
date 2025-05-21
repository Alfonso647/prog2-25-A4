from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os

# RUTA ABSOLUTA - AJUSTADA A TU SISTEMA
ruta_db = 'C:/Users/Xiaoy/OneDrive/Documents/ejercicio_github/instance/base_de_datos.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{ruta_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if not os.path.exists(ruta_db):
    print(f"❌ El archivo no existe: {ruta_db}")
else:
    with app.app_context():
        inspector = inspect(db.engine)
        columnas = inspector.get_columns('usuario')

        print("📋 Columnas en la tabla 'usuario':")
        for columna in columnas:
            print(f"- {columna['name']} ({columna['type']})")
