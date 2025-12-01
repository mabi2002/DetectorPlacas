from services.vehiculo_service import VehiculoService
from database.db import init_db

def seed_sinaloa_plates():
    print("Insertando placas de Sinaloa de ejemplo...")
    
    # Datos de ejemplo
    datos = [
        {
            "nombre": "Miguel Barraza",
            "telefono": "667-000-0001",
            "direccion": "Domicilio Las Vegas",
            "placa": "VGB-355-A",
            "marca": "Chevrolet",
            "modelo": "Aveo",
            "anio": 2021,
            "color": "Azul"
        },
        {
            "nombre": "Juan Pérez (Sinaloa)",
            "telefono": "667-123-4567",
            "direccion": "Col. Centro, Culiacán",
            "placa": "VSA-1234",
            "marca": "Toyota",
            "modelo": "Hilux",
            "anio": 2020,
            "color": "Blanco"
        },
        {
            "nombre": "María López (Sinaloa)",
            "telefono": "668-987-6543",
            "direccion": "Zona Dorada, Mazatlán",
            "placa": "VLX-5678",
            "marca": "Nissan",
            "modelo": "Sentra",
            "anio": 2019,
            "color": "Gris"
        },
        {
            "nombre": "Carlos Ramos (Sinaloa)",
            "telefono": "687-555-1122",
            "direccion": "Centro, Guasave",
            "placa": "VRG-9012",
            "marca": "Ford",
            "modelo": "Lobo",
            "anio": 2022,
            "color": "Rojo"
        }
    ]

    for d in datos:
        # Registrar propietario
        prop_id = VehiculoService.registrar_propietario(d["nombre"], d["telefono"], d["direccion"])
        if prop_id:
            # Registrar vehículo
            res = VehiculoService.registrar_vehiculo(
                d["placa"], d["marca"], d["modelo"], d["anio"], d["color"], prop_id
            )
            if res:
                print(f"Agregado: {d['placa']} - {d['nombre']}")
            else:
                print(f"La placa {d['placa']} ya existía o hubo un error.")
        else:
            print(f"Error al agregar propietario {d['nombre']}")

if __name__ == "__main__":
    # Asegurar que la BD existe
    init_db()
    seed_sinaloa_plates()
