# Prueba la conexión SSL con MySQL
# Para correr la prueba: python3 -m etl.test_ssl

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "ssl_ca": os.getenv("DB_SSL_CA"),
    "ssl_cert": os.getenv("DB_SSL_CERT"),
    "ssl_key": os.getenv("DB_SSL_KEY"),
    "ssl_verify_identity": os.getenv("DB_SSL_VERIFY_IDENTITY") == "true",
}

print("Intentando conexión...")

conn = mysql.connector.connect(
    host="localhost",
    user="ssl_user",
    password="password_ssl",
    database="dwh_inventario",
    ssl_ca="/usr/local/mysql/ssl/ca.pem",
    ssl_cert="/usr/local/mysql/ssl/client-cert.pem",
    ssl_key="/usr/local/mysql/ssl/client-key.pem",
    ssl_verify_cert=True,
    ssl_disabled=False
)

print("Conectado correctamente")

print("Servidor:", conn.get_server_info)



# Ver cipher usado por la sesión
cursor = conn.cursor()
cursor.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher';")
print("Cipher:", cursor.fetchone())

conn.close()

