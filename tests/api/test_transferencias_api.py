"""Tests de comportamiento de HU-01 a nivel de API.

Verifican lo que ve el cliente del servicio: código HTTP, regla informada, saldos y movimientos.
Funcionan en dev (app en memoria) o contra un servidor con BANCOQA_URL.
"""
import pytest

ANA_PEN, ANA_USD, BRUNO_PEN, CARLA_BLOQ, DIEGO_USD, ELENA_OTRO_BANCO = (
    "191-0000001", "191-0000002", "191-0000003", "191-0000004", "191-0000005", "999-0000006",
)


def transferir(api, origen, destino, monto):
    return api.post("/api/transferencias", json={"cuenta_origen": origen, "cuenta_destino": destino, "monto": monto})


def saldo(api, cuenta):
    return api.get(f"/api/cuentas/{cuenta}").json()["saldo"]


def movimientos(api, cuenta):
    return api.get(f"/api/cuentas/{cuenta}/movimientos").json()


def assert_rechazada_sin_mover_dinero(api, respuesta, regla, origen, destino, saldo_origen, saldo_destino):
    assert respuesta.status_code == 422
    assert respuesta.json()["regla"] == regla
    assert saldo(api, origen) == saldo_origen
    assert saldo(api, destino) == saldo_destino
    assert movimientos(api, origen) == []


@pytest.mark.caso("CP-01")
def test_transferencia_valida_debita_abona_y_registra_movimientos(api):
    respuesta = transferir(api, ANA_PEN, BRUNO_PEN, "1.00")

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "APROBADA"
    assert cuerpo["operacion"].startswith("OP-")
    assert saldo(api, ANA_PEN) == "14999.00"
    assert saldo(api, BRUNO_PEN) == "501.00"
    assert [m["tipo"] for m in movimientos(api, ANA_PEN)] == ["CARGO"]
    assert [m["tipo"] for m in movimientos(api, BRUNO_PEN)] == ["ABONO"]


@pytest.mark.caso("CP-05")
def test_saldo_insuficiente_se_rechaza_sin_mover_dinero(api):
    respuesta = transferir(api, BRUNO_PEN, ANA_PEN, "500.01")
    assert_rechazada_sin_mover_dinero(api, respuesta, "R-03", BRUNO_PEN, ANA_PEN, "500.00", "15000.00")


@pytest.mark.caso("CP-06")
def test_acumulado_exacto_al_limite_diario_se_aprueba(api):
    assert transferir(api, ANA_PEN, BRUNO_PEN, "6000.00").status_code == 201
    assert transferir(api, ANA_PEN, BRUNO_PEN, "4000.00").status_code == 201


@pytest.mark.caso("CP-07")
def test_acumulado_sobre_el_limite_diario_se_rechaza(api):
    assert transferir(api, ANA_PEN, BRUNO_PEN, "6000.00").status_code == 201

    respuesta = transferir(api, ANA_PEN, BRUNO_PEN, "4000.01")

    assert respuesta.status_code == 422
    assert respuesta.json()["regla"] == "R-04"
    assert saldo(api, ANA_PEN) == "9000.00"


@pytest.mark.caso("CP-08")
def test_limite_diario_en_dolares(api):
    respuesta = transferir(api, ANA_USD, DIEGO_USD, "3000.01")
    assert_rechazada_sin_mover_dinero(api, respuesta, "R-04", ANA_USD, DIEGO_USD, "5000.00", "100.00")


@pytest.mark.caso("CP-09")
def test_cuenta_destino_bloqueada_se_rechaza(api):
    respuesta = transferir(api, ANA_PEN, CARLA_BLOQ, "100.00")
    assert_rechazada_sin_mover_dinero(api, respuesta, "R-05", ANA_PEN, CARLA_BLOQ, "15000.00", "0.00")


@pytest.mark.caso("CP-10")
def test_monedas_distintas_se_rechaza(api):
    respuesta = transferir(api, ANA_PEN, DIEGO_USD, "100.00")
    assert_rechazada_sin_mover_dinero(api, respuesta, "R-06", ANA_PEN, DIEGO_USD, "15000.00", "100.00")


@pytest.mark.caso("CP-11")
def test_cuenta_destino_inexistente_se_rechaza(api):
    respuesta = transferir(api, ANA_PEN, "191-9999999", "100.00")
    assert respuesta.status_code == 422
    assert respuesta.json()["regla"] == "R-07"
    assert saldo(api, ANA_PEN) == "15000.00"


@pytest.mark.caso("CP-14")
def test_interbancaria_a_las_20_00_se_rechaza(api, fijar_reloj):
    fijar_reloj("2026-11-03T20:00:00")
    respuesta = transferir(api, ANA_PEN, ELENA_OTRO_BANCO, "100.00")
    assert_rechazada_sin_mover_dinero(api, respuesta, "R-08", ANA_PEN, ELENA_OTRO_BANCO, "15000.00", "0.00")


@pytest.mark.caso("CP-13")
def test_interbancaria_a_las_19_59_se_aprueba(api, fijar_reloj):
    fijar_reloj("2026-11-03T19:59:00")
    assert transferir(api, ANA_PEN, ELENA_OTRO_BANCO, "100.00").status_code == 201
