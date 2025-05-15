# crear_db.py (actualizado con contrasena)

import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            nombre_usuario TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido1 TEXT NOT NULL,
            apellido2 TEXT NOT NULL,
            saldo REAL DEFAULT 0.0,
            premium INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos y tabla 'clientes' creadas correctamente.")

if __name__ == "__main__":
    crear_base_datos()
