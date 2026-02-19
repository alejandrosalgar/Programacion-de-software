from src.entities.cuenta_ahorro import CuentaAhorro
from src.entities.cuenta_corriente import CuentaCorriente

TipoCuenta = CuentaAhorro | CuentaCorriente


def menu() -> None:
    print("\n--- BANCO ---")
    print("1. Crear cuenta de ahorro")
    print("2. Crear cuenta corriente")
    print("3. Depositar")
    print("4. Retirar")
    print("5. Mostrar saldo")
    print("6. Salir")


def validar_numero_cuenta(numero: str) -> bool:
    """Valida que el número de cuenta sea solo dígitos y no vacío."""
    numero = numero.strip()
    if len(numero) == 0:
        return False
    return numero.isdigit()


def validar_texto_no_vacio(texto: str) -> bool:
    """Valida que el texto no esté vacío después de quitar espacios."""
    return len(texto.strip()) > 0


def validar_monto_o_cero(monto_str: str) -> tuple[bool, float]:
    """Como validar_monto pero permite 0 (para sobregiro, saldo inicial, etc.)."""
    monto_str = monto_str.strip()
    if len(monto_str) == 0:
        return False, 0.0
    if monto_str == "0" or monto_str == "0.0":
        return True, 0.0
    return validar_monto(monto_str)


def validar_porcentaje(porcentaje_str: str) -> tuple[bool, float]:
    """
    Valida porcentaje (0-100). Retorna (True, valor/100) o (False, 0.0).
    Ej: "2.5" -> (True, 0.025). Permite 0%.
    """
    s = porcentaje_str.strip()
    if s == "0" or s == "0.0":
        return True, 0.0
    ok, valor = validar_monto(porcentaje_str)
    if not ok:
        return False, 0.0
    if valor > 100:
        return False, 0.0
    return True, valor / 100.0


def validar_monto(monto_str: str) -> tuple[bool, float]:
    """
    Valida que la cadena sea un número positivo (entero o decimal).
    Sin usar try/except: retorna (True, valor) o (False, 0.0).
    """
    monto_str = monto_str.strip()
    if len(monto_str) == 0:
        return False, 0.0
    partes = monto_str.split(".")
    if len(partes) > 2:
        return False, 0.0
    entero = partes[0]
    decimal = partes[1] if len(partes) == 2 else ""
    if not entero.isdigit() or (decimal != "" and not decimal.isdigit()):
        return False, 0.0
    valor_entero = int(entero)
    valor_decimal = 0.0
    if decimal != "":
        valor_decimal = int(decimal) / (10 ** len(decimal))
    valor = float(valor_entero) + valor_decimal
    if valor <= 0:
        return False, 0.0
    return True, valor


def cuenta_existe(numero: str, cuentas: dict[str, TipoCuenta]) -> bool:
    return numero.strip() in cuentas


def main() -> None:
    """
    Menú: Crear cuenta ahorro/corriente, Depositar, Retirar, Mostrar saldo, Salir.
    Validación de datos, ciclo en el menú, POO básica, sin try/except.
    """
    cuentas: dict[str, TipoCuenta] = {}

    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion not in ("1", "2", "3", "4", "5", "6"):
            print("Opción no válida. Elija 1 a 6.")
            continue

        if opcion == "1":
            numero = input("Número de cuenta: ").strip()
            if not validar_numero_cuenta(numero):
                print("Número de cuenta inválido. Use solo dígitos.")
                continue
            if cuenta_existe(numero, cuentas):
                print("Ya existe una cuenta con ese número. No se puede duplicar.")
                continue
            titular = input("Nombre del titular: ").strip()
            if not validar_texto_no_vacio(titular):
                print("El titular no puede estar vacío.")
                continue
            saldo_str = input("Saldo inicial (Enter = 0): ").strip()
            saldo = 0.0
            if saldo_str:
                ok_s, saldo = validar_monto_o_cero(saldo_str)
                if not ok_s:
                    print("Saldo inválido. Se usará 0.")
                    saldo = 0.0
            interes_str = input("Tasa de interés % (Enter = 2): ").strip()
            interes = 0.02
            if interes_str:
                ok_i, interes = validar_porcentaje(interes_str)
                if not ok_i:
                    print("Porcentaje inválido. Se usará 2%.")
                    interes = 0.02
            meta_str = input("Meta de ahorro en $ (Enter = sin meta): ").strip()
            meta = 0.0
            if meta_str:
                ok_m, meta = validar_monto(meta_str)
                if not ok_m:
                    meta = 0.0
            cuentas[numero] = CuentaAhorro(numero, titular, saldo, interes, meta)
            print("Cuenta de ahorro creada correctamente.")

        elif opcion == "2":
            numero = input("Número de cuenta: ").strip()
            if not validar_numero_cuenta(numero):
                print("Número de cuenta inválido. Use solo dígitos.")
                continue
            if cuenta_existe(numero, cuentas):
                print("Ya existe una cuenta con ese número. No se puede duplicar.")
                continue
            titular = input("Nombre del titular: ").strip()
            if not validar_texto_no_vacio(titular):
                print("El titular no puede estar vacío.")
                continue
            saldo_str = input("Saldo inicial (Enter = 0): ").strip()
            saldo = 0.0
            if saldo_str:
                ok_s, saldo = validar_monto_o_cero(saldo_str)
                if not ok_s:
                    print("Saldo inválido. Se usará 0.")
                    saldo = 0.0
            sobregiro_str = input("Límite de sobregiro $ (Enter = 500): ").strip()
            sobregiro = 500.0
            if sobregiro_str:
                ok_sob, sobregiro = validar_monto_o_cero(sobregiro_str)
                if not ok_sob:
                    print("Monto inválido. Se usará 500.")
                    sobregiro = 500.0
            cuentas[numero] = CuentaCorriente(numero, titular, saldo, sobregiro)
            print("Cuenta corriente creada correctamente.")

        elif opcion == "3":
            numero = input("Número de cuenta: ").strip()
            if not cuenta_existe(numero, cuentas):
                print("La cuenta no existe.")
                continue
            monto_str = input("Monto a depositar: ").strip()
            ok, monto = validar_monto(monto_str)
            if not ok:
                print("Monto inválido. Ingrese un número mayor a cero.")
                continue
            cuentas[numero].depositar(monto)

        elif opcion == "4":
            numero = input("Número de cuenta: ").strip()
            if not cuenta_existe(numero, cuentas):
                print("La cuenta no existe.")
                continue
            monto_str = input("Monto a retirar: ").strip()
            ok, monto = validar_monto(monto_str)
            if not ok:
                print("Monto inválido. Ingrese un número mayor a cero.")
                continue
            cuentas[numero].retirar(monto)

        elif opcion == "5":
            numero = input("Número de cuenta: ").strip()
            if not cuenta_existe(numero, cuentas):
                print("La cuenta no existe.")
                continue
            print(cuentas[numero].mostrar_saldo())

        elif opcion == "6":
            print("Saliendo del programa. Hasta pronto.")
            break


if __name__ == "__main__":
    main()
