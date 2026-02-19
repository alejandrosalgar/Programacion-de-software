# Ejemplo de examen — Sistema de cuentas bancarias

Proyecto de **referencia** para el examen de Programación de Software. Sirve como guía de estructura, POO, estilo PEP 8 y validaciones sin `try/except`.

## Contenido del ejemplo

- **POO:** Clase base `Cuenta` y subclases `CuentaAhorro` y `CuentaCorriente`.
- **Estructura modular:** Entidades en `src/entities/`.
- **Menú en consola:** `main.py` con crear cuenta, depositar, retirar y mostrar saldo.
- **Validación explícita:** Funciones como `validar_monto`, `validar_numero_cuenta`, etc., sin uso de `try/except`.
- **Estilo:** Código preparado para formatear con **Black** (PEP 8).

## Estructura del proyecto

```
02-Ejemplo-examen-1/
├── README.md           # Este archivo
├── main.py             # Punto de entrada y menú
├── enunciado-examen.tex
└── src/
    └── entities/
        ├── cuenta.py           # Clase base Cuenta
        ├── cuenta_ahorro.py    # CuentaAhorro (interés, meta)
        └── cuenta_corriente.py # CuentaCorriente (sobregiro)
```

## Cómo ejecutar

Desde la raíz del proyecto (carpeta `02-Ejemplo-examen-1`):

```bash
python main.py
```

Requisito: Python 3.10+ (por el uso de `tuple[bool, float]` y sintaxis de tipos).

## Qué revisar (alineado al enunciado)

| Criterio        | En este ejemplo |
|-----------------|-----------------|
| **POO**         | Encapsulamiento (`_numero`, `_saldo`), `@property`, herencia (`Cuenta` → `CuentaAhorro`, `CuentaCorriente`), type hints en métodos. |
| **Estructura**  | Módulos en `src/entities/`, imports relativos (`.cuenta`). |
| **Validación**  | `validar_monto`, `validar_numero_cuenta`, etc. retornan `(bool, valor)`; no se usan `try/except` para validar entradas. |
| **PEP 8 / Black** | Nombres en `snake_case` y `PascalCase`, líneas dentro del límite; ejecutar `black .` antes de entregar. |

El **dominio del negocio** (qué debe hacer exactamente el programa) lo define el docente; este proyecto solo ilustra la forma de organizar código y cumplir requisitos técnicos del examen.

## Formatear con Black

En la raíz del proyecto:

```bash
black .
```

---

*Documento de apoyo al curso de Programación de Software. Fechas y entregas según enunciado del examen.*
