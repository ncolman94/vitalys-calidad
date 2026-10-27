"""Pruebas de ServicioCobro aislado de la API externa de pagos.

- Stub: provee entradas indirectas (respuestas enlatadas) y se verifica ESTADO/RESULTADO.
- Mock: registra las llamadas y se verifica el PROTOCOLO DE INTERACCIÓN.
"""

from unittest.mock import Mock, call

import pytest

from vitalys.pagos import PagoRechazadoError, ServicioCobro


class StubPasarela:
    """Stub escrito a mano: siempre devuelve lo que se le configura. No registra nada."""

    def __init__(self, estado_tarjeta="ACTIVA", estado_cobro="APROBADO", id_tx="TX-001"):
        self._estado_tarjeta = estado_tarjeta
        self._respuesta = {"estado": estado_cobro, "id_transaccion": id_tx}

    def consultar_estado_tarjeta(self, token_tarjeta):
        return self._estado_tarjeta

    def cobrar(self, token_tarjeta, monto, referencia):
        return self._respuesta


class NotificadorNulo:
    """Dummy: cumple la interfaz y no hace nada."""

    def enviar_comprobante(self, turno_id, id_transaccion):
        return None


# ---------------------------------------------------------------- STUBS


def test_pg01_stub_cobro_aprobado_devuelve_id_transaccion():
    # Arrange
    servicio = ServicioCobro(StubPasarela(id_tx="TX-777"), NotificadorNulo())

    # Act
    id_tx = servicio.cobrar_turno(turno_id=7, token_tarjeta="tok_visa", monto=5000)

    # Assert
    assert id_tx == "TX-777"


@pytest.mark.parametrize("estado", ["VENCIDA", "BLOQUEADA"])
def test_pg02_stub_tarjeta_no_activa_rechaza_el_cobro(estado):
    # Arrange
    servicio = ServicioCobro(StubPasarela(estado_tarjeta=estado), NotificadorNulo())

    # Act / Assert
    with pytest.raises(PagoRechazadoError, match=estado):
        servicio.cobrar_turno(7, "tok_visa", 5000)


def test_pg03_stub_pasarela_rechaza_lanza_error_controlado():
    # Arrange
    servicio = ServicioCobro(StubPasarela(estado_cobro="RECHAZADO"), NotificadorNulo())

    # Act / Assert
    with pytest.raises(PagoRechazadoError, match="rechazó"):
        servicio.cobrar_turno(7, "tok_visa", 5000)


def test_pg04_monto_invalido_no_llega_a_la_pasarela():
    # Arrange
    pasarela = Mock()
    servicio = ServicioCobro(pasarela, NotificadorNulo())

    # Act / Assert
    with pytest.raises(ValueError):
        servicio.cobrar_turno(7, "tok_visa", -1)
    pasarela.assert_not_called()


# ---------------------------------------------------------------- MOCKS


def _mocks_aprobados():
    pasarela = Mock()
    pasarela.consultar_estado_tarjeta.return_value = "ACTIVA"
    pasarela.cobrar.return_value = {"estado": "APROBADO", "id_transaccion": "TX-900"}
    notificador = Mock()
    return pasarela, notificador


def test_pg05_mock_cobra_una_sola_vez_con_los_parametros_exactos():
    # Arrange
    pasarela, notificador = _mocks_aprobados()
    servicio = ServicioCobro(pasarela, notificador)

    # Act
    servicio.cobrar_turno(turno_id=42, token_tarjeta="tok_master", monto=8400.0)

    # Assert: se interroga al mock, no al resultado
    pasarela.cobrar.assert_called_once_with("tok_master", 8400.0, referencia="TURNO-42")


def test_pg06_mock_nunca_cobra_una_tarjeta_vencida():
    # Arrange
    pasarela = Mock()
    pasarela.consultar_estado_tarjeta.return_value = "VENCIDA"
    notificador = Mock()
    servicio = ServicioCobro(pasarela, notificador)

    # Act
    with pytest.raises(PagoRechazadoError):
        servicio.cobrar_turno(42, "tok_master", 8400.0)

    # Assert
    pasarela.cobrar.assert_not_called()
    notificador.enviar_comprobante.assert_not_called()


def test_pg07_mock_consulta_la_tarjeta_antes_de_cobrar_y_luego_notifica():
    # Arrange
    pasarela, notificador = _mocks_aprobados()
    orden = Mock()
    orden.attach_mock(pasarela, "pasarela")
    orden.attach_mock(notificador, "notificador")
    servicio = ServicioCobro(pasarela, notificador)

    # Act
    servicio.cobrar_turno(42, "tok_master", 8400.0)

    # Assert: orden exacto del protocolo
    assert orden.mock_calls == [
        call.pasarela.consultar_estado_tarjeta("tok_master"),
        call.pasarela.cobrar("tok_master", 8400.0, referencia="TURNO-42"),
        call.notificador.enviar_comprobante(42, "TX-900"),
    ]


def test_pg08_mock_cobro_rechazado_no_envia_comprobante():
    # Arrange
    pasarela, notificador = _mocks_aprobados()
    pasarela.cobrar.return_value = {"estado": "RECHAZADO", "id_transaccion": None}
    servicio = ServicioCobro(pasarela, notificador)

    # Act
    with pytest.raises(PagoRechazadoError):
        servicio.cobrar_turno(42, "tok_master", 8400.0)

    # Assert
    notificador.enviar_comprobante.assert_not_called()
