import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# 1. Cargar variables de entorno desde el archivo .env
load_dotenv()

# URL de la base de datos
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://root@localhost:3306/billeterapp_db?charset=utf8mb4"
)

# 2. Configuración del Engine con recarga de conexiones
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,   # Recicla conexiones cada hora
    pool_pre_ping=True   # Verifica si la conexión sigue activa
)

# 3. Creación de Sesión Segura para entorno Web (Thread-safe)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

# 4. Declaración Base para los modelos
Base = declarative_base()
Base.metadata.bind = engine

__all__ = ["engine", "session", "Base"]
