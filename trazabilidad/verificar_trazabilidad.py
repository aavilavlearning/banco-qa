"""Verifica la matriz de trazabilidad de HU-01 contra la historia y el código de tests.

Uso:
    python trazabilidad/verificar_trazabilidad.py --modulo 2
    python trazabilidad/verificar_trazabilidad.py --matriz soluciones/modulo-8/matriz.csv --modulo 8

Qué revisa según el módulo alcanzado (cada módulo exige sus columnas y las anteriores):
    1 · Cada regla R-01..R-08 de la historia tiene al menos un caso; casos con descripción y esperado.
    2 · Prompt: qué versión del prompt refactorizado produjo cada caso (P-01 v1, v2, v3...).
    3 · Riesgo.
    4 · Tests y Suite: cada caso tiene tests, cada test listado existe y lleva @pytest.mark.caso
        con ese ID, y no hay tests marcados con casos que no estén en la matriz.
    5 · Herramienta_MCP      6 · Agente      7 · Control      8 · Eval
Sale con código 1 si encuentra brechas: sirve como evaluador determinista (M7) y guardrail (M8).
"""
from __future__ import annotations

import argparse
import ast
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
HISTORIA = RAIZ / "docs" / "HU-01-transferencia-terceros.md"
COLUMNAS_POR_MODULO = {
    1: ["Caso", "Regla", "Descripcion", "Esperado", "Prioridad"],
    2: ["Prompt"],
    3: ["Riesgo"],
    4: ["Tests", "Suite"],
    5: ["Herramienta_MCP"],
    6: ["Agente"],
    7: ["Control"],
    8: ["Eval"],
}


def reglas_de_la_historia() -> list[str]:
    return sorted(set(re.findall(r"^\| (R-\d\d) \|", HISTORIA.read_text(encoding="utf-8"), re.M)))


def tests_marcados() -> dict[str, set[str]]:
    """Devuelve {CP-xx: {ruta::nombre_test}} leyendo los @pytest.mark.caso del código."""
    por_caso: dict[str, set[str]] = defaultdict(set)
    for archivo in (RAIZ / "tests").rglob("test_*.py"):
        arbol = ast.parse(archivo.read_text(encoding="utf-8"))
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.FunctionDef) and nodo.name.startswith("test_"):
                for deco in nodo.decorator_list:
                    if (
                        isinstance(deco, ast.Call)
                        and getattr(deco.func, "attr", "") == "caso"
                        and deco.args
                        and isinstance(deco.args[0], ast.Constant)
                    ):
                        ruta = archivo.relative_to(RAIZ).as_posix()
                        por_caso[deco.args[0].value].add(f"{ruta}::{nodo.name}")
    return por_caso


def verificar(matriz: Path, modulo: int) -> list[str]:
    errores: list[str] = []
    filas = list(csv.DictReader(matriz.open(encoding="utf-8")))
    exigidas = [c for m in range(1, modulo + 1) for c in COLUMNAS_POR_MODULO[m]]

    faltan_columnas = [c for c in exigidas if filas and c not in filas[0]]
    if not filas:
        return ["La matriz está vacía"]
    if faltan_columnas:
        return [f"Faltan columnas en la matriz: {', '.join(faltan_columnas)}"]

    casos = [f for f in filas if f.get("Caso")]
    for regla in reglas_de_la_historia():
        if not any(f["Regla"] == regla for f in casos):
            errores.append(f"{regla} no tiene ningún caso")

    for fila in casos:
        for columna in exigidas:
            if not (fila.get(columna) or "").strip():
                errores.append(f"{fila['Caso']}: columna {columna} vacía")

    if modulo >= 4:
        marcados = tests_marcados()
        ids_matriz = {f["Caso"] for f in casos}
        for fila in casos:
            listados = {t.strip() for t in (fila.get("Tests") or "").split(";") if t.strip()}
            for test in listados - marcados.get(fila["Caso"], set()):
                errores.append(f"{fila['Caso']}: el test {test} no existe o no tiene @pytest.mark.caso('{fila['Caso']}')")
        for caso in sorted(set(marcados) - ids_matriz):
            errores.append(f"{caso} tiene tests en el código pero no está en la matriz")
    return errores


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--matriz", default=str(RAIZ / "trazabilidad" / "matriz.csv"))
    parser.add_argument("--modulo", type=int, default=2, choices=range(1, 9))
    args = parser.parse_args()

    errores = verificar(Path(args.matriz), args.modulo)
    if errores:
        print(f"Trazabilidad INCOMPLETA hasta el módulo {args.modulo} ({len(errores)} brechas):")
        for e in errores:
            print(f"  - {e}")
        return 1
    print(f"Trazabilidad completa hasta el módulo {args.modulo}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
