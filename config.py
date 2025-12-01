import os

# Rutas de Archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
DEFAULT_MODEL_PATH = os.path.join(MODEL_DIR, 'lp_detector.pt')

# Base de Datos
DB_PATH = os.path.join(BASE_DIR, 'database', 'sistema_placas.db')

# Capturas
CAPTURES_DIR = os.path.join(BASE_DIR, 'capturas')

# Configuración de Detección
CONF_THRESHOLD = 0.25
OCR_CONF_THRESHOLD = 0.2
