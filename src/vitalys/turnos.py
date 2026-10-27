"""Agenda de turnos de Vitalys App (refactorización de src/legacy/turnos_legacy.py)."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from vitalys.copago import DESCUENTO_PLAN, RECARGO_URGENCIA


@dataclass(frozen=True)
class Especialidad:
    """Regla de atención de una especialidad."""

    precio_base: float
    dias: range
    horas: range


ESPECIALIDADES = {
    "clinica": Especialidad(10000, range(1, 6), range(8, 20)),
    "pediatria": Especialidad(12000, range(1, 6), range(9, 18)),
    "cardiologia": Especialidad(15000, range(1, 4), range(8, 14)),
}


@dataclass
class Turno:
    """Turno registrado en la agenda."""

    id: int
    paciente: str
    especialidad: str
    dia: int
    hora: int
    precio: float


class TurnoInvalidoError(ValueError):
    """Los datos del turno no cumplen las reglas de la agenda."""


def calcular_precio(especialidad: str, plan: str, urgente: bool) -> float:
    """Precio del turno según especialidad, plan y urgencia (única fuente de verdad)."""
    regla = _obtener_especialidad(especialidad)
    if plan not in DESCUENTO_PLAN:
        raise TurnoInvalidoError(f"Plan desconocido: {plan}")
    precio = regla.precio_base * (1 - DESCUENTO_PLAN[plan])
    if urgente:
        precio *= 1 + RECARGO_URGENCIA
    return round(precio, 2)


def _obtener_especialidad(nombre: str) -> Especialidad:
    try:
        return ESPECIALIDADES[nombre]
    except KeyError as error:
        raise TurnoInvalidoError(f"Especialidad inexistente: {nombre}") from error


class AgendaTurnos:
    """Registra turnos validando días y horarios de cada especialidad."""

    def __init__(self) -> None:
        self._turnos: dict[int, Turno] = {}
        self._ultimo_id = 0

    def registrar(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self, paciente: str, especialidad: str, dia: int, hora: int, plan: str, urgente: bool
    ) -> Turno:
        """Valida y registra un turno nuevo."""
        if not paciente:
            raise TurnoInvalidoError("El paciente es obligatorio")
        regla = _obtener_especialidad(especialidad)
        if dia not in regla.dias:
            raise TurnoInvalidoError(f"{especialidad} no atiende el día {dia}")
        if hora not in regla.horas:
            raise TurnoInvalidoError(f"{especialidad} no atiende a las {hora} h")

        self._ultimo_id += 1
        turno = Turno(
            id=self._ultimo_id,
            paciente=paciente,
            especialidad=especialidad,
            dia=dia,
            hora=hora,
            precio=calcular_precio(especialidad, plan, urgente),
        )
        self._turnos[turno.id] = turno
        return turno

    def recalcular_precio(self, id_turno: int, plan: str, urgente: bool) -> float:
        """Actualiza el precio de un turno existente."""
        turno = self._turnos.get(id_turno)
        if turno is None:
            raise TurnoInvalidoError(f"Turno inexistente: {id_turno}")
        turno.precio = calcular_precio(turno.especialidad, plan, urgente)
        return turno.precio

    def exportar(self, ruta: Path) -> None:
        """Guarda la agenda en JSON. Los errores de E/S se propagan al llamador."""
        datos = [asdict(turno) for turno in self._turnos.values()]
        ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
