"""
Operaciones CRUD para Producto
"""

from typing import List, Optional
from uuid import UUID

from entities.producto import Producto
from sqlalchemy.orm import Session


class ProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        categoria_id: UUID,
        usuario_id: UUID,
        id_usuario_crea: UUID = None,
    ) -> Producto:
        """
        Crear un nuevo producto con validaciones

        Args:
            nombre: Nombre del producto (máximo 200 caracteres)
            descripcion: Descripción del producto
            precio: Precio del producto (debe ser positivo)
            stock: Cantidad en stock (no puede ser negativo)
            categoria_id: UUID de la categoría
            usuario_id: UUID del usuario propietario
            id_usuario_crea: UUID del usuario que crea el producto

        Returns:
            Producto creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del producto es obligatorio")

        if len(nombre) > 200:
            raise ValueError("El nombre no puede exceder 200 caracteres")

        if not descripcion or len(descripcion.strip()) == 0:
            raise ValueError("La descripción del producto es obligatoria")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        from entities.categoria import Categoria

        categoria = (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == categoria_id)
            .first()
        )
        if not categoria:
            raise ValueError("La categoría especificada no existe")

        from entities.usuario import Usuario

        usuario = (
            self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        )
        if not usuario:
            raise ValueError("El usuario especificado no existe")

        if id_usuario_crea is None:
            id_usuario_crea = usuario_id

        producto = Producto(
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            precio=precio,
            stock=stock,
            categoria_id=categoria_id,
            usuario_id=usuario_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_producto(self, producto_id: UUID) -> Optional[Producto]:
        """
        Obtener un producto por ID

        Args:
            producto_id: UUID del producto

        Returns:
            Producto encontrado o None
        """
        return (
            self.db.query(Producto).filter(Producto.id_producto == producto_id).first()
        )

    def obtener_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        """
        Obtener lista de productos con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de productos
        """
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def obtener_productos_por_categoria(self, categoria_id: UUID) -> List[Producto]:
        """
        Obtener productos por categoría

        Args:
            categoria_id: UUID de la categoría

        Returns:
            Lista de productos de la categoría
        """
        return (
            self.db.query(Producto).filter(Producto.categoria_id == categoria_id).all()
        )

    def obtener_productos_por_usuario(self, usuario_id: UUID) -> List[Producto]:
        """
        Obtener productos por usuario

        Args:
            usuario_id: UUID del usuario

        Returns:
            Lista de productos del usuario
        """
        return self.db.query(Producto).filter(Producto.usuario_id == usuario_id).all()

    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """
        Buscar productos por nombre (búsqueda parcial)

        Args:
            nombre: Texto a buscar en el nombre

        Returns:
            Lista de productos que coinciden
        """
        return self.db.query(Producto).filter(Producto.nombre.contains(nombre)).all()

    def actualizar_producto(
        self, producto_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Producto]:
        """
        Actualizar un producto con validaciones

        Args:
            producto_id: UUID del producto
            id_usuario_edita: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Producto actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        producto = self.obtener_producto(producto_id)
        if not producto:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del producto es obligatorio")
            if len(nombre) > 200:
                raise ValueError("El nombre no puede exceder 200 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "descripcion" in kwargs:
            descripcion = kwargs["descripcion"]
            if not descripcion or len(descripcion.strip()) == 0:
                raise ValueError("La descripción del producto es obligatoria")
            kwargs["descripcion"] = descripcion.strip()

        if "precio" in kwargs:
            precio = kwargs["precio"]
            if precio <= 0:
                raise ValueError("El precio debe ser mayor a 0")

        if "stock" in kwargs:
            stock = kwargs["stock"]
            if stock < 0:
                raise ValueError("El stock no puede ser negativo")

        if "categoria_id" in kwargs:
            from entities.categoria import Categoria

            categoria = (
                self.db.query(Categoria)
                .filter(Categoria.id_categoria == kwargs["categoria_id"])
                .first()
            )
            if not categoria:
                raise ValueError("La categoría especificada no existe")

        if "usuario_id" in kwargs:
            from entities.usuario import Usuario

            usuario = (
                self.db.query(Usuario)
                .filter(Usuario.id == kwargs["usuario_id"])
                .first()
            )
            if not usuario:
                raise ValueError("El usuario especificado no existe")

        if id_usuario_edita is None:
            from entities.usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el producto"
                )
            id_usuario_edita = admin.id

        producto.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(producto, key):
                setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def actualizar_stock(
        self, producto_id: UUID, nuevo_stock: int
    ) -> Optional[Producto]:
        """
        Actualizar el stock de un producto

        Args:
            producto_id: UUID del producto
            nuevo_stock: Nueva cantidad en stock

        Returns:
            Producto actualizado o None
        """
        return self.actualizar_producto(producto_id, stock=nuevo_stock)

    def eliminar_producto(self, producto_id: UUID) -> bool:
        """
        Eliminar un producto

        Args:
            producto_id: UUID del producto

        Returns:
            True si se eliminó, False si no existe
        """
        producto = self.obtener_producto(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False
