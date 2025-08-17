import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

SERVER_NAME = os.getenv("SERVER_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")
ODBC_DRIVER = os.getenv("ODBC_DRIVER")


def conectar(master=False):
    """
    Si master=True, conecta a la base de datos 'master' para crear FarmDB si no existe.
    """
    try:
        db = "master" if master else DATABASE_NAME
        
        conn = pyodbc.connect(
            rf"DRIVER={{{ODBC_DRIVER}}};"
            rf"SERVER={SERVER_NAME};"
            rf"DATABASE={db};"
            r"Trusted_Connection=yes;"
            r"TrustServerCertificate=yes;"
        )
        
        print(f"✅ Conexión establecida a la base de datos: {db}")
        print(f"✅ Conexión establecida a la base de datos: {SERVER_NAME}")
        return conn
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        raise