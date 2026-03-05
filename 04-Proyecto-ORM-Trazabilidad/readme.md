# Proyecto ORM con trazabilidad

Proyecto Python con **SQLAlchemy (ORM)**, **Pydantic** para validaciones y **PostgreSQL**. Las entidades (excepto Persona) llevan trazabilidad: quién creó y quién editó cada registro.

## Estructura del proyecto

```
04-Proyecto-ORM-Trazabilidad/
├── .env.example      # Plantilla de variables de entorno (copiar a .env)
├── .gitignore
├── README.md
├── main.py           # Punto de entrada
├── requirements.txt
└── src/
    ├── database/     # Conexión a la base de datos
    │   ├── __init__.py
    │   └── config.py
    ├── entities/     # Clases ORM + esquemas Pydantic
    │   ├── __init__.py
    │   ├── persona.py
    │   ├── proyecto.py
    │   ├── tarea.py
    │   └── categoria.py
    └── crud/         # Lógica por entidad (crear, editar, listar, eliminar)
        ├── __init__.py
        ├── persona_crud.py
        ├── proyecto_crud.py
        ├── tarea_crud.py
        └── categoria_crud.py
```

## Entidades

| Entidad    | Descripción |
|-----------|-------------|
| **Persona** | Base de trazabilidad. No tiene `id_usuario_crea`/`id_usuario_edita`; las demás entidades la referencian. |
| **Proyecto** | Con `id_usuario_crea`, `id_usuario_edita`, `fecha_creacion`, `fecha_edicion`. |
| **Tarea**  | Pertenece a un Proyecto; tiene los mismos campos de trazabilidad. |
| **Categoria** | Independiente; tiene los mismos campos de trazabilidad. |

En **Proyecto**, **Tarea** y **Categoria** siempre se exige `id_usuario_crea` al crear y `id_usuario_edita` al actualizar (referencias a **Persona**).

## Requisitos

- Python 3.10+
- PostgreSQL (o servicio tipo Neon)

## Instalación

1. Clonar o abrir el proyecto y crear un entorno virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # Linux/macOS
   ```

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Configurar la base de datos:

   - Copiar `.env.example` a `.env`.
   - En `.env`, definir `DATABASE_URL` con tu cadena de conexión PostgreSQL, por ejemplo:

     ```
     DATABASE_URL=postgresql://usuario:password@host:5432/nombre_bd
     ```

4. Ejecutar el programa (crea tablas y ejecuta un ejemplo):

   ```bash
   python main.py
   ```

## Uso desde código

```python
from src.database.config import SessionLocal
from src.crud import PersonaCRUD, ProyectoCRUD

db = SessionLocal()
try:
    persona_crud = PersonaCRUD(db)
    p = persona_crud.crear(nombre="Ana", email="ana@ejemplo.com")
    proyecto_crud = ProyectoCRUD(db)
    proy = proyecto_crud.crear(nombre="Mi proyecto", id_usuario_crea=p.id)
finally:
    db.close()
```

## Validaciones

- **Pydantic**: en cada entidad hay esquemas `*Base`, `*Create`, `*Update`, `*Response` con `Field` (longitudes, opcionales, etc.).
- **CRUD**: las funciones de crear/actualizar validan datos básicos y que existan la Persona y, si aplica, el Proyecto.

## Notas

- No subas el archivo `.env` al repositorio (está en `.gitignore`).
- Para producción, considera usar migraciones (por ejemplo Alembic) en lugar de `create_tables()` en cada arranque.
