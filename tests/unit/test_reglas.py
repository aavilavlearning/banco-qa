"""Tests de comportamiento de las reglas de HU-01 (nivel unitario).

Cada test:
- se llama como la regla de negocio que demuestra,
- lleva el ID del caso de la matriz de trazabilidad (@pytest.mark.caso),
- verifica el resultado observable (aprobado o rechazado con su regla), no la implementación.
"""
from datetime import datetime
from decimal import Decimal

import pytest

from app.reglas import Cuenta, ReglaIncumplida, convertir_monto, validar_transferencia

MARTES_10AM = datetime(2026, 11, 3, 10, 0)

# Mensajes que ve el cliente, tal como están en docs/HU-01-transferencia-terceros.md
MENSAJES = {
    "R-01": "El monto mínimo es 1.00",
    "R-02": "El monto admite como máximo 2 decimales",
    "R-03": "Saldo insuficiente para realizar la operación",
    "R-04": "La operación supera tu límite diario",
    "R-05": "La cuenta origen o destino no está habilitada",
    "R-06": "Las cuentas deben tener la misma moneda",
    "R-07": "La cuenta destino no es válida para esta operación",
    "R-08": "Las transferencias interbancarias solo se procesan de lunes a viernes de 08:00 a 20:00",
}


def cuenta(numero="191-0000001", cliente="CLI-001", moneda="PEN", saldo="15000.00", bloqueada=False):
    return Cuenta(numero, "Titular ficticio", cliente, moneda, Decimal(saldo), bloqueada)


def destino_tercero(**kw):
    datos = dict(numero="191-0000003", cliente="CLI-002")
    datos.update(kw)
    return cuenta(**datos)


def rechazo(origen, destino, monto, acumulado="0", ahora=MARTES_10AM) -> str:
    """Devuelve la regla que rechazó la operación y verifica el mensaje que ve el cliente."""
    with pytest.raises(ReglaIncumplida) as error:
        validar_transferencia(origen, destino, Decimal(monto), Decimal(acumulado), ahora)
    assert error.value.mensaje == MENSAJES[error.value.regla]
    return error.value.regla


def aprueba(origen, destino, monto, acumulado="0", ahora=MARTES_10AM) -> None:
    validar_transferencia(origen, destino, Decimal(monto), Decimal(acumulado), ahora)


# R-01 · monto mínimo -------------------------------------------------------------------
@pytest.mark.caso("CP-01")
def test_aprueba_el_monto_minimo_de_1_00():
    aprueba(cuenta(), destino_tercero(), "1.00")


@pytest.mark.caso("CP-02")
def test_rechaza_montos_menores_a_1_00():
    assert rechazo(cuenta(), destino_tercero(), "0.99") == "R-01"


# R-02 · decimales --------------------------------------------------------------------------
@pytest.mark.caso("CP-03")
def test_rechaza_montos_con_mas_de_2_decimales():
    assert rechazo(cuenta(), destino_tercero(), "10.123") == "R-02"


# R-03 · saldo ------------------------------------------------------------------------------
@pytest.mark.caso("CP-04")
def test_aprueba_transferir_exactamente_el_saldo_disponible():
    aprueba(cuenta(saldo="500.00"), destino_tercero(), "500.00")


@pytest.mark.caso("CP-05")
def test_rechaza_transferir_mas_que_el_saldo_disponible():
    assert rechazo(cuenta(saldo="500.00"), destino_tercero(), "500.01") == "R-03"


# R-04 · límite diario ----------------------------------------------------------------------
@pytest.mark.caso("CP-06")
def test_aprueba_si_el_acumulado_del_dia_llega_exacto_al_limite_en_soles():
    aprueba(cuenta(), destino_tercero(), "4000.00", acumulado="6000.00")


@pytest.mark.caso("CP-07")
def test_rechaza_si_el_acumulado_del_dia_supera_el_limite_en_soles():
    assert rechazo(cuenta(), destino_tercero(), "4000.01", acumulado="6000.00") == "R-04"


@pytest.mark.caso("CP-08")
def test_rechaza_si_supera_el_limite_diario_en_dolares():
    origen = cuenta(numero="191-0000002", moneda="USD", saldo="5000.00")
    destino = destino_tercero(numero="191-0000005", cliente="CLI-004", moneda="USD")
    assert rechazo(origen, destino, "3000.01") == "R-04"


# R-05 · cuentas activas --------------------------------------------------------------------
@pytest.mark.caso("CP-09")
def test_rechaza_transferir_a_una_cuenta_bloqueada():
    assert rechazo(cuenta(), destino_tercero(bloqueada=True), "100.00") == "R-05"


# R-06 · misma moneda -----------------------------------------------------------------------
@pytest.mark.caso("CP-10")
def test_rechaza_transferir_entre_monedas_distintas():
    destino = destino_tercero(numero="191-0000005", cliente="CLI-004", moneda="USD")
    assert rechazo(cuenta(), destino, "100.00") == "R-06"


# R-07 · destino válido ---------------------------------------------------------------------
@pytest.mark.caso("CP-11")
def test_rechaza_una_cuenta_destino_inexistente():
    assert rechazo(cuenta(), None, "100.00") == "R-07"


@pytest.mark.caso("CP-12")
def test_rechaza_transferir_a_una_cuenta_del_mismo_titular():
    assert rechazo(cuenta(), cuenta(numero="191-0000002", moneda="USD"), "100.00") == "R-07"


# R-08 · horario de interbancarias ---------------------------------------------------------
INTERBANCARIA = dict(numero="999-0000006", cliente="EXT-001")


@pytest.mark.caso("CP-13")
def test_aprueba_interbancaria_a_las_19_59_de_un_dia_habil():
    aprueba(cuenta(), destino_tercero(**INTERBANCARIA), "100.00", ahora=datetime(2026, 11, 3, 19, 59))


@pytest.mark.caso("CP-14")
def test_rechaza_interbancaria_a_las_20_00():
    assert rechazo(cuenta(), destino_tercero(**INTERBANCARIA), "100.00", ahora=datetime(2026, 11, 3, 20, 0)) == "R-08"


@pytest.mark.caso("CP-15")
def test_rechaza_interbancaria_un_sabado():
    assert rechazo(cuenta(), destino_tercero(**INTERBANCARIA), "100.00", ahora=datetime(2026, 11, 7, 10, 0)) == "R-08"


# Casos que aparecieron al refactorizar el prompt (Módulo 2, versiones v2 y v3) --------------
@pytest.mark.caso("CP-16")
def test_aprueba_interbancaria_a_las_08_00_de_un_dia_habil():
    aprueba(cuenta(), destino_tercero(**INTERBANCARIA), "100.00", ahora=datetime(2026, 11, 3, 8, 0))


@pytest.mark.caso("CP-17")
def test_rechaza_interbancaria_a_las_07_59():
    assert rechazo(cuenta(), destino_tercero(**INTERBANCARIA), "100.00", ahora=datetime(2026, 11, 3, 7, 59)) == "R-08"


@pytest.mark.caso("CP-18")
def test_rechaza_transferir_desde_una_cuenta_bloqueada():
    assert rechazo(cuenta(bloqueada=True), destino_tercero(), "100.00") == "R-05"


@pytest.mark.caso("CP-19")
@pytest.mark.parametrize("valor", ["abc", "NaN", "Infinity"])
def test_rechaza_montos_que_no_son_numeros_validos(valor):
    with pytest.raises(ReglaIncumplida) as error:
        convertir_monto(valor)
    assert error.value.regla == "R-01"
    assert error.value.mensaje == MENSAJES["R-01"]


@pytest.mark.caso("CP-19")
def test_acepta_montos_numericos_en_texto():
    assert convertir_monto("150.50") == Decimal("150.50")
