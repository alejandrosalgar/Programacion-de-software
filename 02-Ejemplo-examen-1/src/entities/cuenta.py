class Cuenta:
    def __init__(self, numero: int, saldo: float = 0):
        self._numero = numero
        self._saldo = saldo

    def depositar(self, monto: float) -> None:
        self._saldo += monto

    def retirar(self, monto: float) -> None:
        if monto <= self._saldo:
            self._saldo -= monto
        else:
            print("Fondos insuficientes")

    def mostrar_saldo(self) -> str:
        return f"Cuenta {self._numero} - Saldo: {self._saldo}"
