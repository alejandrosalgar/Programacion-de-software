"""
Configuración de la base de datos PostgreSQL con Neon
"""

from sqlalchemy.orm.session import Session


import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos Neon PostgreSQL
# Obtener la URL completa de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para ver consultas SQL
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300,  # Reciclar conexiones cada 5 minutos
    connect_args={"sslmode": "require"},  # Requerir SSL para Neon
)

# Crear la sesión
SessionLocal = sessionmaker[Session](autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    Base.metadata.create_all(bind=engine)
