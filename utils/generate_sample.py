import cv2
import numpy as np
import os

def create_dummy_plate(text="ABC-123", filename="ejemplo_placa.jpg"):
    """
    Crea una imagen sintética de una matrícula para pruebas.
    """
    # Crear fondo blanco
    width, height = 400, 200
    img = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Dibujar borde negro (marco de la placa)
    cv2.rectangle(img, (10, 10), (width-10, height-10), (0, 0, 0), 5)
    
    # Configurar fuente
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3
    thickness = 5
    color = (0, 0, 0)
    
    # Obtener tamaño del texto para centrarlo
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    
    # Escribir texto
    cv2.putText(img, text, (text_x, text_y), font, font_scale, color, thickness)
    
    # Guardar
    if not os.path.exists('ejemplos'):
        os.makedirs('ejemplos')
        
    path = os.path.join('ejemplos', filename)
    cv2.imwrite(path, img)
    print(f"Imagen de prueba generada: {path}")
    return path

if __name__ == "__main__":
    create_dummy_plate("TEST-001", "placa_test_001.jpg")
    create_dummy_plate("XYZ-999", "placa_desconocida.jpg")
