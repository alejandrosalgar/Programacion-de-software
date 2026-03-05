"""
Punto de entrada: inicio de sesión (o creación del primer usuario)
y menú CRUD para Categoría, Producto y Pedido.
"""

import sys
from typing import Optional
from uuid import UUID

sys.path.insert(0, ".")

from src.crud import categoria as crud_categoria
from src.crud import pedido as crud_pedido
from src.crud import producto as crud_producto
from src.crud import usuario as crud_usuario
from src.entities.usuario import Usuario


def leer_texto(mensaje: str, default: str = "") -> str:
    s = input(mensaje).strip()
    return s if s else default


def leer_float(mensaje: str, default: float = 0.0) -> float:
    try:
        return float(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_int(mensaje: str, default: int = 0) -> int:
    try:
        return int(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario() -> Optional[Usuario]:
    """
    Si no hay usuarios, ofrece crear el primero.
    Luego pide login hasta que sea correcto.
    Devuelve el Usuario logueado.
    """
    if not crud_usuario.hay_usuarios():
        print("\n--- No hay usuarios en el sistema ---")
        print("Crea el primer usuario para poder entrar.\n")
        nombre = leer_texto("Nombre de usuario: ")
        if not nombre:
            print("Nombre obligatorio.")
            return None
        contra = leer_texto("Contraseña: ")
        if not contra:
            print("Contraseña obligatoria.")
            return None
        rol = leer_texto("Rol (por defecto 'admin'): ") or "admin"
        try:
            usuario_creado = crud_usuario.crear(
                nombre_usuario=nombre, contrasena=contra, rol=rol
            )
            print(
                f"\nUsuario '{usuario_creado.nombre_usuario}' creado. Inicia sesión.\n"
            )
        except Exception as e:
            print("Error al crear usuario:", e)
            return None

    while True:
        print("--- Inicio de sesión ---")
        nombre = leer_texto("Usuario: ")
        contra = leer_texto("Contraseña: ")
        if not nombre or not contra:
            print("Usuario y contraseña obligatorios.\n")
            continue
        usuario = crud_usuario.login(nombre, contra)
        if usuario:
            print(f"\nBienvenido, {usuario.nombre_usuario} ({usuario.rol}).\n")
            return usuario
        print("Usuario o contraseña incorrectos.\n")


def menu_categorias(usuario_id: UUID) -> None:
    while True:
        print("\n--- Categorías ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in crud_categoria.obtener_todos():
                print(f"  {c.id_categoria} | {c.nombre} | {c.descripcion or '-'}")
        elif op == "2":
            nombre = leer_texto("Nombre categoría: ")
            desc = leer_texto("Descripción (opcional): ")
            if nombre:
                try:
                    crud_categoria.crear(nombre, usuario_id, desc or None)
                    print("Categoría creada.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Nombre obligatorio.")
        elif op == "3":
            id_cat = leer_uuid("ID categoría a actualizar: ")
            if not id_cat:
                print("ID inválido.")
                continue
            c = crud_categoria.obtener_por_id(id_cat)
            if not c:
                print("No existe esa categoría.")
                continue
            nombre = leer_texto(f"Nuevo nombre (actual: {c.nombre}): ") or c.nombre
            desc = leer_texto(f"Nueva descripción (actual: {c.descripcion or ''}): ")
            crud_categoria.actualizar(
                id_cat,
                usuario_id,
                nombre=nombre,
                descripcion=desc if desc else c.descripcion,
            )
            print("Actualizado.")
        elif op == "4":
            id_cat = leer_uuid("ID categoría a eliminar: ")
            if id_cat and crud_categoria.eliminar(id_cat):
                print("Eliminada.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


def menu_productos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Productos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for p in crud_producto.obtener_todos():
                print(
                    f"  {p.id_producto} | {p.nombre} | precio={p.precio} | stock={p.stock} | cat={p.id_categoria}"
                )
        elif op == "2":
            nombre = leer_texto("Nombre producto: ")
            id_cat = leer_uuid("ID categoría: ")
            precio = leer_float("Precio: ")
            stock = leer_int("Stock: ")
            desc = leer_texto("Descripción (opcional): ")
            if nombre and id_cat is not None:
                if not crud_categoria.obtener_por_id(id_cat):
                    print("Esa categoría no existe.")
                else:
                    try:
                        crud_producto.crear(
                            nombre, id_cat, usuario_id, precio, stock, desc or None
                        )
                        print("Producto creado.")
                    except Exception as e:
                        print("Error:", e)
            else:
                print("Nombre e ID categoría obligatorios.")
        elif op == "3":
            id_prod = leer_uuid("ID producto a actualizar: ")
            if not id_prod:
                print("ID inválido.")
                continue
            p = crud_producto.obtener_por_id(id_prod)
            if not p:
                print("No existe ese producto.")
                continue
            nombre = leer_texto(f"Nuevo nombre (actual: {p.nombre}): ") or p.nombre
            precio = leer_float(f"Nuevo precio (actual: {p.precio}): ")
            if precio <= 0:
                precio = p.precio
            stock = leer_int(f"Nuevo stock (actual: {p.stock}): ")
            if stock < 0:
                stock = p.stock
            crud_producto.actualizar(
                id_prod, usuario_id, nombre=nombre, precio=precio, stock=stock
            )
            print("Actualizado.")
        elif op == "4":
            id_prod = leer_uuid("ID producto a eliminar: ")
            if id_prod and crud_producto.eliminar(id_prod):
                print("Eliminado.")
            else:
                print("No se pudo eliminar.")


def menu_pedidos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Pedidos ---")
        print("1. Listar todos  2. Listar míos  3. Crear  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for p in crud_pedido.obtener_todos():
                print(
                    f"  {p.id_pedido} | usuario={p.id_usuario} | total={p.total_pagado}"
                )
        elif op == "2":
            for p in crud_pedido.obtener_por_usuario(usuario_id):
                print(f"  {p.id_pedido} | total={p.total_pagado}")
        elif op == "3":
            total = leer_float("Total pagado: ")
            if total >= 0:
                try:
                    crud_pedido.crear(total, usuario_id, usuario_id)
                    print("Pedido creado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Total debe ser >= 0.")
        elif op == "4":
            id_ped = leer_uuid("ID pedido a eliminar: ")
            if id_ped and crud_pedido.eliminar(id_ped):
                print("Eliminado.")
            else:
                print("No se pudo eliminar.")


def main() -> None:
    usuario = ingresar_o_crear_usuario()
    if not usuario:
        print("No se pudo iniciar sesión. Saliendo.")
        return

    while True:
        print("\n========== Menú principal ==========")
        print("1. Categorías  2. Productos  3. Pedidos  0. Salir")
        op = leer_texto("Opción: ")
        if op == "0":
            print(f"Hasta luego {usuario.nombre_usuario}.")
            break
        if op == "1":
            menu_categorias(usuario.id_usuario)
        elif op == "2":
            menu_productos(usuario.id_usuario)
        elif op == "3":
            menu_pedidos(usuario.id_usuario)
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
