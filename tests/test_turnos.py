"""Pruebas de la agenda refactorizada (red de seguridad del refactor del TP3)."""

import json

import pytest

from vitalys.turnos import AgendaTurnos, TurnoInvalidoError, calcular_precio


@pytest.fixture
def agenda():
    return AgendaTurnos()


@pytest.mark.parametrize(
    ("especialidad", "plan", "urgente", "esperado"),
    [
        ("clinica", "basico", False, 10000.00),
        ("clinica", "premium", True, 4800.00),
        ("pediatria", "plus", False, 8400.00),
        ("cardiologia", "basico", True, 18000.00),
    ],
)
def test_tu01_precio_equivalente_al_modulo_legacy(especialidad, plan, urgente, esperado):
    # Act
    precio = calcular_precio(especialidad, plan, urgente)

    # Assert
    assert precio == esperado


def test_tu02_registrar_turno_valido_asigna_id_incremental(agenda):
    # Act
    primero = agenda.registrar("Ana", "clinica", 1, 9, "basico", False)
    segundo = agenda.registrar("Luis", "pediatria", 2, 10, "plus", False)

    # Assert
    assert (primero.id, segundo.id) == (1, 2)
    assert segundo.precio == 8400.00


@pytest.mark.parametrize(
    ("paciente", "especialidad", "dia", "hora", "plan", "mensaje"),
    [
        ("", "clinica", 1, 9, "basico", "obligatorio"),
        ("Ana", "odontologia", 1, 9, "basico", "inexistente"),
        ("Ana", "cardiologia", 4, 9, "basico", "día 4"),
        ("Ana", "pediatria", 1, 18, "basico", "18 h"),
        ("Ana", "clinica", 1, 9, "oro", "Plan desconocido"),
    ],
)
def test_tu03_datos_invalidos_lanzan_excepcion_controlada(
    agenda, paciente, especialidad, dia, hora, plan, mensaje
):
    # Act / Assert
    with pytest.raises(TurnoInvalidoError, match=mensaje):
        agenda.registrar(paciente, especialidad, dia, hora, plan, False)


def test_tu04_recalcular_precio_de_turno_existente(agenda):
    # Arrange
    turno = agenda.registrar("Ana", "clinica", 1, 9, "basico", False)

    # Act
    nuevo = agenda.recalcular_precio(turno.id, "premium", False)

    # Assert
    assert nuevo == 4000.00


def test_tu05_recalcular_turno_inexistente_lanza_error(agenda):
    with pytest.raises(TurnoInvalidoError, match="inexistente"):
        agenda.recalcular_precio(99, "basico", False)


def test_tu06_exportar_genera_json_con_los_turnos(agenda, tmp_path):
    # Arrange
    agenda.registrar("Ana", "clinica", 1, 9, "basico", False)
    destino = tmp_path / "agenda.json"

    # Act
    agenda.exportar(destino)

    # Assert
    datos = json.loads(destino.read_text(encoding="utf-8"))
    assert [t["paciente"] for t in datos] == ["Ana"]
