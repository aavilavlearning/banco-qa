"""Guardrails del pipeline (Módulo 8): bloquean cambios peligrosos aunque el agente "obedezca" o no.

Compara el estado actual contra una rama base y falla (código 1) si:
- se eliminaron tests o bajó el número de aserciones de un archivo de tests;
- se agregaron skip o xfail;
- aparecen datos que parecen reales (tarjetas de 16 dígitos, DNI) o URLs fuera de dev/qa;
- una rama agente/* modificó archivos fuera de sus rutas permitidas;
- la trazabilidad quedó incompleta.

Uso:
    python anexo-avanzado/harness/verificar_guardrails.py --base origin/main
    python anexo-avanzado/harness/verificar_guardrails.py --base HEAD~1 --sin-trazabilidad
"""
from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from trazabilidad.verificar_trazabilidad import verificar  # noqa: E402

POLITICA = yaml.safe_load((RAIZ / "harness" / "politica-agente.yaml").read_text(encoding="utf-8"))
PATRONES_PROHIBIDOS = {
    "skip o xfail agregado": re.compile(r"pytest\.mark\.(skip|xfail)|pytest\.skip\(|\.skip\(|test\.fixme"),
    "posible número de tarjeta real": re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b"),
    "posible DNI real": re.compile(r"DNI\D{0,3}\d{8}\b", re.I),
    "URL fuera de dev/qa": re.compile(r"https?://(?!localhost|127\.0\.0\.1|dev\.|qa\.)[\w.-]+"),
}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, check=True).stdout


def contar(codigo: str) -> tuple[int, int]:
    """Devuelve (tests, aserciones) de un archivo Python de tests."""
    arbol = ast.parse(codigo)
    tests = sum(isinstance(n, ast.FunctionDef) and n.name.startswith("test_") for n in ast.walk(arbol))
    aserciones = sum(isinstance(n, ast.Assert) for n in ast.walk(arbol))
    aserciones += sum(
        isinstance(n, ast.Call) and getattr(n.func, "id", getattr(n.func, "attr", "")) in {"expect", "rechazo", "aprueba"}
        for n in ast.walk(arbol)
    )
    return tests, aserciones


def revisar(base: str, con_trazabilidad: bool, matriz: str, modulo: int) -> list[str]:
    errores: list[str] = []
    cambios = [linea.split("\t") for linea in git("diff", "--name-status", base).splitlines() if linea]

    rama = os.getenv("GITHUB_HEAD_REF") or git("rev-parse", "--abbrev-ref", "HEAD").strip()
    if rama.startswith("agente/"):
        permitidas = tuple(POLITICA["rutas_escritura"])
        for estado, ruta, *_ in cambios:
            if not ruta.startswith(permitidas):
                errores.append(f"La rama {rama} modificó {ruta}, fuera de {', '.join(permitidas)}")

    for estado, ruta, *_ in cambios:
        if not (ruta.startswith("tests/") and ruta.endswith(".py")):
            continue
        antes = git("show", f"{base}:{ruta}") if estado != "A" else ""
        if estado == "D":
            errores.append(f"Se eliminó el archivo de tests {ruta}")
            continue
        if antes:
            tests_antes, aserciones_antes = contar(antes)
            tests_ahora, aserciones_ahora = contar((RAIZ / ruta).read_text(encoding="utf-8"))
            if tests_ahora < tests_antes:
                errores.append(f"{ruta}: bajó de {tests_antes} a {tests_ahora} tests")
            if aserciones_ahora < aserciones_antes:
                errores.append(f"{ruta}: bajó de {aserciones_antes} a {aserciones_ahora} aserciones")

    agregadas = [l[1:] for l in git("diff", "-U0", base, "--", "tests", "app", "servidor_mcp", "herramientas").splitlines()
                 if l.startswith("+") and not l.startswith("+++")]
    for descripcion, patron in PATRONES_PROHIBIDOS.items():
        for linea in agregadas:
            if patron.search(linea):
                errores.append(f"{descripcion}: {linea.strip()[:100]}")

    if con_trazabilidad:
        errores += [f"Trazabilidad: {e}" for e in verificar(Path(matriz), modulo)]
    return errores


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--sin-trazabilidad", action="store_true")
    parser.add_argument("--matriz", default=str(RAIZ / "trazabilidad" / "matriz.csv"))
    parser.add_argument("--modulo", type=int, default=2)
    args = parser.parse_args()

    errores = revisar(args.base, not args.sin_trazabilidad, args.matriz, args.modulo)
    if errores:
        print(f"GUARDRAILS: cambio BLOQUEADO ({len(errores)} violaciones)")
        for e in errores:
            print(f"  - {e}")
        return 1
    print("GUARDRAILS: sin violaciones")
    return 0


if __name__ == "__main__":
    sys.exit(main())
