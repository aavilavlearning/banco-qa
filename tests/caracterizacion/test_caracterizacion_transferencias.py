"""Prueba de caracterización (golden master) del servicio de transferencias.

Captura cómo responde HOY el servicio ante 6 entradas representativas. No dice si está bien:
dice si cambió. Se usa antes de refactorizar o migrar (por ejemplo, de mainframe a la nube).

- Primera vez o después de un cambio aprobado:  ACTUALIZAR_GOLDEN=1 pytest tests/caracterizacion
- Siempre lo demás:                             pytest tests/caracterizacion
"""
import json
import os
from pathlib import Path

GOLDEN = Path(__file__).with_name("golden_transferencias.json")
CAMPOS_VARIABLES = {"fecha", "operacion"}  # cambian en cada ejecución: se excluyen

ENTRADAS = [
    {"nombre": "saldo justo", "cuenta_origen": "191-0000003", "cuenta_destino": "191-0000001", "monto": "500.00"},
    {"nombre": "saldo insuficiente", "cuenta_origen": "191-0000003", "cuenta_destino": "191-0000001", "monto": "500.01"},
    {"nombre": "destino bloqueado", "cuenta_origen": "191-0000001", "cuenta_destino": "191-0000004", "monto": "10.00"},
    {"nombre": "dolares", "cuenta_origen": "191-0000002", "cuenta_destino": "191-0000005", "monto": "250.00"},
    {"nombre": "sobre limite diario", "cuenta_origen": "191-0000001", "cuenta_destino": "191-0000003", "monto": "10000.01"},
    {"nombre": "tres decimales", "cuenta_origen": "191-0000001", "cuenta_destino": "191-0000003", "monto": "1.005"},
]


def capturar(api) -> dict:
    resultado = {}
    for entrada in ENTRADAS:
        api.post("/api/test/reset")
        cuerpo = {k: v for k, v in entrada.items() if k != "nombre"}
        respuesta = api.post("/api/transferencias", json=cuerpo)
        datos = {k: v for k, v in respuesta.json().items() if k not in CAMPOS_VARIABLES}
        resultado[entrada["nombre"]] = {"status": respuesta.status_code, "respuesta": datos}
    return resultado


def test_el_comportamiento_del_servicio_no_cambio(api):
    actual = capturar(api)
    if os.getenv("ACTUALIZAR_GOLDEN") == "1" or not GOLDEN.exists():
        GOLDEN.write_text(json.dumps(actual, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    esperado = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert actual == esperado
