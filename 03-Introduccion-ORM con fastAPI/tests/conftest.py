"""
Configuración compartida para todas las pruebas
Fixtures y configuración común
"""
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from database.config import Base, get_db
from main import app

# Base de datos en memoria para testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Hacer que SQLite soporte UUID convirtiéndolos a String
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Configurar SQLite para soportar foreign keys"""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Monkey patch para que SQLite soporte UUID como TEXT
import sqlalchemy.dialects.sqlite.base as sqlite_base
from sqlalchemy.dialects.postgresql import UUID

# Agregar soporte para UUID en SQLite
def visit_UUID(self, type_, **kw):
    return "TEXT"

if not hasattr(sqlite_base.SQLiteTypeCompiler, 'visit_UUID'):
    sqlite_base.SQLiteTypeCompiler.visit_UUID = visit_UUID

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Crear una sesión de base de datos para cada test.
    Se crea y destruye la base de datos para cada prueba.
    """
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpiar después de cada prueba
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente de prueba para hacer requests HTTP a la API.
    Sobrescribe la dependencia get_db para usar la sesión de prueba.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def categoria_ejemplo(db_session, usuario_ejemplo):
    """Fixture para crear una categoría de ejemplo"""
    from entities.categoria import Categoria
    categoria = Categoria(
        nombre="Electrónicos",
        descripcion="Productos electrónicos",
        id_usuario_crea=usuario_ejemplo.id
    )
    db_session.add(categoria)
    db_session.commit()
    db_session.refresh(categoria)
    return categoria


@pytest.fixture
def usuario_ejemplo(db_session):
    """Fixture para crear un usuario de ejemplo"""
    from entities.usuario import Usuario
    from auth.security import PasswordManager
    
    usuario = Usuario(
        nombre="Usuario Test",
        nombre_usuario="testuser",
        email="test@example.com",
        contraseña_hash=PasswordManager.hash_password("Password123!"),
        activo=True,
        es_admin=False
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario


@pytest.fixture
def admin_ejemplo(db_session):
    """Fixture para crear un usuario administrador de ejemplo"""
    from entities.usuario import Usuario
    from auth.security import PasswordManager
    
    admin = Usuario(
        nombre="Administrador",
        nombre_usuario="admin",
        email="admin@system.com",
        contraseña_hash=PasswordManager.hash_password("Admin123!"),
        activo=True,
        es_admin=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

