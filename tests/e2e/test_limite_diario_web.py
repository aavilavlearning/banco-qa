"""Test generado a partir de la exploración con Playwright MCP (Módulo 5), revisado por el QE.

Recorrido explorado: dos transferencias seguidas que superan el límite diario en soles.
"""
import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def transferir(page: Page, servidor: str, monto: str):
    page.goto(f"{servidor}/transferir")
    page.get_by_label("Cuenta origen").fill("191-0000001")
    page.get_by_label("Cuenta destino").fill("191-0000003")
    page.get_by_label("Monto").fill(monto)
    page.get_by_role("button", name="Transferir").click()


@pytest.mark.caso("CP-07")
def test_el_cliente_ve_el_mensaje_de_limite_diario_al_superarlo_por_0_01(page: Page, servidor):
    transferir(page, servidor, "6000.00")
    expect(page.get_by_role("status")).to_contain_text("Transferencia aprobada")

    transferir(page, servidor, "4000.01")

    expect(page.get_by_role("alert")).to_have_text("La operación supera tu límite diario")
    expect(page.get_by_role("status")).to_be_empty()
