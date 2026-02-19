# Introducción a ORM con SQLAlchemy, PostgreSQL y Neon

Este proyecto sirve como guía completa para entender **qué es un ORM**, **cómo se relaciona con la base de datos**, **SQLAlchemy**, **PostgreSQL**, **Neon** y el uso de archivos **.env** para la conexión. Incluye ejemplos de uso y un flujo de trabajo listo para usar con FastAPI.

---

## Índice

1. [¿Qué es un ORM?](#1-qué-es-un-orm)
2. [¿Cómo se relaciona el ORM con la base de datos?](#2-cómo-se-relaciona-el-orm-con-la-base-de-datos)
3. [¿Qué es SQLAlchemy?](#3-qué-es-sqlalchemy)
4. [Ejemplos de uso con SQLAlchemy](#4-ejemplos-de-uso-con-sqlalchemy)
5. [¿Qué es PostgreSQL?](#5-qué-es-postgresql)
6. [¿Qué es Neon?](#6-qué-es-neon)
7. [¿Qué es un archivo .env?](#7-qué-es-un-archivo-env)
8. [Cómo conectarse a la base de datos](#8-cómo-conectarse-a-la-base-de-datos)
9. [Ejemplo de uso completo](#9-ejemplo-de-uso-completo)
10. [Inicio rápido y estructura del proyecto](#10-inicio-rápido-y-estructura-del-proyecto)

---

## 1. ¿Qué es un ORM?

**ORM** significa **Object-Relational Mapping** (mapeo objeto-relacional). Es una técnica de programación que permite trabajar con una **base de datos relacional** (tablas, filas, columnas, SQL) usando **objetos** de tu lenguaje de programación (clases, atributos, métodos) en lugar de escribir consultas SQL a mano.

### Idea central

- En la base de datos tienes **tablas** (por ejemplo `productos`, `usuarios`) con **filas** y **columnas**.
- En tu código quieres usar **objetos** (por ejemplo una instancia `Producto` con atributos `nombre`, `precio`).
- El ORM hace de **puente**: traduce entre objetos y tablas. Cuando guardas un objeto, el ORM genera el `INSERT`; cuando lees, genera el `SELECT` y te devuelve objetos.

Así evitas escribir y concatenar cadenas SQL, reduces errores y mantienes el código más legible y fácil de mantener.

### Ventajas de usar un ORM

| Ventaja | Descripción |
|--------|-------------|
| **Código más legible** | Trabajas con clases y atributos en lugar de cadenas SQL. |
| **Menos errores** | No construyes SQL a mano; el ORM genera consultas parametrizadas (menos riesgo de inyección SQL). |
| **Independencia del motor** | En teoría puedes cambiar de PostgreSQL a otro motor cambiando la configuración, no todo el código. |
| **Relaciones y validaciones** | Puedes definir relaciones (uno a muchos, muchos a muchos) y validaciones en un solo lugar. |
| **Migraciones** | Herramientas como Alembic permiten versionar cambios del esquema de la BD. |

### Desventajas o consideraciones

- **Curva de aprendizaje**: hay que entender sesiones, transacciones y el ciclo de vida de los objetos.
- **Rendimiento**: en consultas muy complejas o masivas a veces el SQL escrito a mano es más eficiente; el ORM puede generar consultas no óptimas si no se usa bien.
- **Abstracción**: a veces necesitas bajar al nivel SQL para optimizar; los ORMs suelen permitirlo.

En resumen: un **ORM** es la capa que mapea tus **objetos** (Python) a **tablas y filas** (base de datos) y viceversa.

---

## 2. ¿Cómo se relaciona el ORM con la base de datos?

El ORM no reemplaza la base de datos: **la base de datos sigue siendo la que almacena los datos**. El ORM solo cambia **cómo** tu aplicación se comunica con ella.

### Flujo general

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Tu código     │         │      ORM        │         │  Base de datos  │
│   (Python)      │  ────►  │  (SQLAlchemy)   │  ────►  │  (PostgreSQL)   │
│                 │  objetos │                 │  SQL    │  tablas, filas  │
│  producto.nombre│         │  INSERT/SELECT  │         │  productos      │
│  producto.precio│  ◄────  │  UPDATE/DELETE  │  ◄────  │  usuarios       │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

- **De tu código hacia la BD**: creas o modificas un objeto (por ejemplo `Producto(nombre="Laptop", precio=999.99)`). El ORM traduce eso a `INSERT` o `UPDATE` en la tabla correspondiente.
- **De la BD hacia tu código**: el ORM ejecuta un `SELECT`, recibe filas, y te devuelve instancias de tus clases (objetos) con los datos rellenados.

### Relación con el esquema

- Cada **clase** (modelo) del ORM suele corresponder a una **tabla**.
- Cada **atributo** de la clase corresponde a una **columna**.
- Las **relaciones** (ForeignKey, relationship) se traducen en claves foráneas y joins.

Así, el ORM mantiene una **correspondencia** entre el mundo orientado a objetos y el mundo relacional, y se encarga de generar el SQL adecuado y de rellenar los objetos con los datos leídos.

---

## 3. ¿Qué es SQLAlchemy?

**SQLAlchemy** es una biblioteca de Python que implementa un ORM y además ofrece una capa de acceso a la base de datos a bajo nivel. Es uno de los ORMs más usados en el ecosistema Python.

### Componentes principales

| Componente | Uso |
|-----------|-----|
| **Engine** | Gestiona la conexión con la BD (URL, pool de conexiones). Se crea con `create_engine(DATABASE_URL)`. |
| **Session** | Contexto de trabajo: todas las operaciones (añadir, modificar, borrar, consultar) se hacen dentro de una sesión. Al final haces `commit()` o `rollback()`. |
| **Modelo (Base declarativa)** | Clases que heredan de `Base` y definen tablas mediante `Column`, tipos, y `relationship`. |
| **SessionMaker** | Fábrica de sesiones asociada a un engine; en el proyecto se usa como `SessionLocal`. |

### Tipos de uso

- **ORM (alto nivel)**: defines modelos y trabajas con objetos. Es lo que usamos en este proyecto (entidades en `entities/`, CRUD en `crud/`).
- **Core / SQL (bajo nivel)**: puedes escribir consultas SQL o usar el “Core” de SQLAlchemy si necesitas más control.

En este README y en el código del proyecto se usa sobre todo el **ORM**: modelos en `entities/`, configuración en `database/config.py`, y operaciones a través de sesiones.

---

## 4. Ejemplos de uso con SQLAlchemy

### Definir un modelo (entidad)

Cada modelo es una clase que hereda de `Base` y define una tabla con `Column`:

```python
from database.config import Base
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String(500), nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
```

Aquí la **tabla** se llama `productos` y tiene columnas `id_producto`, `nombre`, `descripcion`, `precio`, `stock`. El ORM usará esta definición para generar `CREATE TABLE` y para mapear filas a objetos `Producto`.

### Crear un registro (INSERT)

```python
from database.config import SessionLocal
from entities.producto import Producto

db = SessionLocal()
try:
    producto = Producto(
        nombre="Laptop",
        descripcion="Portátil 15 pulgadas",
        precio=899.99,
        stock=10,
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    print(producto.id_producto)  # UUID generado
finally:
    db.close()
```

El ORM traduce esto a un `INSERT` en la tabla `productos`.

### Leer registros (SELECT)

```python
# Por ID
producto = db.query(Producto).filter(Producto.id_producto == algun_uuid).first()

# Listar con límite
productos = db.query(Producto).offset(0).limit(10).all()

# Con filtro
baratos = db.query(Producto).filter(Producto.precio < 100).all()
```

### Actualizar (UPDATE)

```python
producto = db.query(Producto).filter(Producto.id_producto == id).first()
if producto:
    producto.precio = 799.99
    producto.stock = 5
    db.commit()
```

### Eliminar (DELETE)

```python
producto = db.query(Producto).filter(Producto.id_producto == id).first()
if producto:
    db.delete(producto)
    db.commit()
```

En todos los casos el ORM genera el SQL correspondiente; tú trabajas con objetos Python.

---

## 5. ¿Qué es PostgreSQL?

**PostgreSQL** (o “Postgres”) es un **motor de base de datos relacional** open source. Guarda los datos en **tablas** relacionadas entre sí mediante claves primarias y foráneas, y se accede con el lenguaje **SQL**.

### Características relevantes

- Soporta tipos avanzados (JSON, UUID, arrays, etc.).
- Cumple bien con el estándar SQL y con transacciones ACID.
- Muy usado en producción y en entornos cloud (por ejemplo Neon).

En este proyecto la base de datos que usamos es **PostgreSQL**; puede estar instalada localmente o en la nube (por ejemplo en **Neon**). El ORM (SQLAlchemy) se conecta a Postgres mediante un driver como `psycopg2` o `asyncpg`.

---

## 6. ¿Qué es Neon?

**Neon** es un servicio de **base de datos PostgreSQL en la nube**, pensado para ser fácil de usar y escalable. Ofrece PostgreSQL “serverless”: no tienes que instalar ni mantener el servidor tú mismo.

### Por qué usarlo aquí

- **Sin instalar Postgres**: creas un proyecto en [neon.tech](https://neon.tech), obtienes una URL de conexión y listo.
- **SSL incluido**: las conexiones son seguras; en la URL suele ir `?sslmode=require`.
- **Gratis para empezar**: hay plan gratuito para desarrollo y aprendizaje.
- **Compatible con PostgreSQL**: es Postgres estándar, así que todo lo que aprendes (SQL, tipos, conexión) aplica.

En resumen: **Neon = PostgreSQL en la nube**, listo para conectar desde tu aplicación usando la misma URL y el mismo driver que con cualquier Postgres.

---

## 7. ¿Qué es un archivo .env?

Un archivo **.env** es un archivo de texto que guarda **variables de entorno** en forma de pares `NOMBRE=valor`. Se usa para configuraciones que **no deben estar escritas en el código**, sobre todo secretos (contraseñas, URLs de BD, API keys).

### Para qué sirve

- **Seguridad**: las credenciales no van en el repositorio; cada desarrollador o servidor tiene su propio `.env`.
- **Flexibilidad**: en desarrollo usas una BD; en producción otra; solo cambias el `.env`.
- **Convención**: muchas herramientas (FastAPI, Django, Node, etc.) leen automáticamente variables de entorno.

### Formato típico

```env
DATABASE_URL=postgresql://usuario:password@host.neon.tech/nombre_bd?sslmode=require
API_KEY=mi_clave_secreta
DEBUG=true
```

- Sin espacios alrededor del `=`.
- Valores con espacios o caracteres raros suelen ir entre comillas.
- Una variable por línea.

### Uso en Python: python-dotenv

La biblioteca **python-dotenv** lee el archivo `.env` y carga esas variables en el entorno del proceso, de modo que `os.getenv("DATABASE_URL")` devuelva el valor.

```python
from dotenv import load_dotenv
import os

load_dotenv()   # Carga .env del directorio actual (o el que indiques)
url = os.getenv("DATABASE_URL")
```

### Buenas prácticas

- **No subir `.env` a Git**: añádelo a `.gitignore`. Sube un `env.example` con nombres de variables pero sin valores reales.
- **No poner secretos en el código**: siempre usar variables de entorno (o un gestor de secretos) en producción.

---

## 8. Cómo conectarse a la base de datos

En este proyecto la conexión se hace en **un solo lugar**: `database/config.py`, usando la URL que viene del `.env`.

### Paso 1: Crear el archivo .env

En la raíz del proyecto (carpeta `03-Introduccion-ORM con fastAPI`) crea un archivo llamado `.env` con la URL de tu base de datos. Si usas Neon, la copias desde el dashboard:

```env
DATABASE_URL=postgresql://usuario:contraseña@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

Sustituye `usuario`, `contraseña`, `ep-xxx...` y `neondb` por los datos que te da Neon.

### Paso 2: Código de configuración (database/config.py)

El proyecto ya tiene este patrón:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en las variables de entorno")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

- **load_dotenv()**: carga las variables del `.env`.
- **create_engine(DATABASE_URL)**: crea el motor de SQLAlchemy contra PostgreSQL.
- **SessionLocal**: fábrica de sesiones; en cada request o script creas una sesión, haces las operaciones y la cierras.

### Paso 3: Obtener una sesión

Para hacer consultas o cambios:

```python
from database.config import SessionLocal

db = SessionLocal()
try:
    # usar db para consultas y cambios
    db.commit()
finally:
    db.close()
```

O usar el generador `get_db()` que ya está en `config.py` para inyectar la sesión en FastAPI.

---

## 9. Ejemplo de uso completo

Este ejemplo junta: **.env** → **cargar configuración** → **conectar** → **definir modelo** → **crear tabla** → **insertar y leer**.

### 1. Archivo .env (en la raíz del proyecto)

```env
DATABASE_URL=postgresql://usuario:password@tu-host.neon.tech/neondb?sslmode=require
```

### 2. Configuración (database/config.py)

Ya está en el proyecto: `load_dotenv()`, `os.getenv("DATABASE_URL")`, `create_engine`, `SessionLocal`, `Base`.

### 3. Modelo (entities/producto.py)

```python
from database.config import Base
from sqlalchemy import Column, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Producto(Base):
    __tablename__ = "productos"
    id_producto = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(200), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
```

### 4. Crear tablas y usar la sesión

```python
from database.config import engine, SessionLocal, create_tables
from entities.producto import Producto

# Crear tablas (si no existen)
create_tables()

db = SessionLocal()
try:
    p = Producto(nombre="Monitor", precio=199.99, stock=5)
    db.add(p)
    db.commit()
    db.refresh(p)
    print("Creado:", p.id_producto, p.nombre)

    # Leer todos
    todos = db.query(Producto).all()
    for prod in todos:
        print(prod.nombre, prod.precio)
finally:
    db.close()
```

Flujo resumido: **.env** guarda la URL → **config.py** la lee y crea el engine y la sesión → los **modelos** definen las tablas → **create_tables()** crea el esquema → usas **SessionLocal()** para hacer CRUD con objetos.

---

## 10. Inicio rápido y estructura del proyecto

### Inicio rápido

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar Neon**
   - Cuenta en [neon.tech](https://neon.tech), crear proyecto, copiar la cadena de conexión.

3. **Crear .env**
   ```bash
   cp env.example .env
   ```
   Editar `.env` y pegar tu `DATABASE_URL` de Neon.

4. **Crear tablas**
   ```bash
   python setup_simple.py
   ```
   (o el script que uses para crear tablas en tu proyecto)

5. **Ejecutar la API**
   ```bash
   python main.py
   ```
   o con uvicorn según cómo esté expuesta la app.

### Estructura del proyecto

```
03-Introduccion-ORM con fastAPI/
├── database/
│   └── config.py          # Conexión, engine, SessionLocal, Base, get_db
├── entities/               # Modelos ORM (tablas)
│   ├── usuario.py
│   ├── categoria.py
│   └── producto.py
├── crud/                  # Operaciones CRUD por entidad
│   ├── usuario_crud.py
│   ├── categoria_crud.py
│   └── producto_crud.py
├── apis/                  # Rutas FastAPI
├── migrations/            # Alembic (versiones del esquema)
├── .env                   # Variables de entorno (no subir a Git)
├── env.example            # Plantilla sin valores sensibles
├── requirements.txt
├── main.py
└── README.md
```

### Dependencias principales

- **sqlalchemy**: ORM y motor.
- **psycopg2-binary**: driver de PostgreSQL para Python.
- **python-dotenv**: carga de variables desde `.env`.
- **alembic**: migraciones del esquema.
- **fastapi / uvicorn**: API REST.

### Comandos útiles (Alembic)

```bash
alembic revision --autogenerate -m "Descripción"
alembic upgrade head
alembic current
alembic history
```

---

## Resumen conceptual

| Tema | Resumen |
|------|--------|
| **ORM** | Mapeo entre objetos (Python) y tablas/filas (BD); evita escribir SQL a mano. |
| **Relación ORM–BD** | El ORM traduce operaciones sobre objetos a SQL contra la BD. |
| **SQLAlchemy** | Biblioteca ORM en Python; Engine, Session, modelos declarativos. |
| **PostgreSQL** | Base de datos relacional; la que usa Neon. |
| **Neon** | PostgreSQL en la nube, listo para usar con una URL. |
| **.env** | Archivo con variables de entorno (ej. `DATABASE_URL`); no se sube a Git. |
| **Conexión** | `load_dotenv()` + `os.getenv("DATABASE_URL")` + `create_engine()` + `SessionLocal`. |

Con esto tienes todo en un solo README: conceptos (ORM, SQLAlchemy, Postgres, Neon, .env), relación con la BD, ejemplos de uso y un ejemplo completo de conexión y CRUD.
