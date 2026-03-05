"""
API de Categorías - Endpoints para gestión de categorías
"""

from typing import List
from uuid import UUID

from crud.categoria_crud import CategoriaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import CategoriaCreate, CategoriaResponse, CategoriaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/", response_model=List[CategoriaResponse])
async def obtener_categorias(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todas las categorías con paginación."""
    try:
        categoria_crud = CategoriaCRUD(db)
        categorias = categoria_crud.obtener_categorias(skip=skip, limit=limit)
        return categorias
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías: {str(e)}",
        )


@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def obtener_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    """Obtener una categoría por ID."""
    try:
        categoria_crud = CategoriaCRUD(db)
        categoria = categoria_crud.obtener_categoria(categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        return categoria
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categoría: {str(e)}",
        )


@router.get("/nombre/{nombre}", response_model=CategoriaResponse)
async def obtener_categoria_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """Obtener una categoría por nombre."""
    try:
        categoria_crud = CategoriaCRUD(db)
        categoria = categoria_crud.obtener_categoria_por_nombre(nombre)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        return categoria
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categoría: {str(e)}",
        )


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    categoria_data: CategoriaCreate, db: Session = Depends(get_db)
):
    """Crear una nueva categoría."""
    try:
        categoria_crud = CategoriaCRUD(db)
        categoria = categoria_crud.crear_categoria(
            nombre=categoria_data.nombre,
            descripcion=categoria_data.descripcion,
        )
        return categoria
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear categoría: {str(e)}",
        )


@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def actualizar_categoria(
    categoria_id: UUID, categoria_data: CategoriaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una categoría existente."""
    try:
        categoria_crud = CategoriaCRUD(db)

        # Verificar que la categoría existe
        categoria_existente = categoria_crud.obtener_categoria(categoria_id)
        if not categoria_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in categoria_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return categoria_existente

        categoria_actualizada = categoria_crud.actualizar_categoria(
            categoria_id, **campos_actualizacion
        )
        return categoria_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar categoría: {str(e)}",
        )


@router.delete("/{categoria_id}", response_model=RespuestaAPI)
async def eliminar_categoria(categoria_id: UUID, db: Session = Depends(get_db)):
    """Eliminar una categoría."""
    try:
        categoria_crud = CategoriaCRUD(db)

        # Verificar que la categoría existe
        categoria_existente = categoria_crud.obtener_categoria(categoria_id)
        if not categoria_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )

        eliminada = categoria_crud.eliminar_categoria(categoria_id)
        if eliminada:
            return RespuestaAPI(mensaje="Categoría eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar categoría",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar categoría: {str(e)}",
        )
