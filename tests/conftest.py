"""Fixtures compartidas.

- `api`: cliente HTTP de BancoQA con datos reiniciados.
    * Sin variables: usa la app en memoria (ambiente "dev").
    * Con BANCOQA_URL=http://host:puerto: prueba contra un servidor levantado (ambiente "qa").
- `fijar_reloj`: fija la fecha y hora del banco para probar horarios (R-08).
"""
from __future__ import annotations

import os

import pytest
import requests


class ClienteRemoto:
    def __init__(self, base: str):
        self.base = base.rstrip("/")

    def get(self, ruta, **kw):
        return requests.get(self.base + ruta, timeout=10, **kw)

    def post(self, ruta, **kw):
        return requests.post(self.base + ruta, timeout=10, **kw)


@pytest.fixture
def api():
    base = os.getenv("BANCOQA_URL")
    if base:
        cliente = ClienteRemoto(base)
        cliente.post("/api/test/reset")
        yield cliente
        cliente.post("/api/test/reloj", json={"fecha_hora": None})
        return

    from fastapi.testclient import TestClient

    from app.main import app, banco

    banco.reiniciar()
    with TestClient(app) as cliente:
        yield cliente
    banco.reiniciar()


@pytest.fixture
def fijar_reloj(api):
    def _fijar(fecha_hora: str):
        respuesta = api.post("/api/test/reloj", json={"fecha_hora": fecha_hora})
        assert respuesta.status_code == 200

    return _fijar
