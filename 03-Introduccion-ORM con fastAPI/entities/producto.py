import uuid

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Producto(Base):
    """Modelo de Producto"""

    __tablename__ = "productos"

    id_producto = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    elimado = Column(boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    categoria_id = Column(
        UUID(as_uuid=True), ForeignKey("categorias.id_categoria"), nullable=False
    )
    usuario_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_usuarios.id"), nullable=False
    )

    id_usuario_crea = Column(
        UUID(as_uuid=True), ForeignKey("tbl_usuarios.id"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("tbl_usuarios.id"), nullable=True
    )

    categoria = relationship("Categoria", back_populates="productos")
    # usuario = relationship(
    #     "Usuario", back_populates="productos", foreign_keys=[usuario_id]
    # )

    usuario_crea = relationship(
        "Usuario",
        foreign_keys=[id_usuario_crea],
    )
    usuario_edita = relationship(
        "Usuario",
        foreign_keys=[id_usuario_edita],
    )

    def __repr__(self):
        return f"<Producto(id_producto={self.id_producto}, nombre='{self.nombre}', precio={self.precio})>"
