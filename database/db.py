import sqlite3
import os

DB_PATH = 'database/sistema_placas.db'
SCHEMA_PATH = 'database/schema.sql'

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos SQLite.
    Configura row_factory para acceder a columnas por nombre.
    :return: Objeto de conexión sqlite3.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa la base de datos si no existe.
    Crea el directorio 'database' y ejecuta el script SQL de esquema.
    """
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = get_db_connection()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

if __name__ == '__main__':
    init_db()
