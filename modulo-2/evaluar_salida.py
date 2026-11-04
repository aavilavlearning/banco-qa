"""Mide la salida de una o varias versiones de un prompt de diseño de casos (Módulo 2).

Uso:
    python modulo-2/evaluar_salida.py salida-v1.csv salida-v2.csv salida-v3.csv

Cada archivo es la salida (CSV) de una versión del prompt sobre HU-01, con columnas
Caso,CA,Regla,Descripcion,Datos,Esperado,Prioridad. Las métricas son deterministas:
la misma salida da siempre el mismo puntaje, así se compara una versión con otra.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
HISTORIA = RAIZ / "docs" / "HU-01-transferencia-terceros.md"

# Valores límite que la historia exige probar (en ambos extremos)
LIMITES = {
    "monto 1.00": r"; 1\.00\b",
    "monto 0.99": r"; 0\.99\b",
    "3 decimales": r"; \d+\.\d{3}\b",
    "saldo exacto": r"; 500\.00\b",
    "saldo + 0.01": r"; 500\.01\b",
    "acumulado exacto": r"\+ 4000\.00",
    "acumulado + 0.01": r"\+ 4000\.01",
    "límite en dólares": r"3000\.01",
    "interbancaria 19:59": r"19:59",
    "interbancaria 20:00": r"20:00",
    "interbancaria 07:59": r"07:59",
    "interbancaria 08:00": r"08:00",
    "fin de semana": r"sábado|domingo",
}
# Clases inválidas (partición de equivalencia) que la historia permite derivar
PARTICIONES = {
    "destino bloqueado": r"-> 191-0000004",
    "origen bloqueado": r"^191-0000004 ->",
    "destino inexistente": r"-> 191-9999999",
    "mismo titular": r"191-0000001 -> 191-0000002",
    "moneda distinta": r"191-0000001 -> 191-0000005",
    "monto no numérico": r"; [a-zA-Z]+$",
}


def mensajes() -> dict[str, str]:
    return dict(re.findall(r"^\| (R-\d\d) \| .*? \| (.*?) \|$", HISTORIA.read_text(encoding="utf-8"), re.M))


def medir(ruta: Path) -> dict:
    filas = list(csv.DictReader(ruta.open(encoding="utf-8")))
    msj = mensajes()
    validas, exactos, rechazos, vistos, duplicados = 0, 0, 0, set(), 0
    for f in filas:
        esperado = (f.get("Esperado") or "").strip()
        m = re.fullmatch(r"Rechazada (R-\d\d): (.+)", esperado)
        formato_ok = bool(re.fullmatch(r"CP-\d\d", f.get("Caso", ""))) and f.get("Regla") in msj and (esperado == "Aprobada" or m)
        validas += bool(formato_ok)
        if m:
            rechazos += 1
            exactos += msj.get(m.group(1)) == m.group(2)
        clave = (f.get("Regla"), f.get("Datos"))
        duplicados += clave in vistos
        vistos.add(clave)
    datos = [f.get("Datos", "") for f in filas]
    limites = [n for n, p in LIMITES.items() if any(re.search(p, d) for d in datos)]
    particiones = [n for n, p in PARTICIONES.items() if any(re.search(p, d) for d in datos)]
    return {
        "casos": len(filas),
        "formato válido": f"{validas}/{len(filas)}",
        "reglas cubiertas": f"{len({f.get('Regla') for f in filas} & set(msj))}/{len(msj)}",
        "mensajes exactos": f"{exactos}/{rechazos}",
        "duplicados": duplicados,
        "límites": f"{len(limites)}/{len(LIMITES)}",
        "particiones inválidas": f"{len(particiones)}/{len(PARTICIONES)}",
        "_faltan": [n for n in LIMITES if n not in limites] + [n for n in PARTICIONES if n not in particiones],
    }


def main(rutas: list[str]) -> None:
    resultados = {Path(r).stem: medir(Path(r)) for r in rutas}
    metricas = [k for k in next(iter(resultados.values())) if not k.startswith("_")]
    ancho = max(len(m) for m in metricas) + 2
    print("".ljust(ancho) + "".join(n.ljust(12) for n in resultados))
    for metrica in metricas:
        print(metrica.ljust(ancho) + "".join(str(r[metrica]).ljust(12) for r in resultados.values()))
    for nombre, r in resultados.items():
        if r["_faltan"]:
            print(f"\n{nombre} · falta probar: {', '.join(r['_faltan'])}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1:])
