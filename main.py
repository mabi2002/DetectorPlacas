import cv2
import sys
from database.db import init_db
from services.vehiculo_service import VehiculoService
from services.captura_service import CapturaService
from utils.visualizer import draw_results

def menu():
    print("\n--- SISTEMA DE DETECCIÓN DE MATRÍCULAS ---")
    print("1. Iniciar Detección (Cámara/Video)")
    print("2. Registrar Nuevo Vehículo")
    print("3. Ver Propietarios Registrados")
    print("4. Salir")
    return input("Seleccione una opción: ")

def registrar_vehiculo_interactivo():
    print("\n--- Registro de Vehículo ---")
    nombre = input("Nombre del Propietario: ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    
    prop_id = VehiculoService.registrar_propietario(nombre, telefono, direccion)
    
    if prop_id:
        placa = input("Placa (ej. ABC-123): ").upper()
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        anio = input("Año: ")
        color = input("Color: ")
        
        res = VehiculoService.registrar_vehiculo(placa, marca, modelo, anio, color, prop_id)
        if res:
            print("Vehículo registrado exitosamente.")
        else:
            print("Error al registrar vehículo.")
    else:
        print("Error al registrar propietario.")

def ver_propietarios():
    from database.db import get_db_connection
    conn = get_db_connection()
    rows = conn.execute("SELECT p.nombre, v.placa, v.marca FROM propietarios p JOIN vehiculos v ON p.id = v.propietario_id").fetchall()
    print("\n--- Vehículos Registrados ---")
    for row in rows:
        print(f"Propietario: {row['nombre']} | Placa: {row['placa']} | Vehículo: {row['marca']}")
    conn.close()

import config

def iniciar_deteccion():
    source = input("Ingrese fuente de video (0 para webcam, o ruta de archivo): ")
    if source == '0':
        source = 0
    
    default_model = config.DEFAULT_MODEL_PATH
    print(f"Modelo detectado: {default_model}")
    model_path = input("Presione ENTER para usar este modelo (o escriba otra ruta): ")
    
    if not model_path:
        model_path = default_model
    
    print(f"Cargando modelo desde: {model_path}")
    service = CapturaService(model_path=model_path)
    
    cap = cv2.VideoCapture(source)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Procesar frame
        resultados = service.procesar_frame(frame)
        
        # Dibujar resultados
        frame = draw_results(frame, resultados)
        
        cv2.imshow('Detector de Placas', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    init_db()
    
    while True:
        opcion = menu()
        
        if opcion == '1':
            iniciar_deteccion()
        elif opcion == '2':
            registrar_vehiculo_interactivo()
        elif opcion == '3':
            ver_propietarios()
        elif opcion == '4':
            sys.exit()
        else:
            print("Opción no válida.")
