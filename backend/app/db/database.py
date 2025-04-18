from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Conexión a la BBDD
# Cargamos las variables de entorno


# TODO: Porque no funciona el env?
user = os.getenv("USER")
password = os.getenv("PASSWORD")
bbdd = os.getenv("BBDD")
host = os.getenv("HOST")
port = os.getenv("PORT")

print("Conexión →", user, password, host, port, bbdd)

# Construimos la url de la bbdd
URL_BD = f"postgresql://{user}:{password}@{host}:{port}/{bbdd}"

# Creamos el motor de conexión
# engine = create_engine(URL_BD, pool_pre_ping=True)

engine = create_engine(URL_BD, pool_pre_ping=True)

try:
    connection = engine.connect()
    print("¡Conexión exitosa a la base de datos!")
except Exception as e:
    print(f"Error de conexión: {e}")


# Creamos la sesion
session_local = sessionmaker(autocommit=False, bind=engine, autoflush=False)
# Definimos la base de datos
BASE = declarative_base()
# Verificamos la conexion
try:
    connection = engine.connect()
    print("Conexion a la BBDD con exito.")
except Exception as e:
    print(f"Fallo al conectar a la BBDD, error {e}")
