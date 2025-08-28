from src.cuenta_ahorro import CuentaAhorro
from src.cuenta_corriente import CuentaCorriente

def menu():
    print("\n--- BANCO ---")
    print("1. Crear cuenta de ahorro")
    print("2. Crear cuenta corriente")
    print("3. Depositar")
    print("4. Retirar")
    print("5. Mostrar saldo")
    print("6. Salir")
    print("error")
def main() -> None:
    cuentas = {}

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            numero = input("Número de cuenta: ")
            cuentas[numero] = CuentaAhorro(numero)
            print("Cuenta de ahorro creada.")

        elif opcion == "2":
            numero = input("Número de cuenta: ")
            cuentas[numero] = CuentaCorriente(numero)
            print("Cuenta corriente creada.")

        elif opcion == "3":
            numero = input("Número de cuenta: ")
            monto = float(input("Monto: "))
            cuentas[numero].depositar(monto)

        elif opcion == "4":
            numero = input("Número de cuenta: ")
            monto = float(input("Monto: "))
            cuentas[numero].retirar(monto)

        elif opcion == "5":
            numero = input("Número de cuenta: ")
            print(cuentas[numero].mostrar_saldo())

        elif opcion == "6":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
