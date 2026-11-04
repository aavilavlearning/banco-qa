"""Valida una matriz de casos contra el estándar del equipo y la historia.

Uso: python .github/skills/disenar-casos-de-prueba/scripts/validar_casos.py <casos.csv> [historia.md]
Sale con código 1 si encuentra problemas. Es la parte determinista de la skill:
no depende del modelo.
"""
import csv
import re
import sys
from pathlib import Path

COLUMNAS = ["Caso", "CA", "Regla", "Descripcion", "Datos", "Esperado", "Prioridad"]
HISTORIA_POR_DEFECTO = Path(__file__).resolve().parents[4] / "docs" / "HU-01-transferencia-terceros.md"


def leer_historia(ruta: Path) -> tuple[dict[str, str], set[str]]:
    texto = ruta.read_text(encoding="utf-8")
    reglas = dict(re.findall(r"^\| (R-\d\d) \| .*? \| (.*?) \|$", texto, re.M))
    criterios = set(re.findall(r"\*\*(CA-\d\d)\*\*", texto))
    return reglas, criterios


def validar(casos: Path, historia: Path) -> list[str]:
    reglas, criterios = leer_historia(historia)
    filas = list(csv.DictReader(casos.open(encoding="utf-8")))
    if not filas:
        return ["El archivo no tiene casos"]
    faltan = [c for c in COLUMNAS if c not in filas[0]]
    if faltan:
        return [f"Faltan columnas: {', '.join(faltan)}"]

    errores, vistos = [], set()
    for f in filas:
        caso = f["Caso"]
        if not re.fullmatch(r"CP-\d\d", caso):
            errores.append(f"{caso}: el ID debe ser CP- y dos dígitos")
        if caso in vistos:
            errores.append(f"{caso}: ID duplicado")
        vistos.add(caso)
        if f["Regla"] not in reglas:
            errores.append(f"{caso}: la regla {f['Regla']} no existe en la historia")
        if f["CA"] not in criterios:
            errores.append(f"{caso}: el criterio {f['CA']} no existe en la historia")
        esperado = f["Esperado"].strip()
        if esperado != "Aprobada":
            m = re.fullmatch(r"Rechazada (R-\d\d): (.+)", esperado)
            if not m:
                errores.append(f"{caso}: el esperado debe ser 'Aprobada' o 'Rechazada R-xx: <mensaje>'")
            elif reglas.get(m.group(1)) != m.group(2):
                errores.append(f"{caso}: el mensaje no coincide con el de {m.group(1)} en la historia")
        if f["Prioridad"] not in {"Alta", "Media", "Baja"}:
            errores.append(f"{caso}: prioridad inválida")
        if not f["Descripcion"].strip() or not f["Datos"].strip():
            errores.append(f"{caso}: descripción o datos vacíos")

    for regla in sorted(set(reglas) - {f["Regla"] for f in filas}):
        errores.append(f"{regla} no tiene ningún caso")
    if len(filas) > 20:
        errores.append(f"Hay {len(filas)} casos; el máximo es 20")
    return errores


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    historia = Path(sys.argv[2]) if len(sys.argv) > 2 else HISTORIA_POR_DEFECTO
    errores = validar(Path(sys.argv[1]), historia)
    if errores:
        print(f"{len(errores)} problemas:")
        print("\n".join(f"  - {e}" for e in errores))
        sys.exit(1)
    print("Matriz de casos válida.")
