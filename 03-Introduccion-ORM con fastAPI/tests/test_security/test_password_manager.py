"""
Pruebas unitarias para PasswordManager
"""
import pytest
from auth.security import PasswordManager


class TestPasswordManager:
    """Pruebas para el gestor de contraseñas"""
    
    def test_hash_password_genera_hash_diferente(self):
        """Prueba que cada hash generado es único (por el salt)"""
        # Arrange
        password = "MiPassword123!"
        
        # Act
        hash1 = PasswordManager.hash_password(password)
        hash2 = PasswordManager.hash_password(password)
        
        # Assert
        assert hash1 != hash2, "Cada hash debe ser diferente debido al salt"
        assert ":" in hash1, "El hash debe contener el separador ':'"
        assert ":" in hash2, "El hash debe contener el separador ':'"
    
    def test_verify_password_correcta(self):
        """Prueba verificar una contraseña correcta"""
        # Arrange
        password = "MiPassword123!"
        password_hash = PasswordManager.hash_password(password)
        
        # Act
        es_valida = PasswordManager.verify_password(password, password_hash)
        
        # Assert
        assert es_valida is True
    
    def test_verify_password_incorrecta(self):
        """Prueba verificar una contraseña incorrecta"""
        # Arrange
        password = "MiPassword123!"
        password_hash = PasswordManager.hash_password(password)
        wrong_password = "WrongPassword123!"
        
        # Act
        es_valida = PasswordManager.verify_password(wrong_password, password_hash)
        
        # Assert
        assert es_valida is False
    
    def test_verify_password_hash_invalido(self):
        """Prueba verificar contraseña con hash inválido"""
        # Arrange
        password = "MiPassword123!"
        hash_invalido = "hash_sin_formato_correcto"
        
        # Act
        es_valida = PasswordManager.verify_password(password, hash_invalido)
        
        # Assert
        assert es_valida is False
    
    def test_validate_password_strength_valida(self):
        """Prueba validar una contraseña válida"""
        # Arrange
        password = "MiPassword123!"
        
        # Act
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        # Assert
        assert es_valida is True
        assert mensaje == "Contraseña válida"
    
    def test_validate_password_strength_corta(self):
        """Prueba validar una contraseña muy corta"""
        # Arrange
        password = "Short1!"
        
        # Act
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        # Assert
        assert es_valida is False
        assert "8 caracteres" in mensaje
    
    def test_validate_password_strength_sin_mayuscula(self):
        """Prueba validar una contraseña sin mayúscula"""
        # Arrange
        password = "mipassword123!"
        
        # Act
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        # Assert
        assert es_valida is False
        assert "mayúscula" in mensaje.lower()
    
    def test_validate_password_strength_sin_minuscula(self):
        """Prueba validar una contraseña sin minúscula"""
        # Arrange
        password = "MIPASSWORD123!"
        
        # Act
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        # Assert
        assert es_valida is False
        assert "minúscula" in mensaje.lower()
    
    def test_validate_password_strength_sin_numero(self):
        """Prueba validar una contraseña sin número"""
        # Arrange
        password = "MiPassword!"
        
        # Act
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        # Assert
        assert es_valida is False
        assert "número" in mensaje.lower()
    
    def test_validate_password_strength_sin_caracter_especial(self):
        """Prueba validar una contraseña sin carácter especial"""
        # Arrange
        password = "MiPassword123"
        
        # Act
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        # Assert
        assert es_valida is False
        assert "especial" in mensaje.lower()
    
    def test_validate_password_strength_muy_larga(self):
        """Prueba validar una contraseña muy larga"""
        # Arrange
        password = "A" * 129 + "1!"  # Más de 128 caracteres
        
        # Act
        es_valida, mensaje = PasswordManager.validate_password_strength(password)
        
        # Assert
        assert es_valida is False
        assert "128 caracteres" in mensaje
    
    def test_generate_secure_password(self):
        """Prueba generar una contraseña segura"""
        # Act
        password = PasswordManager.generate_secure_password(12)
        
        # Assert
        assert len(password) == 12
        assert any(c.isupper() for c in password)
        assert any(c.islower() for c in password)
        assert any(c.isdigit() for c in password)
        assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    def test_generate_secure_password_longitud_personalizada(self):
        """Prueba generar contraseña con longitud personalizada"""
        # Act
        password = PasswordManager.generate_secure_password(20)
        
        # Assert
        assert len(password) == 20
    
    def test_hash_y_verify_round_trip(self):
        """Prueba el ciclo completo: hash y verificación"""
        # Arrange
        password = "MiPasswordSegura123!"
        
        # Act
        password_hash = PasswordManager.hash_password(password)
        es_valida = PasswordManager.verify_password(password, password_hash)
        
        # Assert
        assert es_valida is True, "La contraseña debe ser verificable después del hash"

