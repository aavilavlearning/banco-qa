"""Prueba el servidor banco-qa como lo haría un host (VS Code, Claude Code): por stdio.

Uso: python servidor_mcp/probar_servidor.py
Lista herramientas y resources, lee la historia y ejecuta ejecutar_suite sobre CP-05.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

RAIZ = Path(__file__).resolve().parents[1]


async def main():
    parametros = StdioServerParameters(command=sys.executable, args=[str(RAIZ / "servidor_mcp" / "banco_qa_server.py")], env=dict(os.environ))
    async with stdio_client(parametros) as (lectura, escritura):
        async with ClientSession(lectura, escritura) as sesion:
            await sesion.initialize()

            herramientas = await sesion.list_tools()
            print("Herramientas:")
            for h in herramientas.tools:
                solo_lectura = h.annotations.read_only_hint if h.annotations else None
                print(f"  - {h.name} (solo lectura: {solo_lectura})")

            recursos = await sesion.list_resources()
            print("Resources:")
            for r in recursos.resources:
                print(f"  - {r.uri}")

            historia = await sesion.read_resource("banco-qa://historia/HU-01")
            print("Historia (primera línea):", historia.contents[0].text.splitlines()[0])

            resultado = await sesion.call_tool("ejecutar_suite", {"suite": "regresion", "ambiente": "dev", "casos": ["CP-05"]})
            print("ejecutar_suite(CP-05):")
            datos = resultado.structured_content or json.loads(resultado.content[0].text)
            print(json.dumps(datos, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
