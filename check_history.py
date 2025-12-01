from database.db import get_db_connection

def ver_historial_lecturas():
    conn = get_db_connection()
    try:
        # Consulta uniendo lecturas con vehiculos y propietarios para ver si hubo vinculación
        query = """
        SELECT 
            l.id,
            l.placa_detectada,
            l.fecha,
            l.coincidencia as ocr_confianza,
            v.placa as placa_real,
            p.nombre as propietario
        FROM lecturas l
        LEFT JOIN vehiculos v ON l.vehiculo_id = v.id
        LEFT JOIN propietarios p ON v.propietario_id = p.id
        ORDER BY l.fecha DESC
        LIMIT 10
        """
        
        rows = conn.execute(query).fetchall()
        
        print("\n--- ÚLTIMAS 10 LECTURAS REGISTRADAS ---")
        print(f"{'FECHA':<20} | {'PLACA DETECTADA':<15} | {'ESTADO':<15} | {'PROPIETARIO'}")
        print("-" * 80)
        
        for row in rows:
            fecha = row['fecha']
            detectada = row['placa_detectada']
            propietario = row['propietario']
            
            if propietario:
                estado = "✅ VINCULADO"
                prop_info = propietario
            else:
                estado = "❌ DESCONOCIDO"
                prop_info = "---"
                
            print(f"{fecha:<20} | {detectada:<15} | {estado:<15} | {prop_info}")
            
    except Exception as e:
        print(f"Error consultando historial: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    ver_historial_lecturas()
