"""
Entidad Persona: base de trazabilidad.
Las demás entidades referencian a Persona en id_usuario_crea e id_usuario_edita.
"""

import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Usuario(Base):
    """Modelo ORM Persona. Es quien crea/edita registros (trazabilidad)."""

    __tablename__ = "usuario"

    id_usuario = Column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    nombre_usuario = Column(String(150), nullable=False)
    activo = Column(Boolean, default=True)
    rol = Column(String(50), nullable=False)
    contrasena = Column(String(255), nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())


class PersonaBase(BaseModel):
    """Esquema base con validaciones simples."""

    nombre: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    activo: bool = True


class PersonaCreate(PersonaBase):
    """Esquema para creación."""

    pass


class PersonaUpdate(BaseModel):
    """Esquema para actualización parcial."""

    nombre_usuario: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None


class PersonaResponse(PersonaBase):
    """Esquema de respuesta (lectura)."""

    id_usuario: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True
