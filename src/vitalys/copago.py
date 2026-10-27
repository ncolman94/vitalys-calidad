"""Cálculo del copago que abona un paciente de Vitalys App por una consulta."""

DESCUENTO_PLAN = {"basico": 0.0, "plus": 0.30, "premium": 0.60}
RECARGO_URGENCIA = 0.20
DESCUENTO_EDAD = 0.50
EDAD_MAYORIA = 18
EDAD_JUBILATORIA = 65


def calcular_copago(monto: float, plan: str, edad: int, es_urgencia: bool) -> float:
    """Devuelve el importe a cobrar al paciente, redondeado a 2 decimales.

    Reglas de negocio:
    - El plan aplica un descuento sobre el monto de la consulta.
    - Las urgencias tienen recargo, salvo para el plan premium.
    - Menores de 18 y mayores de 65 abonan la mitad.
    """
    if monto <= 0:
        raise ValueError("El monto de la consulta debe ser mayor a cero")
    if plan not in DESCUENTO_PLAN:
        raise ValueError(f"Plan desconocido: {plan}")

    copago = monto * (1 - DESCUENTO_PLAN[plan])

    if es_urgencia and plan != "premium":
        copago *= 1 + RECARGO_URGENCIA

    if edad < EDAD_MAYORIA or edad >= EDAD_JUBILATORIA:
        copago *= 1 - DESCUENTO_EDAD

    return round(copago, 2)
