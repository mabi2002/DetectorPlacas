import sqlite3
import os

DB_PATH = 'database/sistema_placas.db'

def remove_plate(placa):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar si existe
    cursor.execute("SELECT id FROM vehiculos WHERE placa = ?", (placa,))
    row = cursor.fetchone()
    
    if row:
        print(f"Eliminando vehículo con placa {placa}...")
        cursor.execute("DELETE FROM vehiculos WHERE placa = ?", (placa,))
        conn.commit()
        print("Eliminado correctamente.")
    else:
        print(f"La placa {placa} no existía.")
        
    conn.close()

if __name__ == "__main__":
    remove_plate("VGB-355-A")
