import sqlite3
from database.db import get_db_connection

class VehiculoService:
    @staticmethod
    def registrar_propietario(nombre, telefono, direccion):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO propietarios (nombre, telefono, direccion) VALUES (?, ?, ?)",
                (nombre, telefono, direccion)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al registrar propietario: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def registrar_vehiculo(placa, marca, modelo, anio, color, propietario_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO vehiculos (placa, marca, modelo, anio, color, propietario_id) VALUES (?, ?, ?, ?, ?, ?)",
                (placa, marca, modelo, anio, color, propietario_id)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: La placa {placa} ya existe.")
            return None
        except Exception as e:
            print(f"Error al registrar vehículo: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def buscar_propietario_por_placa(placa):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Buscamos coincidencias exactas o parciales (LIKE)
        # Limpiamos la placa de espacios para la búsqueda
        placa_clean = placa.replace(" ", "").replace("-", "")
        
        query = """
        SELECT p.nombre, p.telefono, p.direccion, v.marca, v.modelo, v.color, v.id as vehiculo_id
        FROM vehiculos v
        JOIN propietarios p ON v.propietario_id = p.id
        WHERE REPLACE(REPLACE(v.placa, ' ', ''), '-', '') = ?
        """
        row = cursor.execute(query, (placa_clean,)).fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None

    @staticmethod
    def registrar_lectura(vehiculo_id, placa_detectada, imagen_ruta, coincidencia):
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO lecturas (vehiculo_id, placa_detectada, imagen_ruta, coincidencia) VALUES (?, ?, ?, ?)",
                (vehiculo_id, placa_detectada, imagen_ruta, coincidencia)
            )
            conn.commit()
        except Exception as e:
            print(f"Error al registrar lectura: {e}")
        finally:
            conn.close()
