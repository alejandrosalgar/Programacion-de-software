from .cuenta import Cuenta


class CuentaCorriente(Cuenta):
    def __init__(
        self,
        numero: str,
        titular: str,
        saldo: float = 0.0,
        sobregiro: float = 500.0,
    ) -> None:
        super().__init__(numero, titular, saldo)
        self._sobregiro = sobregiro

    @property
    def sobregiro(self) -> float:
        return self._sobregiro

    def retirar(self, monto: float) -> None:
        if not self._validar_monto_positivo(monto):
            print("El monto debe ser mayor a cero.")
            return
        if monto <= self._saldo + self._sobregiro:
            self._saldo -= monto
            print("Retiro realizado correctamente.")
        else:
            print("Límite de sobregiro excedido.")

    def mostrar_saldo(self) -> str:
        base = super().mostrar_saldo()
        return f"{base} (Corriente - Sobregiro: ${self._sobregiro:.2f})"
