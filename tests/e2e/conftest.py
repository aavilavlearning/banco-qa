"""Levanta BancoQA en un puerto local para los tests E2E (o usa BANCOQA_URL si existe)."""
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

RAIZ = Path(__file__).resolve().parents[2]


def puerto_libre() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def servidor():
    if os.getenv("BANCOQA_URL"):
        yield os.environ["BANCOQA_URL"].rstrip("/")
        return
    puerto = puerto_libre()
    proceso = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", str(puerto), "--log-level", "warning"],
        cwd=RAIZ,
    )
    base = f"http://127.0.0.1:{puerto}"
    for _ in range(50):
        try:
            requests.get(base + "/docs", timeout=1)
            break
        except requests.ConnectionError:
            time.sleep(0.2)
    yield base
    proceso.terminate()
    proceso.wait()


@pytest.fixture(autouse=True)
def datos_limpios(servidor):
    requests.post(servidor + "/api/test/reset", timeout=5)
