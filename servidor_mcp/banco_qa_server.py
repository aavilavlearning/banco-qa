"""Servidor MCP banco-qa (Módulo 5).

Expone las herramientas del Módulo 4 y los documentos clave como resources.
Usa el SDK oficial de Python para MCP, versión 2 (en v1 la clase se llamaba FastMCP).

Ejecutar (stdio, lo lanza el host):   python servidor_mcp/banco_qa_server.py
Probar sin host:                      python servidor_mcp/probar_servidor.py
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

from herramientas import qa_tools  # noqa: E402

mcp = MCPServer(
    "banco-qa",
    instructions=(
        "Herramientas de QA para BancoQA (datos ficticios). Solo ambientes dev y qa. "
        "Los defectos se crean como borradores para aprobación humana."
    ),
)


@mcp.tool(annotations=ToolAnnotations(read_only_hint=False, destructive_hint=False, idempotent_hint=True))
def ejecutar_suite(suite: str, ambiente: str, casos: list[str] | None = None) -> dict:
    """Ejecuta una suite de tests de BancoQA en dev o qa y devuelve un resumen corto.
    suite: unit, api-transferencias, e2e-banca-web, caracterizacion o regresion.
    ambiente: dev o qa (nunca producción). casos: opcional, IDs CP-xx de la matriz."""
    return qa_tools.ejecutar_suite(suite, ambiente, casos)


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def obtener_resultados_ci() -> dict:
    """Devuelve el resumen de la última ejecución registrada. Solo lectura."""
    return qa_tools.obtener_resultados_ci()


@mcp.tool(annotations=ToolAnnotations(read_only_hint=False, destructive_hint=False))
def crear_borrador_defecto(
    titulo: str, caso: str, regla: str, pasos: list[str], esperado: str, obtenido: str, evidencia: str, severidad: str
) -> dict:
    """Crea un BORRADOR de defecto (no publica) para revisión del QE. Solo para posibles defectos del sistema.
    caso: CP-xx. regla: R-xx. severidad: Crítica, Alta, Media o Baja."""
    return qa_tools.crear_borrador_defecto(titulo, caso, regla, pasos, esperado, obtenido, evidencia, severidad)


@mcp.resource("banco-qa://historia/HU-01", mime_type="text/markdown")
def historia_hu01() -> str:
    """Historia HU-01 con criterios de aceptación, reglas R-01..R-08 y datos de prueba ficticios."""
    return (RAIZ / "docs" / "HU-01-transferencia-terceros.md").read_text(encoding="utf-8")


@mcp.resource("banco-qa://trazabilidad/matriz", mime_type="text/csv")
def matriz_trazabilidad() -> str:
    """Matriz de trazabilidad de trabajo (HU -> regla -> caso -> test -> ...)."""
    return (RAIZ / "trazabilidad" / "matriz.csv").read_text(encoding="utf-8")


@mcp.resource("banco-qa://openapi", mime_type="application/json")
def contrato_openapi() -> str:
    """Contrato OpenAPI vigente de la API de BancoQA."""
    import json

    from app.main import app

    return json.dumps(app.openapi(), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
