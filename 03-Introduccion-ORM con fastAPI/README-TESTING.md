# Guía de Pruebas Unitarias y Testing

Esta guía explica las buenas prácticas de testing y cómo implementar pruebas unitarias en el backend FastAPI.

## Tabla de Contenidos

1. [Introducción a las Pruebas](#introducción-a-las-pruebas)
2. [Tipos de Pruebas](#tipos-de-pruebas)
3. [Configuración del Entorno de Testing](#configuración-del-entorno-de-testing)
4. [Estructura de Pruebas](#estructura-de-pruebas)
5. [Buenas Prácticas](#buenas-prácticas)
6. [Ejecutar Pruebas](#ejecutar-pruebas)
7. [Cobertura de Código](#cobertura-de-código)
8. [Recursos Adicionales](#recursos-adicionales)

---

## Introducción a las Pruebas

Las pruebas unitarias son una parte fundamental del desarrollo de software que permite verificar que cada componente de tu aplicación funciona correctamente de forma aislada. Escribir pruebas ayuda a:

- Detectar errores tempranamente
- Facilitar el mantenimiento del código
- Documentar el comportamiento esperado
- Permitir refactorización segura
- Mejorar la calidad del código

### ¿Por qué son importantes las pruebas?

- **Confianza**: Sabes que tu código funciona como se espera
- **Documentación viva**: Las pruebas muestran cómo se debe usar el código
- **Refactorización segura**: Puedes cambiar código sabiendo que las pruebas detectarán errores
- **Detección temprana**: Encuentras bugs antes de que lleguen a producción

Para más información sobre la importancia del testing, consulta: [Why Write Tests?](https://docs.pytest.org/en/stable/getting-started.html#why-use-pytest)

---

## Tipos de Pruebas

### Pruebas Unitarias (Unit Tests)

Prueban funciones o métodos individuales de forma aislada, sin dependencias externas (base de datos, APIs, etc.).

**Ejemplo**: Probar que una función de validación de email funciona correctamente.

**Cuándo usar**: Para lógica de negocio, validaciones, transformaciones de datos.

**Documentación**: [Unit Testing Best Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)

### Pruebas de Integración (Integration Tests)

Prueban la interacción entre múltiples componentes (por ejemplo, API + Base de datos).

**Ejemplo**: Probar que un endpoint de la API crea correctamente un producto en la base de datos.

**Cuándo usar**: Para verificar que los componentes trabajan juntos correctamente.

**Documentación**: [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

### Pruebas de API (API Tests)

Prueban los endpoints de la API usando HTTP requests.

**Ejemplo**: Hacer un POST a `/productos` y verificar la respuesta.

**Cuándo usar**: Para verificar que los endpoints funcionan correctamente.

**Documentación**: [Testing FastAPI with TestClient](https://fastapi.tiangolo.com/tutorial/testing/#testing-http-requests)

### Pruebas de Base de Datos (Database Tests)

Prueban las operaciones CRUD y las consultas a la base de datos.

**Ejemplo**: Probar que `crear_producto()` guarda correctamente en la base de datos.

**Cuándo usar**: Para verificar operaciones de base de datos.

**Documentación**: [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/core/testing.html)

---

## Configuración del Entorno de Testing

### 1. Instalar Dependencias

Primero, instala las dependencias necesarias para testing:

```bash
pip install pytest pytest-asyncio httpx pytest-cov pytest-mock
```

O agrega estas líneas a tu `requirements.txt`:

```
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
pytest-cov==4.1.0
pytest-mock==3.12.0
```

Luego instala:

```bash
pip install -r requirements.txt
```

### 2. Estructura de Carpetas

Crea la siguiente estructura de carpetas:

```
03-Introduccion-ORM con fastAPI/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Configuración compartida
│   ├── test_crud/            # Pruebas de operaciones CRUD
│   │   ├── __init__.py
│   │   ├── test_producto_crud.py
│   │   ├── test_categoria_crud.py
│   │   └── test_usuario_crud.py
│   ├── test_api/             # Pruebas de endpoints API
│   │   ├── __init__.py
│   │   ├── test_producto_api.py
│   │   ├── test_categoria_api.py
│   │   ├── test_usuario_api.py
│   │   └── test_auth_api.py
│   ├── test_security/         # Pruebas de seguridad
│   │   ├── __init__.py
│   │   └── test_password_manager.py
│   └── test_utils/            # Pruebas de utilidades
│       ├── __init__.py
│       └── test_validaciones.py
```

### 3. Archivo conftest.py

El archivo `conftest.py` contiene fixtures compartidas (datos de prueba reutilizables):

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.config import Base, get_db
from main import app

# Base de datos en memoria para testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Crear una sesión de base de datos para cada test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de prueba para hacer requests HTTP"""
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
```

---

## Estructura de Pruebas

### Patrón AAA (Arrange, Act, Assert)

Todas las pruebas deben seguir este patrón:

1. **Arrange (Preparar)**: Configura el estado inicial y los datos necesarios
2. **Act (Actuar)**: Ejecuta la función o método que quieres probar
3. **Assert (Verificar)**: Verifica que el resultado sea el esperado

**Ejemplo**:

```python
def test_crear_producto(db_session):
    # Arrange: Preparar datos
    from crud.producto_crud import ProductoCRUD
    from uuid import uuid4
    
    categoria_id = uuid4()
    usuario_id = uuid4()
    
    # Act: Ejecutar la función
    producto_crud = ProductoCRUD(db_session)
    producto = producto_crud.crear_producto(
        nombre="Producto Test",
        descripcion="Descripción test",
        precio=100.50,
        stock=10,
        categoria_id=categoria_id,
        usuario_id=usuario_id
    )
    
    # Assert: Verificar el resultado
    assert producto is not None
    assert producto.nombre == "Producto Test"
    assert producto.precio == 100.50
```

### Nomenclatura de Pruebas

Usa nombres descriptivos que expliquen qué se está probando:

```python
# Bueno
def test_crear_producto_con_datos_validos():
def test_crear_producto_falla_con_precio_negativo():
def test_obtener_producto_por_id_existente():
def test_obtener_producto_por_id_no_existente_retorna_none():

# Malo
def test1():
def test_producto():
def test_crear():
```

### Organización de Pruebas

Agrupa pruebas relacionadas en clases:

```python
class TestProductoCRUD:
    def test_crear_producto_exitoso(self, db_session):
        # ...
    
    def test_crear_producto_falla_sin_nombre(self, db_session):
        # ...
    
    def test_obtener_producto_por_id(self, db_session):
        # ...
```

---

## Buenas Prácticas

### 1. Una Prueba, Una Verificación

Cada prueba debe verificar una sola cosa:

```python
# Bueno
def test_precio_debe_ser_positivo(db_session):
    # ...
    assert producto.precio > 0

# Malo
def test_validaciones_producto(db_session):
    # Verifica muchas cosas a la vez
    assert producto.precio > 0
    assert producto.stock >= 0
    assert len(producto.nombre) > 0
```

### 2. Pruebas Independientes

Las pruebas no deben depender unas de otras:

```python
# Bueno: Cada prueba crea sus propios datos
def test_crear_producto_1(db_session):
    # Crea producto 1
    pass

def test_crear_producto_2(db_session):
    # Crea producto 2 (independiente)
    pass

# Malo: La segunda prueba depende de la primera
def test_crear_producto_1(db_session):
    producto = crear_producto(...)
    global producto_id
    producto_id = producto.id

def test_actualizar_producto_1(db_session):
    # Usa producto_id de la prueba anterior (MALO)
    actualizar_producto(producto_id, ...)
```

### 3. Usar Fixtures para Datos Comunes

Crea fixtures para datos que se usan frecuentemente:

```python
@pytest.fixture
def categoria_ejemplo(db_session):
    from crud.categoria_crud import CategoriaCRUD
    categoria_crud = CategoriaCRUD(db_session)
    return categoria_crud.crear_categoria(
        nombre="Electrónicos",
        descripcion="Productos electrónicos"
    )

@pytest.fixture
def usuario_ejemplo(db_session):
    from crud.usuario_crud import UsuarioCRUD
    usuario_crud = UsuarioCRUD(db_session)
    return usuario_crud.crear_usuario(
        nombre="Usuario Test",
        nombre_usuario="testuser",
        email="test@example.com",
        contraseña="Password123!"
    )
```

### 4. Probar Casos Límite

No solo pruebes el caso "feliz", también prueba casos extremos:

```python
def test_crear_producto_con_precio_cero_debe_fallar(db_session):
    # Probar que precio = 0 falla
    pass

def test_crear_producto_con_precio_negativo_debe_fallar(db_session):
    # Probar que precio < 0 falla
    pass

def test_crear_producto_con_nombre_vacio_debe_fallar(db_session):
    # Probar que nombre vacío falla
    pass

def test_crear_producto_con_nombre_muy_largo_debe_fallar(db_session):
    # Probar que nombre > 200 caracteres falla
    pass
```

### 5. Usar Mocks para Dependencias Externas

Para pruebas unitarias, usa mocks para simular dependencias:

```python
from unittest.mock import Mock, patch

def test_funcion_con_dependencia_externa():
    # Mock de una dependencia externa
    with patch('modulo.externa.funcion') as mock_func:
        mock_func.return_value = "valor esperado"
        resultado = mi_funcion()
        assert resultado == "valor esperado"
```

### 6. Mensajes de Assert Claros

Usa mensajes descriptivos en los asserts:

```python
# Bueno
assert producto.precio > 0, f"El precio debe ser positivo, pero es {producto.precio}"

# Mejor: Usar assert con mensaje descriptivo
assert producto.precio > 0, "El precio del producto debe ser mayor a cero"
```

### 7. Limpiar Después de Cada Prueba

Asegúrate de limpiar los datos después de cada prueba (los fixtures con `scope="function"` hacen esto automáticamente):

```python
@pytest.fixture(scope="function")
def db_session():
    # Crea base de datos
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    # Limpia después de la prueba
    db.close()
    Base.metadata.drop_all(bind=engine)
```

---

## Ejecutar Pruebas

### Ejecutar Todas las Pruebas

```bash
pytest
```

### Ejecutar Pruebas de un Archivo Específico

```bash
pytest tests/test_crud/test_producto_crud.py
```

### Ejecutar Pruebas de una Clase Específica

```bash
pytest tests/test_crud/test_producto_crud.py::TestProductoCRUD
```

### Ejecutar una Prueba Específica

```bash
pytest tests/test_crud/test_producto_crud.py::TestProductoCRUD::test_crear_producto_exitoso
```

### Ejecutar con Verbose (Más Detalles)

```bash
pytest -v
```

### Ejecutar y Mostrar Prints

```bash
pytest -s
```

### Ejecutar y Detenerse en el Primer Error

```bash
pytest -x
```

### Ejecutar Solo Pruebas que Contengan un Texto

```bash
pytest -k "producto"
```

---

## Cobertura de Código

La cobertura de código mide qué porcentaje de tu código está siendo probado.

### Instalar pytest-cov

```bash
pip install pytest-cov
```

### Ejecutar Pruebas con Cobertura

```bash
pytest --cov=. --cov-report=html
```

Esto genera un reporte HTML en `htmlcov/index.html` que puedes abrir en tu navegador.

### Ver Cobertura en Terminal

```bash
pytest --cov=. --cov-report=term
```

### Configurar Cobertura Mínima

Crea un archivo `.coveragerc`:

```ini
[run]
source = .
omit = 
    tests/*
    migrations/*
    __pycache__/*
    venv/*

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov
```

### Objetivo de Cobertura

- **Mínimo recomendado**: 70% de cobertura
- **Bueno**: 80% de cobertura
- **Excelente**: 90%+ de cobertura

**Nota**: La cobertura alta no garantiza código de calidad, pero es un buen indicador.

Para más información: [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

---

## Ejemplos de Pruebas

### Ejemplo 1: Prueba Unitaria de CRUD

```python
# tests/test_crud/test_producto_crud.py
import pytest
from uuid import uuid4
from crud.producto_crud import ProductoCRUD
from entities.categoria import Categoria
from entities.usuario import Usuario

class TestProductoCRUD:
    def test_crear_producto_exitoso(self, db_session):
        # Arrange
        categoria = Categoria(nombre="Test", descripcion="Test")
        db_session.add(categoria)
        db_session.commit()
        
        usuario = Usuario(
            nombre="Test User",
            nombre_usuario="testuser",
            email="test@test.com",
            contraseña_hash="hash"
        )
        db_session.add(usuario)
        db_session.commit()
        
        producto_crud = ProductoCRUD(db_session)
        
        # Act
        producto = producto_crud.crear_producto(
            nombre="Producto Test",
            descripcion="Descripción",
            precio=100.50,
            stock=10,
            categoria_id=categoria.id_categoria,
            usuario_id=usuario.id_usuario
        )
        
        # Assert
        assert producto is not None
        assert producto.nombre == "Producto Test"
        assert producto.precio == 100.50
        assert producto.stock == 10
    
    def test_crear_producto_falla_con_precio_negativo(self, db_session):
        # Arrange
        categoria = Categoria(nombre="Test", descripcion="Test")
        db_session.add(categoria)
        db_session.commit()
        
        usuario = Usuario(
            nombre="Test User",
            nombre_usuario="testuser",
            email="test@test.com",
            contraseña_hash="hash"
        )
        db_session.add(usuario)
        db_session.commit()
        
        producto_crud = ProductoCRUD(db_session)
        
        # Act & Assert
        with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
            producto_crud.crear_producto(
                nombre="Producto Test",
                descripcion="Descripción",
                precio=-10,  # Precio negativo
                stock=10,
                categoria_id=categoria.id_categoria,
                usuario_id=usuario.id_usuario
            )
```

### Ejemplo 2: Prueba de API Endpoint

```python
# tests/test_api/test_producto_api.py
import pytest
from uuid import uuid4

class TestProductoAPI:
    def test_obtener_productos_vacio(self, client):
        # Act
        response = client.get("/productos/")
        
        # Assert
        assert response.status_code == 200
        assert response.json() == []
    
    def test_crear_producto_via_api(self, client, db_session):
        # Arrange: Crear categoría y usuario primero
        from entities.categoria import Categoria
        from entities.usuario import Usuario
        
        categoria = Categoria(nombre="Test", descripcion="Test")
        db_session.add(categoria)
        db_session.commit()
        
        usuario = Usuario(
            nombre="Test User",
            nombre_usuario="testuser",
            email="test@test.com",
            contraseña_hash="hash"
        )
        db_session.add(usuario)
        db_session.commit()
        
        producto_data = {
            "nombre": "Producto API Test",
            "descripcion": "Descripción",
            "precio": 100.50,
            "stock": 10,
            "categoria_id": str(categoria.id_categoria),
            "usuario_id": str(usuario.id_usuario)
        }
        
        # Act
        response = client.post("/productos/", json=producto_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Producto API Test"
        assert data["precio"] == 100.50
```

### Ejemplo 3: Prueba de Seguridad

```python
# tests/test_security/test_password_manager.py
import pytest
from auth.security import PasswordManager

class TestPasswordManager:
    def test_hash_password_genera_hash_diferente(self):
        password = "MiPassword123!"
        hash1 = PasswordManager.hash_password(password)
        hash2 = PasswordManager.hash_password(password)
        
        # Cada hash debe ser diferente (por el salt)
        assert hash1 != hash2
    
    def test_verify_password_correcta(self):
        password = "MiPassword123!"
        password_hash = PasswordManager.hash_password(password)
        
        assert PasswordManager.verify_password(password, password_hash) == True
    
    def test_verify_password_incorrecta(self):
        password = "MiPassword123!"
        password_hash = PasswordManager.hash_password(password)
        wrong_password = "WrongPassword123!"
        
        assert PasswordManager.verify_password(wrong_password, password_hash) == False
    
    def test_validate_password_strength_valida(self):
        password = "MiPassword123!"
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        assert es_valida == True
        assert mensaje == "Contraseña válida"
    
    def test_validate_password_strength_corta(self):
        password = "Short1!"
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        assert es_valida == False
        assert "8 caracteres" in mensaje
```

---

## Recursos Adicionales

### Documentación Oficial

- [pytest Documentation](https://docs.pytest.org/) - Documentación completa de pytest
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) - Cómo probar aplicaciones FastAPI
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/core/testing.html) - Testing con SQLAlchemy
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/) - Cobertura de código con pytest

### Artículos y Tutoriales

- [Test-Driven Development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development) - Metodología TDD
- [Python Testing Best Practices](https://realpython.com/python-testing/) - Mejores prácticas de testing en Python
- [Unit Testing Best Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html) - Buenas prácticas de pytest

### Herramientas Relacionadas

- [pytest-xdist](https://pytest-xdist.readthedocs.io/) - Ejecutar pruebas en paralelo
- [pytest-mock](https://pytest-mock.readthedocs.io/) - Mocking en pytest
- [faker](https://faker.readthedocs.io/) - Generar datos de prueba realistas

---

## Checklist de Testing

Antes de considerar que tu código está bien probado, verifica:

- [ ] Cada función CRUD tiene al menos una prueba
- [ ] Cada endpoint de API tiene al menos una prueba
- [ ] Se prueban casos exitosos (happy path)
- [ ] Se prueban casos de error (validaciones, errores 404, etc.)
- [ ] Se prueban casos límite (valores en los bordes)
- [ ] Las pruebas son independientes (no dependen unas de otras)
- [ ] Las pruebas son rápidas (no dependen de servicios externos lentos)
- [ ] La cobertura de código es al menos 70%
- [ ] Los nombres de las pruebas son descriptivos
- [ ] Las pruebas siguen el patrón AAA (Arrange, Act, Assert)

---

## Conclusión

Escribir pruebas unitarias es una inversión en la calidad y mantenibilidad de tu código. Comienza con pruebas simples y ve aumentando la cobertura gradualmente. Recuerda que:

- Las pruebas son código que documenta el comportamiento esperado
- Las pruebas te dan confianza para refactorizar
- Las pruebas detectan errores antes de que lleguen a producción
- Las pruebas bien escritas sirven como ejemplos de uso

¡Feliz testing!

