"""
API de Autenticación - Endpoints para login y autenticación
"""

from uuid import UUID

from crud.usuario_crud import UsuarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import RespuestaAPI, UsuarioLogin, UsuarioResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["autenticación"])


@router.post("/login", response_model=UsuarioResponse)
async def login(login_data: UsuarioLogin, db: Session = Depends(get_db)):
    """Autenticar un usuario con nombre de usuario/email y contraseña."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.autenticar_usuario(
            login_data.nombre_usuario, login_data.contraseña
        )

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas o usuario inactivo",
            )

        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el login: {str(e)}",
        )


@router.post("/crear-admin", response_model=RespuestaAPI)
async def crear_usuario_admin(db: Session = Depends(get_db)):
    """Crear usuario administrador por defecto."""
    try:
        usuario_crud = UsuarioCRUD(db)

        # Verificar si ya existe un admin por defecto
        admin_existente = usuario_crud.obtener_admin_por_defecto()
        if admin_existente:
            return RespuestaAPI(
                mensaje="Ya existe un usuario administrador por defecto",
                exito=True,
                datos={"admin_id": str(admin_existente.id)},
            )

        # Crear admin por defecto
        from auth.security import PasswordManager

        contraseña_admin = PasswordManager.generate_secure_password(12)

        admin = usuario_crud.crear_usuario(
            nombre="Administrador del Sistema",
            nombre_usuario="admin",
            email="admin@system.com",
            contraseña=contraseña_admin,
            es_admin=True,
        )

        return RespuestaAPI(
            mensaje="Usuario administrador creado exitosamente",
            exito=True,
            datos={
                "admin_id": str(admin.id),
                "contraseña_temporal": contraseña_admin,
                "mensaje": "IMPORTANTE: Cambie esta contraseña en su primer inicio de sesión",
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear administrador: {str(e)}",
        )


@router.get("/verificar/{usuario_id}", response_model=RespuestaAPI)
async def verificar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Verificar si un usuario existe y está activo."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario(usuario_id)

        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        return RespuestaAPI(
            mensaje="Usuario verificado exitosamente",
            exito=True,
            datos={
                "usuario_id": str(usuario.id),
                "nombre": usuario.nombre,
                "email": usuario.email,
                "activo": usuario.activo,
                "es_admin": usuario.es_admin,
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar usuario: {str(e)}",
        )


@router.get("/estado", response_model=RespuestaAPI)
async def estado_autenticacion():
    """Verificar el estado del sistema de autenticación."""
    return RespuestaAPI(
        mensaje="Sistema de autenticación funcionando correctamente",
        exito=True,
        datos={
            "sistema": "Sistema de Gestión de Productos",
            "version": "1.0.0",
            "autenticacion": "Activa",
        },
    )
