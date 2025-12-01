import cv2

def draw_results(frame, results):
    for res in results:
        x1, y1, x2, y2 = res['box']
        placa = res['placa']
        
        color = (0, 255, 0) # Verde si encontrado
        label = f"{placa}"
        
        if res['propietario']:
            prop = res['propietario']
            label += f" | {prop['nombre']}"
        else:
            color = (0, 0, 255) # Rojo si no encontrado
            label += " | DESCONOCIDO"
            
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        
        # Fondo para texto
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
        cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return frame
