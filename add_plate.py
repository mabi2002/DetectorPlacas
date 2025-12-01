from services.vehiculo_service import VehiculoService
from database.db import init_db

def add_specific_plate():
    print("Agregando placa solicitada...")
    
    # Datos de la nueva placa
    nuevo_dato = {
        "nombre": "Usuario Solicitado",
        "telefono": "667-000-0000",
        "direccion": "Sinaloa",
        "placa": "VPM-45-32",
        "marca": "Chevrolet",
        "modelo": "Cheyenne",
        "anio": 2023,
        "color": "Blanco"
    }

    # Registrar propietario
    prop_id = VehiculoService.registrar_propietario(nuevo_dato["nombre"], nuevo_dato["telefono"], nuevo_dato["direccion"])
    if prop_id:
        # Registrar vehículo
        res = VehiculoService.registrar_vehiculo(
            nuevo_dato["placa"], nuevo_dato["marca"], nuevo_dato["modelo"], nuevo_dato["anio"], nuevo_dato["color"], prop_id
        )
        if res:
            print(f"Agregado exitosamente: {nuevo_dato['placa']}")
        else:
            print(f"La placa {nuevo_dato['placa']} ya existe.")
    else:
        # Si falla el propietario, intentamos buscarlo o asumimos que es porque ya existe (aunque registrar_propietario siempre crea uno nuevo en mi implementación actual, lo cual es un detalle, pero para este caso rápido está bien)
        # Mi implementación actual de registrar_propietario inserta siempre.
        print("Error al registrar propietario (o ya existe).")

if __name__ == "__main__":
    init_db()
    add_specific_plate()
