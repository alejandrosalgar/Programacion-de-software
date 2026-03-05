from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.pedido import Pedido

db = SessionLocal()


def crear(total_pagado: float, id_usuario: UUID, id_usuario_creacion: UUID) -> Pedido:
    pedido = Pedido(
        id_usuario=id_usuario,
        id_usuario_creacion=id_usuario_creacion,
        total_pagado=total_pagado,
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def obtener_por_id(id_pedido: UUID) -> Optional[Pedido]:
    return db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()


def obtener_todos() -> List[Pedido]:
    return db.query(Pedido).all()


def obtener_por_usuario(id_usuario: UUID) -> List[Pedido]:
    return db.query(Pedido).filter(Pedido.id_usuario == id_usuario).all()


def actualizar(
    id_pedido: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Pedido]:
    pedido = obtener_por_id(id_pedido)
    if not pedido:
        return None
    for key, value in kwargs.items():
        if hasattr(pedido, key):
            setattr(pedido, key, value)
    pedido.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(pedido)
    return pedido


def eliminar(id_pedido: UUID) -> bool:
    pedido = obtener_por_id(id_pedido)
    if not pedido:
        return False
    db.delete(pedido)
    db.commit()
    return True
