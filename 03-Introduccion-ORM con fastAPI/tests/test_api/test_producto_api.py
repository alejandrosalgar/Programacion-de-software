"""
Pruebas para los endpoints de la API de productos
"""
import pytest
from fastapi import status


class TestProductoAPI:
    """Pruebas para los endpoints de productos"""
    
    def test_obtener_productos_vacio(self, client):
        """Prueba obtener lista de productos cuando está vacía"""
        # Act
        response = client.get("/productos/")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_crear_producto_via_api(self, client, categoria_ejemplo, usuario_ejemplo):
        """Prueba crear un producto a través de la API"""
        # Arrange
        producto_data = {
            "nombre": "Producto API Test",
            "descripcion": "Descripción del producto",
            "precio": 100.50,
            "stock": 10,
            "categoria_id": str(categoria_ejemplo.id_categoria),
            "usuario_id": str(usuario_ejemplo.id)
        }
        
        # Act
        response = client.post("/productos/", json=producto_data)
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nombre"] == "Producto API Test"
        assert data["descripcion"] == "Descripción del producto"
        assert data["precio"] == 100.50
        assert data["stock"] == 10
        assert "id_producto" in data
    
    def test_crear_producto_falla_sin_datos_requeridos(self, client):
        """Prueba que crear producto sin datos requeridos falla"""
        # Arrange
        producto_data_incompleto = {
            "nombre": "Producto Test"
            # Faltan otros campos requeridos
        }
        
        # Act
        response = client.post("/productos/", json=producto_data_incompleto)
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_obtener_producto_por_id(self, client, categoria_ejemplo, usuario_ejemplo):
        """Prueba obtener un producto por ID"""
        # Arrange: Crear un producto primero
        producto_data = {
            "nombre": "Producto para Obtener",
            "descripcion": "Descripción",
            "precio": 50.0,
            "stock": 5,
            "categoria_id": str(categoria_ejemplo.id_categoria),
            "usuario_id": str(usuario_ejemplo.id)
        }
        create_response = client.post("/productos/", json=producto_data)
        producto_id = create_response.json()["id_producto"]
        
        # Act
        response = client.get(f"/productos/{producto_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id_producto"] == producto_id
        assert data["nombre"] == "Producto para Obtener"
    
    def test_obtener_producto_por_id_no_existente(self, client):
        """Prueba obtener un producto con ID inexistente"""
        # Arrange
        from uuid import uuid4
        producto_id_inexistente = str(uuid4())
        
        # Act
        response = client.get(f"/productos/{producto_id_inexistente}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrado" in response.json()["detail"].lower()
    
    def test_actualizar_producto_via_api(self, client, categoria_ejemplo, usuario_ejemplo):
        """Prueba actualizar un producto a través de la API"""
        # Arrange: Crear un producto primero
        producto_data = {
            "nombre": "Producto Original",
            "descripcion": "Descripción original",
            "precio": 100.0,
            "stock": 10,
            "categoria_id": str(categoria_ejemplo.id_categoria),
            "usuario_id": str(usuario_ejemplo.id)
        }
        create_response = client.post("/productos/", json=producto_data)
        producto_id = create_response.json()["id_producto"]
        
        # Datos de actualización
        update_data = {
            "nombre": "Producto Actualizado",
            "precio": 200.0
        }
        
        # Act
        response = client.put(f"/productos/{producto_id}", json=update_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nombre"] == "Producto Actualizado"
        assert data["precio"] == 200.0
        assert data["descripcion"] == "Descripción original"  # No cambió
    
    def test_actualizar_stock_via_api(self, client, categoria_ejemplo, usuario_ejemplo):
        """Prueba actualizar el stock de un producto"""
        # Arrange: Crear un producto primero
        producto_data = {
            "nombre": "Producto Stock",
            "descripcion": "Descripción",
            "precio": 50.0,
            "stock": 10,
            "categoria_id": str(categoria_ejemplo.id_categoria),
            "usuario_id": str(usuario_ejemplo.id)
        }
        create_response = client.post("/productos/", json=producto_data)
        producto_id = create_response.json()["id_producto"]
        
        # Act
        response = client.patch(f"/productos/{producto_id}/stock?nuevo_stock=25")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["stock"] == 25
    
    def test_actualizar_stock_negativo_falla(self, client, categoria_ejemplo, usuario_ejemplo):
        """Prueba que actualizar stock a negativo falla"""
        # Arrange: Crear un producto primero
        producto_data = {
            "nombre": "Producto Stock",
            "descripcion": "Descripción",
            "precio": 50.0,
            "stock": 10,
            "categoria_id": str(categoria_ejemplo.id_categoria),
            "usuario_id": str(usuario_ejemplo.id)
        }
        create_response = client.post("/productos/", json=producto_data)
        producto_id = create_response.json()["id_producto"]
        
        # Act
        response = client.patch(f"/productos/{producto_id}/stock?nuevo_stock=-5")
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "negativo" in response.json()["detail"].lower()
    
    def test_eliminar_producto_via_api(self, client, categoria_ejemplo, usuario_ejemplo):
        """Prueba eliminar un producto a través de la API"""
        # Arrange: Crear un producto primero
        producto_data = {
            "nombre": "Producto a Eliminar",
            "descripcion": "Descripción",
            "precio": 50.0,
            "stock": 10,
            "categoria_id": str(categoria_ejemplo.id_categoria),
            "usuario_id": str(usuario_ejemplo.id)
        }
        create_response = client.post("/productos/", json=producto_data)
        producto_id = create_response.json()["id_producto"]
        
        # Act
        response = client.delete(f"/productos/{producto_id}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["exito"] is True
        assert "eliminado" in data["mensaje"].lower()
        
        # Verificar que el producto ya no existe
        get_response = client.get(f"/productos/{producto_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_obtener_productos_por_categoria(self, client, categoria_ejemplo, usuario_ejemplo):
        """Prueba obtener productos filtrados por categoría"""
        # Arrange: Crear productos en la misma categoría
        for i in range(3):
            producto_data = {
                "nombre": f"Producto {i}",
                "descripcion": f"Descripción {i}",
                "precio": 10.0 * (i + 1),
                "stock": i,
                "categoria_id": str(categoria_ejemplo.id_categoria),
                "usuario_id": str(usuario_ejemplo.id)
            }
            client.post("/productos/", json=producto_data)
        
        # Act
        response = client.get(f"/productos/categoria/{categoria_ejemplo.id_categoria}")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        productos = response.json()
        assert len(productos) == 3

