# DB/create_tables.py
from .db_connection import conectar, DATABASE_NAME

def crear_base_si_no_existe():
    """
    Crea la base de datos si no existe.
    """
    conn = conectar(master=True)
    cursor = conn.cursor()
    cursor.execute(f"IF DB_ID('{DATABASE_NAME}') IS NULL CREATE DATABASE {DATABASE_NAME}")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"📦 Base de datos '{DATABASE_NAME}' lista.")


def crear_tablas():
    """
    Crea las tablas Usuario, Suministro y Devolucion si no existen.
    """
    conn = conectar()
    cursor = conn.cursor()

    # SQL Server requiere IF NOT EXISTS con CREATE TABLE separado por GO o múltiples execute
    # Vamos a ejecutarlos por separado
    queries = [
        """
        IF OBJECT_ID('Usuario', 'U') IS NULL
        CREATE TABLE Usuario(
            id_usuario INT PRIMARY KEY IDENTITY(1,1),
            nombre NVARCHAR(100) NOT NULL,
            identificacion NVARCHAR(50) NOT NULL UNIQUE,
            rol NVARCHAR(50) NOT NULL
        )
        """,
        """
        IF OBJECT_ID('Suministro', 'U') IS NULL
        CREATE TABLE Suministro (
            id_suministro INT PRIMARY KEY IDENTITY(1,1),
            id_usuario INT NOT NULL,
            fecha_entrega DATE NOT NULL,
            tipo NVARCHAR(50) NOT NULL,
            cantidad INT NOT NULL,
            observaciones NVARCHAR(255) NULL,
            CONSTRAINT FK_Suministro_Usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
        )
        """,
        """
        IF OBJECT_ID('Devolucion', 'U') IS NULL
        CREATE TABLE Devolucion (
            id_devolucion INT PRIMARY KEY IDENTITY(1,1),
            id_usuario INT NOT NULL,
            fecha_devolucion DATE NOT NULL,
            estado NVARCHAR(50) NOT NULL,
            herramienta NVARCHAR(100) NOT NULL,
            observaciones NVARCHAR(255) NOT NULL,
            CONSTRAINT FK_Devolucion_Usuario FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
        )
        """
    ]

    for q in queries:
        cursor.execute(q)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tablas creadas exitosamente.")


if __name__ == "__main__":
    crear_base_si_no_existe()
    crear_tablas()
