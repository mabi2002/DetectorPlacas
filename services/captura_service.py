from model.detector import LicensePlateDetector
from services.vehiculo_service import VehiculoService
import cv2
import os
from datetime import datetime, timezone, timedelta
import config

class CapturaService:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = config.DEFAULT_MODEL_PATH
            
        self.detector = LicensePlateDetector(model_path=model_path)
        self.save_dir = config.CAPTURES_DIR
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            
        self.last_capture_time = {} # Diccionario para controlar frecuencia de capturas {placa: timestamp}
        self.cooldown_seconds = 10  # Tiempo de espera entre capturas de la misma placa

    def procesar_frame(self, frame):
        """
        Procesa un frame: detecta placas, busca en BD y registra lecturas.
        """
        detections = self.detector.detect_and_read(frame)
        resultados = []
        # Usar zona horaria de Chihuahua (UTC-7)
        chihuahua_tz = timezone(timedelta(hours=-7))
        current_time = datetime.now(chihuahua_tz)

        for det in detections:
            placa_texto = det['text']
            box = det['box']
            score = det['ocr_score']
            
            # Verificar si debemos guardar (Debounce)
            should_save = True
            if placa_texto in self.last_capture_time:
                time_diff = (current_time - self.last_capture_time[placa_texto]).total_seconds()
                if time_diff < self.cooldown_seconds:
                    should_save = False
            
            # Buscar en BD
            info_vehiculo = VehiculoService.buscar_propietario_por_placa(placa_texto)
            
            resultado = {
                'placa': placa_texto,
                'box': box,
                'score': score,
                'propietario': None,
                'alerta': False
            }

            if info_vehiculo:
                resultado['propietario'] = info_vehiculo
                
                if should_save:
                    # Registrar lectura
                    timestamp_str = current_time.strftime("%Y%m%d_%H%M%S")
                    img_name = f"{self.save_dir}/placa_{placa_texto}_{timestamp_str}.jpg"
                    
                    # Guardar solo el recorte de la placa
                    x1, y1, x2, y2 = box
                    plate_img = frame[y1:y2, x1:x2]
                    try:
                        cv2.imwrite(img_name, plate_img)
                        VehiculoService.registrar_lectura(
                            info_vehiculo['vehiculo_id'], 
                            placa_texto, 
                            img_name, 
                            score,
                            fecha=current_time
                        )
                        self.last_capture_time[placa_texto] = current_time
                        print(f"Captura guardada: {placa_texto}")
                    except Exception as e:
                        print(f"Error guardando imagen: {e}")
            else:
                # Placa no encontrada: Registramos como alerta/desconocido
                resultado['alerta'] = True
                
                if should_save:
                    # Guardar imagen y registro para análisis posterior
                    timestamp_str = current_time.strftime("%Y%m%d_%H%M%S")
                    img_name = f"{self.save_dir}/desconocido_{placa_texto}_{timestamp_str}.jpg"
                    x1, y1, x2, y2 = box
                    plate_img = frame[y1:y2, x1:x2]
                    
                    try:
                        cv2.imwrite(img_name, plate_img)
                        # Registramos con vehiculo_id = None
                        VehiculoService.registrar_lectura(
                            None, 
                            placa_texto, 
                            img_name, 
                            score,
                            fecha=current_time
                        )
                        self.last_capture_time[placa_texto] = current_time
                        print(f"Alerta guardada: {placa_texto}")
                    except Exception as e:
                        print(f"Error guardando desconocido: {e}")
            
            resultados.append(resultado)
            
        return resultados
