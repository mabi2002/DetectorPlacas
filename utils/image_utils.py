import cv2
import numpy as np

def preprocess_for_ocr(image):
    """
    Aplica preprocesamiento a una imagen (ROI de placa) para mejorar la precisión del OCR.
    Pasos: Escala de grises -> Aumento de contraste -> (Opcional) Binarización
    """
    if image is None or image.size == 0:
        return image

    # 1. Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Reducción de ruido (Gaussian Blur suave)
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # 3. Mejora de contraste (Histogram Equalization o CLAHE)
    # CLAHE (Contrast Limited Adaptive Histogram Equalization) suele funcionar mejor para iluminación variable
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    # 4. Binarización (Opcional, a veces EasyOCR prefiere solo grises)
    # _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return enhanced

def crop_plate(frame, box):
    """
    Recorta la región de la placa de la imagen original usando las coordenadas [x1, y1, x2, y2].
    """
    x1, y1, x2, y2 = map(int, box)
    h, w = frame.shape[:2]
    
    # Asegurar límites dentro de la imagen
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)
    
    return frame[y1:y2, x1:x2]
