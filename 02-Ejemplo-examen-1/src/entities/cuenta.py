class Cuenta:
    def __init__(self, numero: str, titular: str, saldo: float = 0.0) -> None:
        self._numero = numero.strip()
        self._titular = titular.strip()
        self._saldo = saldo

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def titular(self) -> str:
        return self._titular

    @property
    def saldo(self) -> float:
        return self._saldo

    def _validar_monto_positivo(self, monto: float) -> bool:
        return monto > 0

    def depositar(self, monto: float) -> None:
        if not self._validar_monto_positivo(monto):
            print("El monto debe ser mayor a cero.")
            return
        self._saldo += monto
        print("Depósito realizado correctamente.")

    def retirar(self, monto: float) -> None:
        if not self._validar_monto_positivo(monto):
            print("El monto debe ser mayor a cero.")
            return
        if monto <= self._saldo:
            self._saldo -= monto
            print("Retiro realizado correctamente.")
        else:
            print("Fondos insuficientes.")

    def mostrar_saldo(self) -> str:
        return f"Cuenta {self._numero} - Titular: {self._titular} - Saldo: ${self._saldo:.2f}"
