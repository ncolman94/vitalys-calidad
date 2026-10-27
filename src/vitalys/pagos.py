"""Cobro de turnos a través de una pasarela de pagos externa."""

from typing import Protocol


class PasarelaPagos(Protocol):
    """Contrato de la API externa de pagos (proveedor)."""

    def consultar_estado_tarjeta(self, token_tarjeta: str) -> str:
        """Devuelve ACTIVA, VENCIDA o BLOQUEADA."""

    def cobrar(self, token_tarjeta: str, monto: float, referencia: str) -> dict:
        """Devuelve {'estado': 'APROBADO'|'RECHAZADO', 'id_transaccion': str}."""


class Notificador(Protocol):
    """Servicio que envía el comprobante al paciente."""

    def enviar_comprobante(self, turno_id: int, id_transaccion: str) -> None:
        """Envía el comprobante de pago."""


class PagoRechazadoError(Exception):
    """El cobro no pudo realizarse."""


class ServicioCobro:
    """Orquesta el cobro de un turno contra la pasarela externa."""

    def __init__(self, pasarela: PasarelaPagos, notificador: Notificador) -> None:
        self._pasarela = pasarela
        self._notificador = notificador

    def cobrar_turno(self, turno_id: int, token_tarjeta: str, monto: float) -> str:
        """Cobra el turno y devuelve el id de transacción."""
        if monto <= 0:
            raise ValueError("El monto a cobrar debe ser mayor a cero")

        estado = self._pasarela.consultar_estado_tarjeta(token_tarjeta)
        if estado != "ACTIVA":
            raise PagoRechazadoError(f"Tarjeta no habilitada: {estado}")

        resultado = self._pasarela.cobrar(token_tarjeta, monto, referencia=f"TURNO-{turno_id}")
        if resultado["estado"] != "APROBADO":
            raise PagoRechazadoError("La pasarela rechazó el cobro")

        self._notificador.enviar_comprobante(turno_id, resultado["id_transaccion"])
        return resultado["id_transaccion"]
