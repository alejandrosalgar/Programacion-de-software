"""
API de Productos - Endpoints para gestión de productos
"""

from typing import List
from uuid import UUID

from crud.producto_crud import ProductoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ProductoCreate, ProductoResponse, ProductoUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[ProductoResponse])
async def obtener_productos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los productos con paginación."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.obtener_productos(skip=skip, limit=limit)
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}",
        )


@router.get("/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(producto_id: UUID, db: Session = Depends(get_db)):
    """Obtener un producto por ID."""
    try:
        producto_crud = ProductoCRUD(db)
        producto = producto_crud.obtener_producto(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener producto: {str(e)}",
        )


@router.get("/categoria/{categoria_id}", response_model=List[ProductoResponse])
async def obtener_productos_por_categoria(
    categoria_id: UUID, db: Session = Depends(get_db)
):
    """Obtener productos por categoría."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.obtener_productos_por_categoria(categoria_id)
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos por categoría: {str(e)}",
        )


@router.get("/usuario/{usuario_id}", response_model=List[ProductoResponse])
async def obtener_productos_por_usuario(
    usuario_id: UUID, db: Session = Depends(get_db)
):
    """Obtener productos por usuario."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.obtener_productos_por_usuario(usuario_id)
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos por usuario: {str(e)}",
        )


@router.get("/buscar/{nombre}", response_model=List[ProductoResponse])
async def buscar_productos_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """Buscar productos por nombre (búsqueda parcial)."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.buscar_productos_por_nombre(nombre)
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar productos: {str(e)}",
        )


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto_data: ProductoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto."""
    try:
        producto_crud = ProductoCRUD(db)
        producto = producto_crud.crear_producto(
            nombre=producto_data.nombre,
            descripcion=producto_data.descripcion,
            precio=producto_data.precio,
            stock=producto_data.stock,
            categoria_id=producto_data.categoria_id,
            usuario_id=producto_data.usuario_id,
        )
        return producto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}",
        )


@router.put("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: UUID, producto_data: ProductoUpdate, db: Session = Depends(get_db)
):
    """Actualizar un producto existente."""
    try:
        producto_crud = ProductoCRUD(db)

        # Verificar que el producto existe
        producto_existente = producto_crud.obtener_producto(producto_id)
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in producto_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return producto_existente

        producto_actualizado = producto_crud.actualizar_producto(
            producto_id, **campos_actualizacion
        )
        return producto_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}",
        )


@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
async def actualizar_stock(
    producto_id: UUID, nuevo_stock: int, db: Session = Depends(get_db)
):
    """Actualizar el stock de un producto."""
    try:
        producto_crud = ProductoCRUD(db)

        # Verificar que el producto existe
        producto_existente = producto_crud.obtener_producto(producto_id)
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        if nuevo_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock no puede ser negativo",
            )

        producto_actualizado = producto_crud.actualizar_stock(producto_id, nuevo_stock)
        return producto_actualizado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar stock: {str(e)}",
        )


@router.delete("/{producto_id}", response_model=RespuestaAPI)
async def eliminar_producto(producto_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un producto."""
    try:
        producto_crud = ProductoCRUD(db)

        # Verificar que el producto existe
        producto_existente = producto_crud.obtener_producto(producto_id)
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        eliminado = producto_crud.eliminar_producto(producto_id)
        if eliminado:
            return RespuestaAPI(mensaje="Producto eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar producto",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar producto: {str(e)}",
        )
