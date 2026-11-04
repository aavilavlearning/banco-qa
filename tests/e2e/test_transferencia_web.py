"""Tests E2E de HU-01 en la web de BancoQA (Playwright).

Selectores por rol y etiqueta (lo que ve el usuario), esperas por estado, sin sleeps.
"""
import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def llenar_y_transferir(page: Page, servidor: str, origen: str, destino: str, monto: str):
    page.goto(f"{servidor}/transferir")
    page.get_by_label("Cuenta origen").fill(origen)
    page.get_by_label("Cuenta destino").fill(destino)
    page.get_by_label("Monto").fill(monto)
    page.get_by_role("button", name="Transferir").click()


@pytest.mark.caso("CP-01")
def test_el_cliente_ve_la_operacion_aprobada(page: Page, servidor):
    llenar_y_transferir(page, servidor, "191-0000001", "191-0000003", "1.00")
    expect(page.get_by_role("status")).to_contain_text("Transferencia aprobada. Operación OP-")


@pytest.mark.caso("CP-05")
def test_el_cliente_ve_el_mensaje_de_saldo_insuficiente(page: Page, servidor):
    llenar_y_transferir(page, servidor, "191-0000003", "191-0000001", "500.01")
    expect(page.get_by_role("alert")).to_have_text("Saldo insuficiente para realizar la operación")
    expect(page.get_by_role("status")).to_be_empty()
