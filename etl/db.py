import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector as mysql


# Configuración de variables de entorno desde .env en la raíz del proyecto
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

# Función para obtener variables de entorno requeridas
def _required(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Falta una variable de entorno obligatoria: {name}")
    return val


# Conexión a la base de datos MySQL usando variables de entorno
def get_connection():
    host = _required("DB_HOST")
    user = _required("DB_USER")
    database = _required("DB_NAME")
    password = _required("DB_PASSWORD")

    # Paramentros de conexión 
    kwargs = dict(
        host=host,
        user=user,
        password=password,
        database=database,
    )    

    return mysql.connect(**kwargs)



def bulk_upsert_inventario(df):
    #Inserta registros en la tabla inventario_consolidado con UPSERT
    conn = get_connection()
    cur = conn.cursor()
    sql = """
    INSERT INTO inventario_consolidado
      (codigo_producto, nombre, descripcion_producto, stock, categoria, imagen_url, fecha_carga_dw)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
      nombre=VALUES(nombre),
      descripcion_producto=VALUES(descripcion_producto),
      stock=VALUES(stock),
      categoria=VALUES(categoria),
      imagen_url=VALUES(imagen_url),
      fecha_carga_dw=VALUES(fecha_carga_dw)
    """
    try:
        #Convierte dataframe a lista de tuplas para insertar
        cur.executemany(sql, list(df.itertuples(index=False, name=None)))
        conn.commit()
        return cur.rowcount  #Cantidad de filas insertadas/actualizadas
    except Exception as e:
        conn.rollback() #Revierte cambios si falla
        raise e
    finally:
        cur.close() #Cierra cursor
        conn.close() #Cierra conexión