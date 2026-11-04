# Módulo 5 · MCP

**Viene del M4:** tus herramientas. **Pieza 5:** servidor MCP `banco-qa` + Playwright MCP.
**Trazabilidad que agregas:** columna `Herramienta_MCP` y el resource `banco-qa://trazabilidad/matriz`.

## Ejemplo práctico (instructor)
1. Probar el servidor como lo haría un host: `python servidor_mcp/probar_servidor.py`
2. Configuración: `.vscode/mcp.json` (Copilot en VS Code) o `.mcp.json` (Claude Code).
3. Exploración con Playwright MCP y demo de prompt injection: `modulo-5/ejemplo/prompt-exploracion.md`.

Nota técnica: `servidor_mcp/banco_qa_server.py` usa el SDK de Python MCP versión 2 (`MCPServer`).
En la versión 1 la clase se llamaba `FastMCP`.

## Ejercicio
1. Revisa el servidor y agrega una anotación o resource que te falte.
2. Configúralo en tu host junto con Playwright MCP y verifica que el asistente ve las herramientas.
3. Explora "Transferencia a terceros" con Playwright MCP y genera 1 test E2E para tu suite (con su marca `caso`).
4. Ejecuta tu suite desde el asistente vía `banco-qa`.
5. Verifica: `python trazabilidad/verificar_trazabilidad.py --modulo 5`

## Entregable
`mcp.json`, servidor funcionando y el test E2E nuevo. **Referencia:** `tests/e2e/test_limite_diario_web.py`.
