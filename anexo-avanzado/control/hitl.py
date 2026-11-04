"""Punto de aprobación humana (HITL) con registro (Módulo 7).

Nunca aprueba solo: si nadie responde, la decisión queda "pendiente" y el flujo no avanza.
Cada decisión se guarda en salidas/registro-hitl.csv (quién, cuándo, qué, por qué).
"""
from __future__ import annotations

import csv
import getpass
import os
import sys
from datetime import datetime
from pathlib import Path

REGISTRO = Path(__file__).resolve().parents[2] / "salidas" / "registro-hitl.csv"
OPCIONES = {"a": "aprobado", "r": "rechazado", "e": "editar"}


def solicitar(punto: str, item: str, resumen: str, decision: str | None = None) -> dict:
    """Muestra la evidencia y pide la decisión del QE.

    decision: solo para demos grabadas o pruebas automatizadas (aprobado, rechazado, editar).
    """
    print(f"\n=== {punto} · {item} ===\n{resumen}")
    comentario = ""
    if decision is None and sys.stdin.isatty():
        respuesta = ""
        while respuesta not in OPCIONES:
            respuesta = input("¿[a]probar, [r]echazar con feedback o [e]ditar? ").strip().lower()
        decision = OPCIONES[respuesta]
        if decision != "aprobado":
            comentario = input("Feedback para el generador: ").strip()
    elif decision is None:
        decision = "pendiente"
        comentario = "Sin respuesta del QE: el flujo se detiene"

    registro = {
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "punto": punto,
        "item": item,
        "decision": decision,
        "comentario": comentario,
        "quien": os.getenv("BANCOQA_QE", getpass.getuser()),
    }
    REGISTRO.parent.mkdir(exist_ok=True)
    nuevo = not REGISTRO.exists()
    with REGISTRO.open("a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=list(registro))
        if nuevo:
            escritor.writeheader()
        escritor.writerow(registro)
    print(f"Decisión registrada: {decision}")
    return registro
