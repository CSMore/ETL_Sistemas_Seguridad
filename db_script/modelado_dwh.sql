-- Crear esquemas
CREATE DATABASE IF NOT EXISTS dwh_inventario;
CREATE DATABASE IF NOT EXISTS etl_logs;

-- ==============================
-- Esquema: dw (Data Warehouse)
-- ==============================

USE dwh_inventario;

-- Tabla final de inventario consolidado
CREATE TABLE inventario_consolidado (
  codigo_producto INT NOT NULL PRIMARY KEY, -- # Si quiere que sea alfa numerico poner VARCHAR
  nombre VARCHAR(250) NOT NULL,
  descripcion_producto TEXT NOT NULL,
  stock INT NOT NULL,
  categoria VARCHAR(100) NOT NULL,
  imagen_url VARCHAR(500) NOT NULL,
  fecha_carga_dw TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX ix_categoria (categoria),
  INDEX ix_nombre (nombre)
);

CREATE TABLE IF NOT EXISTS registro_auditoria (
  id_log BIGINT AUTO_INCREMENT PRIMARY KEY,
  fecha_hora DATETIME NOT NULL,
  nivel VARCHAR(50) NOT NULL,
  mensaje TEXT NOT NULL,
  proceso VARCHAR(100) DEFAULT 'PIPELINE'
);

GRANT ALL PRIVILEGES ON dwh_inventario.* TO 'ssl_user'@'localhost' REQUIRE SSL; 













