"""Flujo de triage con controles (Módulo 7): router -> generador -> evaluador -> HITL.

Ejemplo práctico (4 fallos de muestra del pipeline nocturno):
    BANCOQA_DEFECTOS=D1 python anexo-avanzado/control/flujo_triage.py --muestras control/muestras/fallos-nocturno.json
Ejercicio (fallos reales de tu suite con los defectos sembrados):
    BANCOQA_DEFECTOS=D1,D2 python anexo-avanzado/control/flujo_triage.py --ejecutar

El generador de borradores aquí es determinista para que el flujo se pueda mostrar sin modelo;
en el ejercicio, el participante lo reemplaza por su agente del Módulo 6.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "anexo-avanzado"))

from control import evaluador, hitl, router  # noqa: E402
from herramientas import qa_tools  # noqa: E402

MAX_VUELTAS = 3
MATRIZ_REFERENCIA = RAIZ / "soluciones" / "modulo-2" / "matriz.csv"
DIAS = {"martes": "2026-11-03", "sábado": "2026-11-07"}


def fila_de(caso: str) -> dict:
    for matriz in (RAIZ / "trazabilidad" / "matriz.csv", MATRIZ_REFERENCIA):
        for fila in csv.DictReader(matriz.open(encoding="utf-8")):
            if fila.get("Caso") == caso:
                return fila
    raise SystemExit(f"{caso} no está en la matriz")


def reproducir(fila: dict) -> str:
    """Reproduce el caso contra la API (respeta BANCOQA_DEFECTOS) y devuelve request/response."""
    from fastapi.testclient import TestClient

    from app.main import app, banco

    banco.reiniciar()
    partes = [p.strip() for p in fila["Datos"].split(";")]
    origen, destino = [c.strip() for c in partes[0].split("->")]
    montos = [m.strip() for m in partes[1].split("+")]
    lineas = []
    with TestClient(app) as cliente:
        if len(partes) > 2:
            dia, hora = partes[2].split()
            cliente.post("/api/test/reloj", json={"fecha_hora": f"{DIAS[dia]}T{hora}:00"})
            lineas.append(f"Reloj del banco fijado en {DIAS[dia]} {hora}")
        for monto in montos:
            cuerpo = {"cuenta_origen": origen, "cuenta_destino": destino, "monto": monto}
            respuesta = cliente.post("/api/transferencias", json=cuerpo)
            lineas.append(f"Request: POST /api/transferencias {json.dumps(cuerpo)}")
            lineas.append(f"Response: HTTP {respuesta.status_code} {json.dumps(respuesta.json(), ensure_ascii=False)}")
    banco.reiniciar()
    return "\n".join(f"    {linea}" for linea in lineas)


def generar_borrador(fallo: dict, fila: dict, reporte: str) -> dict:
    """Versión 1: lo mínimo que tiene un generador apurado (solo el error del test)."""
    origen_destino, *resto = [p.strip() for p in fila["Datos"].split(";")]
    montos = resto[0].split("+")
    pasos = [f"Transferir {m.strip()} de {origen_destino.replace('->', 'a')}" for m in montos]
    return qa_tools.crear_borrador_defecto(
        titulo=f"{fila['Descripcion']}: el sistema no cumple {fila['Regla']}",
        caso=fila["Caso"],
        regla=fila["Regla"],
        pasos=pasos,
        esperado=fila["Esperado"],
        obtenido=fallo["error"],
        evidencia=f"{fallo['test']}: {fallo['error']} · reporte {reporte}",
        severidad="Alta" if fila["Prioridad"] == "Alta" else "Media",
    )


def mejorar_borrador(ruta: Path, fila: dict, feedback: list[str]) -> None:
    """Versión 2: el generador incorpora el feedback del evaluador."""
    texto = ruta.read_text(encoding="utf-8")
    if any("reproducción HTTP" in f for f in feedback):
        texto += "\nReproducción contra la API:\n" + reproducir(fila) + "\n"
    if any("severidad" in f for f in feedback):
        texto = re.sub(r"(\*\*Severidad propuesta:\*\*) \w+", r"\1 Alta", texto)
    ruta.write_text(texto, encoding="utf-8")


def triage(fallos: list[dict], reporte: str, decision_qe: str | None) -> None:
    print(f"{'Fallo':<6} {'Caso':<6} {'Categoría':<12} {'Conf.':<6} {'HITL':<5} Acción")
    decisiones, casos_con_borrador = [], set()
    for fallo in fallos:
        fila = fila_de(fallo["caso"]) if fallo.get("caso") else {}
        d = router.clasificar(fallo, fila.get("Regla"))
        if not fila:
            d.requiere_hitl, d.accion = True, "Sin caso en la matriz: escalar al QE (¿cambio de comportamiento?)"
        elif d.categoria == "defecto" and fila["Caso"] in casos_con_borrador:
            d.accion = "Mismo caso que un fallo anterior: se suma como evidencia, sin borrador nuevo"
        elif d.categoria == "defecto":
            casos_con_borrador.add(fila["Caso"])
        decisiones.append((fallo, fila, d))
        caso = fallo.get("caso") or "-"
        print(f"{d.fallo:<6} {caso:<6} {d.categoria:<12} {d.confianza:<6} {'sí' if d.requiere_hitl else 'no':<5} {d.accion}")

    procesados = set()
    for fallo, fila, d in decisiones:
        if not fila or d.categoria != "defecto" or d.confianza < router.UMBRAL_CONFIANZA:
            if d.requiere_hitl:
                hitl.solicitar("HITL-ESCALA", d.fallo, f"{d.categoria} ({d.confianza}): {d.motivo}\n{fallo['error']}", decision_qe)
            continue

        if fila["Caso"] in procesados:
            continue
        procesados.add(fila["Caso"])
        mismos = [f for f, fi, _ in decisiones if fi and fi["Caso"] == fila["Caso"]]
        fallo = dict(fallo, test=" | ".join(f["test"] for f in mismos))
        borrador = generar_borrador(fallo, fila, reporte)
        ruta = RAIZ / borrador["ruta"]
        print(f"\n{d.fallo}: borrador {borrador['id']} generado")
        for vuelta in range(1, MAX_VUELTAS + 1):
            resultado = evaluador.evaluar(ruta.read_text(encoding="utf-8"))
            print(f"  Evaluador, vuelta {vuelta}: {resultado['puntajes']} -> {'aprobado' if resultado['aprobado'] else 'no aprobado'}")
            if resultado["aprobado"]:
                break
            for f in resultado["feedback"]:
                print(f"    feedback: {f}")
            mejorar_borrador(ruta, fila, resultado["feedback"])
        else:
            hitl.solicitar("HITL-ESCALA", borrador["id"], "El evaluador no aprobó tras 3 vueltas", decision_qe)
            continue

        registro = hitl.solicitar("HITL-03", borrador["id"], ruta.read_text(encoding="utf-8"), decision_qe)
        if registro["decision"] == "aprobado":
            texto = ruta.read_text(encoding="utf-8").replace(
                "BORRADOR · pendiente de evaluador y aprobación HITL-03",
                f"APROBADO POR QE ({registro['quien']}, {registro['fecha']}) · listo para registrar",
            )
            ruta.write_text(texto, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--muestras", help="JSON con fallos de ejemplo")
    grupo.add_argument("--ejecutar", action="store_true", help="Ejecuta la regresión en dev y hace triage de los fallos")
    parser.add_argument("--decision-qe", choices=["aprobado", "rechazado"], help="Solo para demos grabadas")
    args = parser.parse_args()

    if args.muestras:
        fallos = json.loads(Path(args.muestras).read_text(encoding="utf-8"))
        reporte = "reports/nocturno-muestra.xml"
    else:
        resumen = qa_tools.ejecutar_suite("regresion", "dev")
        fallos = [dict(f, id=f"F-{i:02d}") for i, f in enumerate(resumen["fallidos"], 1)]
        reporte = resumen["reporte"]
        print(f"Regresión: {resumen['total']} tests, {resumen['fallaron']} fallidos\n")
    triage(fallos, reporte, args.decision_qe)


if __name__ == "__main__":
    main()
