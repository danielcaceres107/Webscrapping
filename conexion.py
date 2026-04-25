## en este script se hace la conexion a PostegreSQL

import pymysql
from pymysql import MySQLError
from dotenv import load_dotenv
import os

load_dotenv() 

# Datos de conexión
host = os.getenv("MYSQL_HOST")
port = int(os.getenv("MYSQL_PORT"))
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

def laConexion():
    try:
        conexion = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=True,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.Cursor,
            ssl={"ca": "ca.pem"}
        )
        
        print("✅ Conexión a la base de datos realizada correctamente.")
        return conexion
    except MySQLError as e:
        print("❌ Error al conectar con la base de datos.")
        print(f"Detalle del error: {e}")
        return None

conexion = laConexion()

if conexion:
    print("Puedes continuar con las operaciones en la base de datos.")
    conexion.close()
else:
    print("No se puede continuar sin conexión.")