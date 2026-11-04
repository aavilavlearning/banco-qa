"""Evaluador determinista de borradores de defecto (Módulo 7).

Califica de 1 a 5 cada criterio de la rúbrica. Aprueba si todos son >= 4.
Si no aprueba, devuelve feedback concreto para que el generador lo corrija.
La versión sin código es el subagente agentes/revisor-defectos.md.

Uso: python anexo-avanzado/control/evaluador.py salidas/defectos/borradores/DEF-001.md
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
HISTORIA = RAIZ / "docs" / "HU-01-transferencia-terceros.md"
MATRICES = [RAIZ / "trazabilidad" / "matriz.csv", RAIZ / "soluciones" / "modulo-2" / "matriz.csv"]
REGLAS_DINERO = {"R-01", "R-02", "R-03", "R-04", "R-05", "R-06", "R-07", "R-08"}


def _casos() -> dict[str, str]:
    for matriz in MATRICES:
        filas = [f for f in csv.DictReader(matriz.open(encoding="utf-8")) if f.get("Caso")]
        if filas:
            return {f["Caso"]: f["Regla"] for f in filas}
    return {}


def _mensajes() -> dict[str, str]:
    return dict(re.findall(r"^\| (R-\d\d) \| .*? \| (.*?) \|$", HISTORIA.read_text(encoding="utf-8"), re.M))


def evaluar(texto: str) -> dict:
    casos, mensajes = _casos(), _mensajes()
    puntajes, feedback = {}, []

    m = re.search(r"\*\*Trazabilidad:\*\* (HU-\d\d) · (R-\d\d) · (CP-\d\d)", texto)
    regla = m.group(2) if m else None
    if not m:
        puntajes["trazabilidad"] = 1
        feedback.append("Falta la línea de trazabilidad HU · R-xx · CP-xx")
    elif casos.get(m.group(3)) != regla:
        puntajes["trazabilidad"] = 2
        feedback.append(f"{m.group(3)} no corresponde a {regla} en la matriz")
    else:
        puntajes["trazabilidad"] = 5

    pasos = re.findall(r"^\d+\. .+", texto, re.M)
    con_datos = [p for p in pasos if re.search(r"\d{3}-\d{7}", p) and re.search(r"\d+\.\d{2}", p)]
    puntajes["reproducibilidad"] = 5 if pasos and len(con_datos) == len(pasos) else (3 if pasos else 1)
    if puntajes["reproducibilidad"] < 4:
        feedback.append("Cada paso debe incluir cuentas y montos concretos")

    esperado = re.search(r"\*\*Esperado:\*\* (.+)", texto)
    if regla and esperado and mensajes.get(regla, "@@") in esperado.group(1):
        puntajes["esperado"] = 5
    else:
        puntajes["esperado"] = 2
        feedback.append("El esperado debe citar el mensaje exacto de la regla según la historia")

    evidencia = texto.split("## Evidencia", 1)[-1] if "## Evidencia" in texto else ""
    tiene_reporte = "reports/" in evidencia
    tiene_reproduccion = "HTTP" in evidencia and "Request" in evidencia
    puntajes["evidencia"] = 5 if (tiene_reporte and tiene_reproduccion) else (3 if tiene_reporte else 1)
    if not tiene_reproduccion:
        feedback.append("La evidencia no incluye la reproducción HTTP (request y response de cada paso)")

    severidad = re.search(r"\*\*Severidad propuesta:\*\* (\w+)", texto)
    if regla in REGLAS_DINERO and severidad and severidad.group(1) not in ("Alta", "Crítica"):
        puntajes["severidad"] = 2
        feedback.append("Un defecto que mueve dinero debe ser de severidad Alta o Crítica")
    else:
        puntajes["severidad"] = 5 if severidad else 1

    return {"puntajes": puntajes, "aprobado": all(v >= 4 for v in puntajes.values()), "feedback": feedback}


if __name__ == "__main__":
    import json

    resultado = evaluar(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    sys.exit(0 if resultado["aprobado"] else 1)
