from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.producto import Producto

db = SessionLocal()


def crear(
    nombre: str,
    id_categoria: UUID,
    id_usuario_creacion: UUID,
    precio: float,
    stock: int,
    descripcion: Optional[str] = None,
) -> Producto:
    producto = Producto(
        nombre=nombre.strip(),
        id_categoria=id_categoria,
        id_usuario_creacion=id_usuario_creacion,
        precio=precio,
        stock=stock,
        descripcion=descripcion.strip() if descripcion else None,
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def obtener_por_id(id_producto: UUID) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.id_producto == id_producto).first()


def obtener_todos() -> List[Producto]:
    return db.query(Producto).all()


def obtener_por_categoria(id_categoria: UUID) -> List[Producto]:
    return db.query(Producto).filter(Producto.id_categoria == id_categoria).all()


def actualizar(
    id_producto: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Producto]:
    producto = obtener_por_id(id_producto)
    if not producto:
        return None
    for key, value in kwargs.items():
        if hasattr(producto, key):
            setattr(producto, key, value)
    producto.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(producto)
    return producto


def eliminar(id_producto: UUID) -> bool:
    producto = obtener_por_id(id_producto)
    if not producto:
        return False
    db.delete(producto)
    db.commit()
    return True
