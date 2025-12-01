from database.db import get_db_connection
import sqlite3

class PropietarioService:
    @staticmethod
    def crear_propietario(nombre, telefono, direccion):
        """Crea un nuevo propietario y retorna su ID."""
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                "INSERT INTO propietarios (nombre, telefono, direccion) VALUES (?, ?, ?)",
                (nombre, telefono, direccion)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear propietario: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def obtener_todos():
        """Retorna una lista de todos los propietarios."""
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM propietarios").fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def obtener_por_id(id_propietario):
        """Obtiene un propietario por su ID."""
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM propietarios WHERE id = ?", (id_propietario,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def actualizar_propietario(id_propietario, nombre, telefono, direccion):
        """Actualiza los datos de un propietario existente."""
        conn = get_db_connection()
        try:
            conn.execute(
                "UPDATE propietarios SET nombre = ?, telefono = ?, direccion = ? WHERE id = ?",
                (nombre, telefono, direccion, id_propietario)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar propietario: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def eliminar_propietario(id_propietario):
        """Elimina un propietario y sus vehículos asociados (si aplica cascada o lógica manual)."""
        conn = get_db_connection()
        try:
            # Opcional: Eliminar vehículos primero si no hay ON DELETE CASCADE
            conn.execute("DELETE FROM vehiculos WHERE propietario_id = ?", (id_propietario,))
            conn.execute("DELETE FROM propietarios WHERE id = ?", (id_propietario,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar propietario: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_por_placa(placa):
        """Obtiene el propietario asociado a una placa específica."""
        conn = get_db_connection()
        # Limpieza básica de la placa para búsqueda flexible
        placa_clean = placa.replace(" ", "").replace("-", "")
        
        query = """
        SELECT p.* 
        FROM propietarios p
        JOIN vehiculos v ON p.id = v.propietario_id
        WHERE REPLACE(REPLACE(v.placa, ' ', ''), '-', '') = ?
        """
        row = conn.execute(query, (placa_clean,)).fetchone()
        conn.close()
        return dict(row) if row else None
