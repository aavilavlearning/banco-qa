"""Reproduce, sin modelo, las llamadas a herramientas del log de ejemplo (Módulo 6).

Sirve para que el instructor muestre las salidas reales de cada iteración.
Uso: BANCOQA_DEFECTOS=D1 python agentes/ejemplo/reproducir_ejemplo.py
"""
import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from herramientas import qa_tools  # noqa: E402

os.environ.setdefault("BANCOQA_ACTOR", "AG-EJ")


def paso(numero: int, descripcion: str, resultado) -> None:
    print(f"\n--- Iteración {numero}: {descripcion}")
    print(json.dumps(resultado, indent=2, ensure_ascii=False) if not isinstance(resultado, str) else resultado)


historia = (RAIZ / "docs" / "HU-01-transferencia-terceros.md").read_text(encoding="utf-8")
paso(1, "leer la historia (regla R-04)", next(linea for linea in historia.splitlines() if "| R-04 |" in linea))
paso(2, "casos diseñados (aprobados en HITL-02)", ["CP-06", "CP-07", "CP-08"])
resultado = qa_tools.ejecutar_suite("regresion", "dev", ["CP-06", "CP-07", "CP-08"])
paso(5, "ejecutar los casos de R-04", resultado)

defectos = [f for f in resultado["fallidos"] if f["caso"] == "CP-07"]
if defectos:
    borrador = qa_tools.crear_borrador_defecto(
        titulo="Se aprueba una transferencia que supera el límite diario acumulado en soles",
        caso="CP-07",
        regla="R-04",
        pasos=[
            "Transferir S/ 6,000.00 de 191-0000001 a 191-0000003 (aprobada).",
            "Transferir S/ 4,000.01 de 191-0000001 a 191-0000003 el mismo día.",
        ],
        esperado="Rechazada R-04: La operación supera tu límite diario",
        obtenido="Aprobada (HTTP 201)",
        evidencia=f"{defectos[0]['test']}: {defectos[0]['error']} · reporte {resultado['reporte']}",
        severidad="Alta",
    )
    paso(6, "reportar el posible defecto (sin tocar el test)", borrador)
else:
    print("\nNo hubo fallo en CP-07: ¿activaste BANCOQA_DEFECTOS=D1?")
