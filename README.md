# Sistema de Detección de Matrículas 🚗🔍

Este proyecto es un sistema integral para la detección de matrículas vehiculares y la identificación de sus propietarios mediante visión artificial y bases de datos.

## 📋 Descripción General

El objetivo principal es detectar matrículas en tiempo real (o video) y vincularlas con una base de datos de propietarios registrados. Utiliza **YOLOv8** para la detección de objetos y **EasyOCR** para el reconocimiento óptico de caracteres.

### Componentes Clave
- **Base de Datos (SQLite)**: Almacena propietarios, vehículos y registro de detecciones.
- **Visión Artificial**: Modelo YOLO para detectar la ubicación de la placa y EasyOCR para leer el texto.
- **Sistema de Vinculación**: Cruza la información detectada con la base de datos.

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip

### Pasos
1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repo>
   cd DetectorPlacas
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicializar la Base de Datos**:
   El sistema creará automáticamente el archivo `database/sistema_placas.db` al ejecutar la aplicación por primera vez.

## 📖 Manual de Usuario

### Ejecución
Para iniciar el sistema, ejecute:
```bash
python main.py
```

### Menú Principal
1. **Iniciar Detección**: Abre la cámara o procesa un video.
2. **Registrar Nuevo Vehículo**: Formulario para agregar propietarios y vehículos a la base de datos.
3. **Ver Propietarios**: Lista los vehículos registrados.

## ⚙️ Especificaciones Técnicas

### Arquitectura
- **Lenguaje**: Python
- **ORM/DB**: SQLite nativo.
- **Modelo**: Ultralytics YOLOv8 + EasyOCR.

### Base de Datos
El esquema incluye:
- `propietarios`: ID, nombre, teléfono, dirección.
- `vehiculos`: ID, placa, marca, modelo, FK propietario.
- `lecturas`: Registro histórico de detecciones.
- `alertas`: Tabla para notificaciones (futura expansión).

## 🧪 Pruebas
Para ejecutar las pruebas de integración:
```bash
python -m tests.test_integration
```

## 📂 Estructura del Proyecto
```text
DetectorPlacas/
├── database/           # Base de datos y esquemas
├── model/              # Modelos de IA
├── services/           # Lógica de negocio
├── utils/              # Utilidades
├── tests/              # Pruebas
├── main.py             # Punto de entrada
└── requirements.txt    # Dependencias
```
