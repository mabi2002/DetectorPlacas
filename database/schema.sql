-- ===========================================
-- ESQUEMA COMPLETO DEL SISTEMA DE MATRÍCULAS
-- ===========================================

-- Tabla: propietarios
CREATE TABLE IF NOT EXISTS propietarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    direccion TEXT
);

-- Tabla: vehiculos
CREATE TABLE IF NOT EXISTS vehiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT UNIQUE NOT NULL,
    marca TEXT,
    modelo TEXT,
    anio INTEGER,
    color TEXT,
    propietario_id INTEGER,
    FOREIGN KEY (propietario_id) REFERENCES propietarios(id)
);

-- Tabla: lecturas de cámaras
CREATE TABLE IF NOT EXISTS lecturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehiculo_id INTEGER,
    placa_detectada TEXT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    camara TEXT,
    imagen_ruta TEXT,
    coincidencia REAL,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
);

-- Tabla: alertas generadas
CREATE TABLE IF NOT EXISTS alertas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehiculo_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    descripcion TEXT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id)
);
