"""Router de fallos (Módulo 7).

Primero reglas deterministas; si ninguna decide, la categoría queda "desconocido" con confianza baja
y el fallo va al QE. La versión sin código es la skill .github/skills/clasificar-fallo.

Categorías: defecto, flaky, ambiente, test_roto, desconocido.
Regla de banca: un posible defecto en una regla que mueve dinero SIEMPRE pasa por HITL.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

UMBRAL_CONFIANZA = 0.70
REGLAS_DINERO = {"R-01", "R-02", "R-03", "R-04", "R-05", "R-06", "R-07", "R-08"}  # HU-01 completa mueve dinero


@dataclass
class Decision:
    fallo: str
    categoria: str
    confianza: float
    motivo: str
    requiere_hitl: bool
    accion: str


def clasificar(fallo: dict, regla: str | None = None) -> Decision:
    error = fallo.get("error", "")
    historial = fallo.get("historial", [])

    if re.search(r"ConnectTimeout|ConnectionError|Max retries|503|ECONNREFUSED", error):
        categoria, confianza, motivo = "ambiente", 0.92, "Error de conexión o disponibilidad del servicio"
    elif fallo.get("mismo_commit") and "pasó" in historial and "falló" in historial:
        categoria, confianza, motivo = "flaky", 0.55, "Pasa y falla sin cambios de código en el mismo commit"
    elif re.search(r"locator not found|waiting for get_by|strict mode violation", error):
        categoria, confianza, motivo = "test_roto", 0.88, "El test no encuentra un elemento de la interfaz"
    elif re.search(r"assert \d{3} == \d{3}|regla|saldo|Locator expected to have text", error):
        categoria, confianza, motivo = "defecto", 0.90, "El sistema responde distinto a lo que exige la regla"
    else:
        categoria, confianza, motivo = "desconocido", 0.30, "Ninguna regla determinista aplica"

    baja_confianza = confianza < UMBRAL_CONFIANZA
    toca_dinero = categoria == "defecto" and (regla in REGLAS_DINERO if regla else True)
    requiere_hitl = baja_confianza or toca_dinero

    acciones = {
        "ambiente": "Notificar a infraestructura; no crear defecto",
        "flaky": "Reintentar y registrar como flaky",
        "test_roto": "Asignar al agente de mantenimiento en su rama",
        "defecto": "Generar borrador -> evaluador -> HITL-03",
        "desconocido": "Escalar al QE",
    }
    accion = "Escalar al QE (confianza baja)" if baja_confianza else acciones[categoria]
    return Decision(fallo.get("id", fallo.get("test", "")), categoria, confianza, motivo, requiere_hitl, accion)
