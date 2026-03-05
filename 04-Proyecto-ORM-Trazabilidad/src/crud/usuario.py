"""
CRUD para la entidad Usuario.
Incluye creación, login (verificación de contraseña) y operaciones básicas.
"""

import hashlib
from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.usuario import Usuario

db = SessionLocal()


def _hash_contrasena(contrasena: str) -> str:
    """Hashea la contraseña con SHA-256 (para no guardar en claro)."""
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def crear(
    nombre_usuario: str,
    contrasena: str,
    rol: str = "usuario",
    activo: bool = True,
) -> Usuario:
    """Crea un nuevo usuario. La contraseña se hashea antes de guardar."""
    nombre_usuario_existente = (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip())
        .first()
    )
    if nombre_usuario_existente:
        raise ValueError("El nombre de usuario ya existe")
    usuario = Usuario(
        nombre_usuario=nombre_usuario.strip(),
        contrasena=_hash_contrasena(contrasena),
        rol=rol.strip(),
        activo=activo,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def login(nombre_usuario: str, contrasena: str) -> Optional[Usuario]:
    """
    Verifica credenciales. Devuelve el Usuario si coincide, None si no.
    """
    usuario = obtener_por_nombre_usuario(nombre_usuario)
    if not usuario or not usuario.activo:
        return None
    if usuario.contrasena != _hash_contrasena(contrasena):
        return None
    return usuario


def obtener_por_id(id_usuario: UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def obtener_por_nombre_usuario(nombre_usuario: str) -> Optional[Usuario]:
    return (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip())
        .first()
    )


def obtener_todos() -> List[Usuario]:
    return db.query(Usuario).all()


def hay_usuarios() -> bool:
    """Indica si existe al menos un usuario (para mostrar opción de registro)."""
    return db.query(Usuario).first() is not None


def actualizar(
    id_usuario: UUID,
    *,
    nombre_usuario: Optional[str] = None,
    contrasena: Optional[str] = None,
    rol: Optional[str] = None,
    activo: Optional[bool] = None,
) -> Optional[Usuario]:
    usuario = obtener_por_id(id_usuario)
    if not usuario:
        return None
    if nombre_usuario is not None:
        usuario.nombre_usuario = nombre_usuario.strip()
    if contrasena is not None:
        usuario.contrasena = _hash_contrasena(contrasena)
    if rol is not None:
        usuario.rol = rol.strip()
    if activo is not None:
        usuario.activo = activo
    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar(id_usuario: UUID) -> bool:
    usuario = obtener_por_id(id_usuario)
    if not usuario:
        return False
    db.delete(usuario)
    db.commit()
    return True
