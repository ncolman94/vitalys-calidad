"""Pruebas unitarias de calcular_copago (patrón AAA + cobertura de ramas).

Decisiones del código bajo prueba:
  D1: monto <= 0
  D2: plan not in DESCUENTO_PLAN
  D3: es_urgencia and plan != "premium"
  D4: edad < 18 or edad >= 65
"""

import pytest

from vitalys.copago import calcular_copago


def test_cp01_monto_cero_lanza_error():  # D1 = V
    # Arrange
    monto_invalido = 0

    # Act / Assert (la excepción es el resultado esperado)
    with pytest.raises(ValueError, match="mayor a cero"):
        calcular_copago(monto_invalido, "basico", 30, False)


def test_cp02_plan_inexistente_lanza_error():  # D1 = F, D2 = V
    # Arrange
    plan_invalido = "oro"

    # Act / Assert
    with pytest.raises(ValueError, match="Plan desconocido"):
        calcular_copago(10000, plan_invalido, 30, False)


def test_cp03_urgencia_plan_basico_adulto_aplica_recargo():  # D3 = V, D4 = F
    # Arrange
    monto, plan, edad, urgencia = 10000, "basico", 30, True

    # Act
    copago = calcular_copago(monto, plan, edad, urgencia)

    # Assert
    assert copago == 12000.00


def test_cp04_sin_urgencia_plan_plus_adulto_solo_descuento_plan():  # D3 = F (1ra cond.), D4 = F
    # Arrange
    monto, plan, edad, urgencia = 10000, "plus", 30, False

    # Act
    copago = calcular_copago(monto, plan, edad, urgencia)

    # Assert
    assert copago == 7000.00


def test_cp05_urgencia_plan_premium_no_aplica_recargo():  # D3 = F (2da cond.)
    # Arrange
    monto, plan, edad, urgencia = 10000, "premium", 40, True

    # Act
    copago = calcular_copago(monto, plan, edad, urgencia)

    # Assert
    assert copago == 4000.00


def test_cp06_menor_de_edad_paga_la_mitad():  # D4 = V (1ra cond.)
    # Arrange
    monto, plan, edad, urgencia = 10000, "basico", 10, False

    # Act
    copago = calcular_copago(monto, plan, edad, urgencia)

    # Assert
    assert copago == 5000.00


def test_cp07_mayor_de_65_con_urgencia_combina_recargo_y_descuento():  # D3 = V, D4 = V (2da)
    # Arrange
    monto, plan, edad, urgencia = 10000, "plus", 70, True

    # Act
    copago = calcular_copago(monto, plan, edad, urgencia)

    # Assert
    assert copago == 4200.00


@pytest.mark.parametrize(
    ("edad", "esperado"),
    [(17, 5000.00), (18, 10000.00), (64, 10000.00), (65, 5000.00)],
    ids=["cp08_17_anios", "cp08_18_anios", "cp08_64_anios", "cp08_65_anios"],
)
def test_cp08_valores_limite_de_edad(edad, esperado):  # casos de borde de D4
    # Arrange
    monto, plan, urgencia = 10000, "basico", False

    # Act
    copago = calcular_copago(monto, plan, edad, urgencia)

    # Assert
    assert copago == esperado
