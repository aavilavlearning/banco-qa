"""Ejecuta las evals de evals/tareas.yaml y muestra una tabla de resultados (Módulo 8).

Uso: python anexo-avanzado/evals/ejecutar_evals.py
Sale con código 1 si alguna eval falla.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "anexo-avanzado"))
from control import evaluador, router  # noqa: E402
from trazabilidad.verificar_trazabilidad import verificar  # noqa: E402

TAREAS = {t["id"]: t for t in yaml.safe_load((RAIZ / "anexo-avanzado" / "evals" / "tareas.yaml").read_text(encoding="utf-8"))}


def ev_01(t):
    fallos = json.loads((RAIZ / "control" / "muestras" / "fallos-nocturno.json").read_text(encoding="utf-8"))
    obtenido = {f["id"]: router.clasificar(f).categoria for f in fallos}
    return obtenido == t["esperado"], f"obtenido {obtenido}"


def ev_02(t):
    errores = verificar(RAIZ / t["matriz"], 8)
    return not errores, f"{len(errores)} brechas"


def _suite_con_defecto(t):
    codigo = (
        "import json,sys; sys.path.insert(0,'.'); from herramientas import qa_tools; "
        f"print(json.dumps(qa_tools.ejecutar_suite('regresion','dev',{t['casos']!r})))"
    )
    env = dict(os.environ, BANCOQA_DEFECTOS=t["defectos"], BANCOQA_ACTOR="evals")
    salida = subprocess.run([sys.executable, "-c", codigo], cwd=RAIZ, env=env, capture_output=True, text=True, timeout=600)
    resumen = json.loads(salida.stdout.strip().splitlines()[-1])
    detectados = {f["caso"] for f in resumen["fallidos"]}
    return set(t["casos"]) <= detectados, f"fallaron {resumen['fallaron']} de {resumen['total']}"


def ev_05(t):
    salida = subprocess.run(["bash", "anexo-avanzado/harness/demo_trampa.sh"], cwd=RAIZ, capture_output=True, text=True, timeout=300)
    bloqueado = "Código de salida del guardrail: 1" in salida.stdout
    return bloqueado, "PR bloqueado" if bloqueado else "la trampa pasó"


def ev_06(t):
    base = (
        "# DEF-900 · prueba\n\n**Estado:** BORRADOR\n**Trazabilidad:** HU-01 · R-04 · CP-07\n"
        "**Severidad propuesta:** Alta\n\n## Pasos para reproducir\n"
        "1. Transferir 6000.00 de 191-0000001 a 191-0000003\n2. Transferir 4000.01 de 191-0000001 a 191-0000003\n\n"
        "**Esperado:** Rechazada R-04: La operación supera tu límite diario\n\n**Obtenido:** HTTP 201\n\n"
        "## Evidencia\ntest: assert 201 == 422 · reporte reports/x.xml\n"
    )
    completo = base + "Request: POST /api/transferencias {...}\nResponse: HTTP 201 {...}\n"
    rechaza = not evaluador.evaluar(base)["aprobado"]
    aprueba = evaluador.evaluar(completo)["aprobado"]
    return rechaza and aprueba, f"rechaza incompleto={rechaza}, aprueba completo={aprueba}"


EJECUTORES = {"EV-01": ev_01, "EV-02": ev_02, "EV-03": _suite_con_defecto, "EV-04": _suite_con_defecto, "EV-05": ev_05, "EV-06": ev_06}


def main() -> int:
    fallidas = 0
    print(f"{'Eval':<6} {'Resultado':<10} Detalle")
    for id_, tarea in TAREAS.items():
        try:
            ok, detalle = EJECUTORES[id_](tarea)
        except Exception as error:  # una eval rota cuenta como fallida
            ok, detalle = False, f"error: {error}"
        fallidas += not ok
        print(f"{id_:<6} {'PASA' if ok else 'FALLA':<10} {tarea['nombre']} · {detalle}")
    print(f"\n{len(TAREAS) - fallidas} de {len(TAREAS)} evals pasan")
    return 1 if fallidas else 0


if __name__ == "__main__":
    sys.exit(main())
