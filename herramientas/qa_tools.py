"""Herramientas de QA para BancoQA (Módulo 4). El servidor MCP del Módulo 5 las expone tal cual.

Tipos:
- ejecutar_suite ........... ejecución (solo dev y qa)
- obtener_resultados_ci .... lectura
- crear_borrador_defecto ... escritura con aprobación humana: crea un BORRADOR, nunca publica

Trazabilidad: ejecutar_suite filtra por casos (CP-xx) usando los @pytest.mark.caso del código.
"""
from __future__ import annotations

import functools
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from trazabilidad.verificar_trazabilidad import tests_marcados  # noqa: E402

SUITES = {
    "unit": "tests/unit",
    "api-transferencias": "tests/api",
    "e2e-banca-web": "tests/e2e",
    "caracterizacion": "tests/caracterizacion",
    "regresion": "tests",
}
AMBIENTES = ("dev", "qa")
SEVERIDADES = ("Crítica", "Alta", "Media", "Baja")
REPORTES = RAIZ / "reports"
BORRADORES = RAIZ / "salidas" / "defectos" / "borradores"


AUDITORIA = RAIZ / "logs" / "auditoria.jsonl"


class ErrorHerramienta(ValueError):
    """Error con un mensaje que le enseña al modelo cómo corregir la llamada."""


def auditada(funcion):
    """Registra cada llamada (quién, qué, con qué argumentos y qué resultó) en logs/auditoria.jsonl."""

    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):
        registro = {
            "fecha": datetime.now().isoformat(timespec="seconds"),
            "herramienta": funcion.__name__,
            "argumentos": kwargs or list(args),
            "actor": os.getenv("BANCOQA_ACTOR", "desconocido"),
        }
        try:
            resultado = funcion(*args, **kwargs)
            registro["resultado"] = {k: resultado[k] for k in ("total", "fallaron", "id", "estado") if k in resultado}
            return resultado
        except Exception as error:
            registro["error"] = str(error)
            raise
        finally:
            AUDITORIA.parent.mkdir(exist_ok=True)
            with AUDITORIA.open("a", encoding="utf-8") as archivo:
                archivo.write(json.dumps(registro, ensure_ascii=False, default=str) + "\n")

    return envoltura


def _caso_de(nombre_test: str, por_caso: dict[str, set[str]]) -> str | None:
    for caso, tests in por_caso.items():
        if any(t.endswith("::" + nombre_test.split("[")[0]) for t in tests):
            return caso
    return None


@auditada
def ejecutar_suite(suite: str, ambiente: str, casos: list[str] | None = None) -> dict:
    """Ejecuta una suite de tests de BancoQA en dev o qa y devuelve un resumen corto.

    suite: unit, api-transferencias, e2e-banca-web, caracterizacion o regresion.
    ambiente: dev (app en memoria) o qa (servidor en BANCOQA_URL). Nunca producción.
    casos: opcional, lista de IDs de la matriz (por ejemplo ["CP-07"]) para ejecutar solo esos.
    """
    if suite not in SUITES:
        raise ErrorHerramienta(f"La suite '{suite}' no existe. Suites válidas: {', '.join(SUITES)}")
    if ambiente not in AMBIENTES:
        raise ErrorHerramienta(f"Ambiente '{ambiente}' no permitido. Ambientes válidos: dev, qa")

    entorno = dict(os.environ)
    if ambiente == "dev":
        entorno.pop("BANCOQA_URL", None)
    elif not entorno.get("BANCOQA_URL"):
        raise ErrorHerramienta("El ambiente qa no está configurado: define BANCOQA_URL con la URL del servidor de QA")

    objetivos = [SUITES[suite]]
    por_caso = tests_marcados()
    if casos:
        desconocidos = [c for c in casos if c not in por_caso]
        if desconocidos:
            raise ErrorHerramienta(f"Casos sin tests en el código: {', '.join(desconocidos)}")
        objetivos = sorted(t for c in casos for t in por_caso[c] if t.startswith(SUITES[suite]) or suite == "regresion")
        if not objetivos:
            raise ErrorHerramienta(f"Los casos {', '.join(casos)} no tienen tests en la suite {suite}")

    REPORTES.mkdir(exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d-%H%M%S")
    junit = REPORTES / f"{suite}-{ambiente}-{marca}.xml"
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={junit}", *objetivos],
        cwd=RAIZ, env=entorno, capture_output=True, text=True, timeout=600,
    )

    raiz_xml = ET.parse(junit).getroot()
    fallidos, total = [], 0
    for tc in raiz_xml.iter("testcase"):
        total += 1
        falla = tc.find("failure")
        if falla is None:
            falla = tc.find("error")
        if falla is not None:
            mensaje = (falla.get("message") or "").splitlines()[0][:200]
            fallidos.append({"test": tc.get("name"), "caso": _caso_de(tc.get("name"), por_caso), "error": mensaje})

    resumen = {
        "suite": suite,
        "ambiente": ambiente,
        "total": total,
        "pasaron": total - len(fallidos),
        "fallaron": len(fallidos),
        "fallidos": fallidos,
        "reporte": junit.relative_to(RAIZ).as_posix(),
        "fecha": datetime.now().isoformat(timespec="seconds"),
    }
    (REPORTES / "ultimo-resultado.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False), encoding="utf-8")
    return resumen


@auditada
def obtener_resultados_ci() -> dict:
    """Devuelve el resumen de la última ejecución registrada (local o del pipeline de CI).

    Solo lectura. Úsala cuando pregunten cómo terminó la última corrida o qué falló.
    """
    ultimo = REPORTES / "ultimo-resultado.json"
    if not ultimo.exists():
        raise ErrorHerramienta("Todavía no hay ejecuciones registradas. Usa ejecutar_suite primero.")
    return json.loads(ultimo.read_text(encoding="utf-8"))


@auditada
def crear_borrador_defecto(
    titulo: str,
    caso: str,
    regla: str,
    pasos: list[str],
    esperado: str,
    obtenido: str,
    evidencia: str,
    severidad: str,
) -> dict:
    """Crea un BORRADOR de defecto para que el QE lo revise. No publica nada.

    Úsala solo cuando un test falle por un posible defecto del sistema (no por el test ni el ambiente).
    caso: ID de la matriz (CP-xx). regla: ID de la regla incumplida (R-xx).
    severidad: Crítica, Alta, Media o Baja.
    """
    if severidad not in SEVERIDADES:
        raise ErrorHerramienta(f"Severidad inválida. Valores válidos: {', '.join(SEVERIDADES)}")
    if not caso.startswith("CP-") or not regla.startswith("R-"):
        raise ErrorHerramienta("caso debe ser CP-xx y regla R-xx, tal como en la matriz de trazabilidad")
    if not pasos:
        raise ErrorHerramienta("El borrador necesita al menos un paso para reproducir")

    BORRADORES.mkdir(parents=True, exist_ok=True)
    numero = len(list(BORRADORES.glob("DEF-*.md"))) + 1
    identificador = f"DEF-{numero:03d}"
    ruta = BORRADORES / f"{identificador}.md"
    lineas = [
        f"# {identificador} · {titulo}",
        "",
        "**Estado:** BORRADOR · pendiente de evaluador y aprobación HITL-03",
        f"**Trazabilidad:** HU-01 · {regla} · {caso}",
        f"**Severidad propuesta:** {severidad}",
        "",
        "## Pasos para reproducir",
        *[f"{i}. {p}" for i, p in enumerate(pasos, 1)],
        "",
        f"**Esperado:** {esperado}",
        "",
        f"**Obtenido:** {obtenido}",
        "",
        "## Evidencia",
        evidencia,
        "",
    ]
    ruta.write_text("\n".join(lineas), encoding="utf-8")
    return {"id": identificador, "estado": "BORRADOR", "ruta": ruta.relative_to(RAIZ).as_posix()}
