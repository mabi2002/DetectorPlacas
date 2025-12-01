import unittest
import os
import sqlite3
import sys

# Agregar el directorio raíz al path para poder importar services y database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.vehiculo_service import VehiculoService
from database.db import init_db, get_db_connection

class TestSistemaPlacas(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial antes de todas las pruebas"""
        # Usar una BD de prueba si fuera necesario, pero por simplicidad usaremos la principal
        # asegurándonos de no borrar datos críticos o usando transacciones revertidas.
        # Para este ejemplo escolar, reinicializamos la BD (CUIDADO en prod).
        if os.path.exists('database/sistema_placas.db'):
            os.remove('database/sistema_placas.db')
        init_db()

    def test_1_registro_propietario(self):
        """Prueba el registro de un nuevo propietario"""
        prop_id = VehiculoService.registrar_propietario("Juan Perez", "555-0101", "Calle Falsa 123")
        self.assertIsNotNone(prop_id)
        self.assertIsInstance(prop_id, int)
        print(f"Propietario registrado con ID: {prop_id}")

    def test_2_registro_vehiculo(self):
        """Prueba el registro de un vehículo asociado a un propietario"""
        # Asumimos que el ID 1 existe del test anterior
        res = VehiculoService.registrar_vehiculo("TEST-001", "Toyota", "Corolla", 2020, "Rojo", 1)
        self.assertIsNotNone(res)
        print(f"Vehículo registrado con ID: {res}")

    def test_3_busqueda_placa(self):
        """Prueba la búsqueda de un propietario por placa"""
        resultado = VehiculoService.buscar_propietario_por_placa("TEST-001")
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['nombre'], "Juan Perez")
        self.assertEqual(resultado['marca'], "Toyota")
        print("Búsqueda de placa exitosa.")

    def test_4_busqueda_placa_inexistente(self):
        """Prueba la búsqueda de una placa que no existe"""
        resultado = VehiculoService.buscar_propietario_por_placa("XYZ-999")
        self.assertIsNone(resultado)
        print("Manejo de placa inexistente correcto.")

if __name__ == '__main__':
    unittest.main()
