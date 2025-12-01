import cv2
import numpy as np
from ultralytics import YOLO
import easyocr
from utils import image_utils

class LicensePlateDetector:
    def __init__(self, model_path='yolov8n.pt', gpu=False):
        """
        Inicializa el detector con un modelo YOLO y EasyOCR.
        :param model_path: Ruta al modelo YOLO (.pt). Se recomienda usar un modelo entrenado para matrículas.
                           Si se usa yolov8n.pt (COCO), detectará coches, no matrículas específicamente.
        :param gpu: Booleano para usar GPU en EasyOCR.
        """
        print(f"Cargando modelo YOLO desde {model_path}...")
        self.model = YOLO(model_path)
        print("Cargando EasyOCR...")
        self.reader = easyocr.Reader(['en'], gpu=gpu)

    def detect_and_read(self, frame, conf_threshold=0.25):
        """
        Detecta objetos (idealmente matrículas) y lee el texto.
        :param frame: Imagen (numpy array) BGR.
        :return: Lista de diccionarios con 'box', 'text', 'score'.
        """
        results = self.model(frame, conf=conf_threshold)
        detections = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                cls = int(box.cls[0])
                
                # Recortar la región detectada (ROI)
                roi = frame[y1:y2, x1:x2]
                
                # Preprocesamiento para OCR usando utilidades
                processed_roi = image_utils.preprocess_for_ocr(roi)
                
                # Leer texto con EasyOCR
                # detail=0 devuelve solo el texto, pero queremos confianza también, así que usamos default
                ocr_results = self.reader.readtext(processed_roi)
                
                detected_text = ""
                text_conf = 0.0
                
                # Concatenar texto detectado si hay múltiples líneas o fragmentos
                for (_, text, prob) in ocr_results:
                    if prob > 0.2: # Umbral de confianza de OCR
                        detected_text += text + " "
                        text_conf = prob # Tomamos la última o promedio (simplificado)

                detected_text = detected_text.strip().upper()
                
                # Filtrar textos muy cortos o ruido
                if len(detected_text) > 3:
                    detections.append({
                        'box': (x1, y1, x2, y2),
                        'text': detected_text,
                        'detection_score': confidence,
                        'ocr_score': text_conf,
                        'class_id': cls
                    })
        
        return detections
