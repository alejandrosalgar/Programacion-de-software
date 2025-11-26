"""
Pruebas unitarias para ProductoCRUD
"""
import pytest
from uuid import uuid4
from crud.producto_crud import ProductoCRUD


class TestProductoCRUD:
    """Pruebas para las operaciones CRUD de productos"""
    
    def test_crear_producto_exitoso(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba crear un producto con datos válidos"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        
        # Act
        producto = producto_crud.crear_producto(
            nombre="Producto Test",
            descripcion="Descripción del producto test",
            precio=100.50,
            stock=10,
            categoria_id=categoria_ejemplo.id_categoria,
            usuario_id=usuario_ejemplo.id
        )
        
        # Assert
        assert producto is not None
        assert producto.nombre == "Producto Test"
        assert producto.descripcion == "Descripción del producto test"
        assert float(producto.precio) == 100.50
        assert producto.stock == 10
        assert producto.categoria_id == categoria_ejemplo.id_categoria
        assert producto.usuario_id == usuario_ejemplo.id
    
    def test_crear_producto_falla_con_nombre_vacio(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba que crear producto con nombre vacío falla"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        
        # Act & Assert
        with pytest.raises(ValueError, match="El nombre del producto es obligatorio"):
            producto_crud.crear_producto(
                nombre="",  # Nombre vacío
                descripcion="Descripción",
                precio=100.50,
                stock=10,
                categoria_id=categoria_ejemplo.id_categoria,
                usuario_id=usuario_ejemplo.id
            )
    
    def test_crear_producto_falla_con_precio_negativo(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba que crear producto con precio negativo falla"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        
        # Act & Assert
        with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
            producto_crud.crear_producto(
                nombre="Producto Test",
                descripcion="Descripción",
                precio=-10,  # Precio negativo
                stock=10,
                categoria_id=categoria_ejemplo.id_categoria,
                usuario_id=usuario_ejemplo.id
            )
    
    def test_crear_producto_falla_con_precio_cero(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba que crear producto con precio cero falla"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        
        # Act & Assert
        with pytest.raises(ValueError, match="El precio debe ser mayor a 0"):
            producto_crud.crear_producto(
                nombre="Producto Test",
                descripcion="Descripción",
                precio=0,  # Precio cero
                stock=10,
                categoria_id=categoria_ejemplo.id_categoria,
                usuario_id=usuario_ejemplo.id
            )
    
    def test_crear_producto_falla_con_stock_negativo(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba que crear producto con stock negativo falla"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        
        # Act & Assert
        with pytest.raises(ValueError, match="El stock no puede ser negativo"):
            producto_crud.crear_producto(
                nombre="Producto Test",
                descripcion="Descripción",
                precio=100.50,
                stock=-5,  # Stock negativo
                categoria_id=categoria_ejemplo.id_categoria,
                usuario_id=usuario_ejemplo.id
            )
    
    def test_crear_producto_falla_con_categoria_inexistente(self, db_session, usuario_ejemplo):
        """Prueba que crear producto con categoría inexistente falla"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        categoria_id_inexistente = uuid4()
        
        # Act & Assert
        with pytest.raises(ValueError, match="La categoría especificada no existe"):
            producto_crud.crear_producto(
                nombre="Producto Test",
                descripcion="Descripción",
                precio=100.50,
                stock=10,
                categoria_id=categoria_id_inexistente,
                usuario_id=usuario_ejemplo.id
            )
    
    def test_crear_producto_falla_con_usuario_inexistente(self, db_session, categoria_ejemplo):
        """Prueba que crear producto con usuario inexistente falla"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        usuario_id_inexistente = uuid4()
        
        # Act & Assert
        with pytest.raises(ValueError, match="El usuario especificado no existe"):
            producto_crud.crear_producto(
                nombre="Producto Test",
                descripcion="Descripción",
                precio=100.50,
                stock=10,
                categoria_id=categoria_ejemplo.id_categoria,
                usuario_id=usuario_id_inexistente
            )
    
    def test_obtener_producto_por_id_existente(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba obtener un producto por ID cuando existe"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        producto = producto_crud.crear_producto(
            nombre="Producto Test",
            descripcion="Descripción",
            precio=100.50,
            stock=10,
            categoria_id=categoria_ejemplo.id_categoria,
            usuario_id=usuario_ejemplo.id
        )
        
        # Act
        producto_obtenido = producto_crud.obtener_producto(producto.id_producto)
        
        # Assert
        assert producto_obtenido is not None
        assert producto_obtenido.id_producto == producto.id_producto
        assert producto_obtenido.nombre == "Producto Test"
    
    def test_obtener_producto_por_id_no_existente(self, db_session):
        """Prueba obtener un producto por ID cuando no existe"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        producto_id_inexistente = uuid4()
        
        # Act
        producto = producto_crud.obtener_producto(producto_id_inexistente)
        
        # Assert
        assert producto is None
    
    def test_obtener_productos_con_paginacion(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba obtener lista de productos con paginación"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        
        # Crear varios productos
        for i in range(5):
            producto_crud.crear_producto(
                nombre=f"Producto {i}",
                descripcion=f"Descripción {i}",
                precio=10.0 * (i + 1),
                stock=i,
                categoria_id=categoria_ejemplo.id_categoria,
                usuario_id=usuario_ejemplo.id
            )
        
        # Act
        productos = producto_crud.obtener_productos(skip=0, limit=3)
        
        # Assert
        assert len(productos) == 3
        assert productos[0].nombre == "Producto 0"
        assert productos[1].nombre == "Producto 1"
        assert productos[2].nombre == "Producto 2"
    
    def test_actualizar_producto_exitoso(self, db_session, categoria_ejemplo, usuario_ejemplo, admin_ejemplo):
        """Prueba actualizar un producto existente"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        producto = producto_crud.crear_producto(
            nombre="Producto Original",
            descripcion="Descripción original",
            precio=100.50,
            stock=10,
            categoria_id=categoria_ejemplo.id_categoria,
            usuario_id=usuario_ejemplo.id
        )
        
        # Act
        producto_actualizado = producto_crud.actualizar_producto(
            producto.id_producto,
            id_usuario_edita=admin_ejemplo.id,
            nombre="Producto Actualizado",
            precio=200.75
        )
        
        # Assert
        assert producto_actualizado is not None
        assert producto_actualizado.nombre == "Producto Actualizado"
        assert float(producto_actualizado.precio) == 200.75
        assert producto_actualizado.descripcion == "Descripción original"  # No cambió
    
    def test_actualizar_producto_no_existente(self, db_session, admin_ejemplo):
        """Prueba actualizar un producto que no existe"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        producto_id_inexistente = uuid4()
        
        # Act
        resultado = producto_crud.actualizar_producto(
            producto_id_inexistente,
            id_usuario_edita=admin_ejemplo.id,
            nombre="Nuevo nombre"
        )
        
        # Assert
        assert resultado is None
    
    def test_eliminar_producto_exitoso(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba eliminar un producto existente"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        producto = producto_crud.crear_producto(
            nombre="Producto a Eliminar",
            descripcion="Descripción",
            precio=100.50,
            stock=10,
            categoria_id=categoria_ejemplo.id_categoria,
            usuario_id=usuario_ejemplo.id
        )
        producto_id = producto.id_producto
        
        # Act
        eliminado = producto_crud.eliminar_producto(producto_id)
        
        # Assert
        assert eliminado is True
        producto_verificacion = producto_crud.obtener_producto(producto_id)
        assert producto_verificacion is None
    
    def test_eliminar_producto_no_existente(self, db_session):
        """Prueba eliminar un producto que no existe"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        producto_id_inexistente = uuid4()
        
        # Act
        eliminado = producto_crud.eliminar_producto(producto_id_inexistente)
        
        # Assert
        assert eliminado is False
    
    def test_buscar_productos_por_nombre(self, db_session, categoria_ejemplo, usuario_ejemplo):
        """Prueba buscar productos por nombre"""
        # Arrange
        producto_crud = ProductoCRUD(db_session)
        producto_crud.crear_producto(
            nombre="Laptop HP",
            descripcion="Laptop",
            precio=500.0,
            stock=5,
            categoria_id=categoria_ejemplo.id_categoria,
            usuario_id=usuario_ejemplo.id
        )
        producto_crud.crear_producto(
            nombre="Mouse Logitech",
            descripcion="Mouse",
            precio=25.0,
            stock=10,
            categoria_id=categoria_ejemplo.id_categoria,
            usuario_id=usuario_ejemplo.id
        )
        
        # Act
        productos = producto_crud.buscar_productos_por_nombre("Laptop")
        
        # Assert
        assert len(productos) == 1
        assert productos[0].nombre == "Laptop HP"

