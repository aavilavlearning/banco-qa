# Laboratorio · IA aplicada a testing · BancoQA

Laboratorio de 8 módulos sobre **una sola historia**, HU-01 "Transferencia a terceros", en BancoQA,
un banco de práctica con **datos ficticios**. Cada ejercicio produce una pieza que usa el siguiente,
y la matriz de trazabilidad conecta todo: historia → regla → caso → prompt → riesgo → test → herramienta → MCP →
agente → control → eval.

> Nunca uses datos reales de clientes ni sistemas internos en este laboratorio.

## Requisitos

- Python 3.11 o superior.
- Node.js (para Playwright MCP en el Módulo 5).
- Git y un editor con un asistente de IA aprobado, con modo agente, skills y MCP.

## Instalación

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
pytest -q                                              # 36 tests en verde
uvicorn app.main:app --port 8000                       # web: http://localhost:8000/transferir
```

**Servidor MCP con `.venv`:** `.mcp.json` y `.vscode/mcp.json` lanzan `banco-qa` con el comando `python`.
Si instalaste las dependencias en `.venv`, abre el editor con el entorno activado o cambia `"command"`
por la ruta del Python del entorno (Windows: `.venv\Scripts\python.exe`; macOS/Linux: `.venv/bin/python`).
Si no, el servidor no conecta.

**Ambientes:** `dev` usa la app en memoria y no necesita nada más. `qa` necesita la variable
`BANCOQA_URL` con la URL del servidor de QA. Nunca se usa producción.

## Ruta del laboratorio

| Módulo | Ejercicio | Pieza que deja | Columna de trazabilidad | Verificación |
| --- | --- | --- | --- | --- |
| 1 · Prompts con contexto | Prompt con contexto para HU-01 | Matriz de casos + preguntas al PO | HU, CA, Regla, Caso, Descripcion, Datos, Esperado, Prioridad | `verificar_trazabilidad.py --modulo 1` |
| 2 · Refactor de prompts | Prompt v1 → v3 medido con evaluar_salida.py | Prompt refactorizado + bitácora | Prompt | `--modulo 2` |
| 3 · Skills | Skills de riesgos y casos | 2 skills versionadas | Riesgo | `--modulo 3` |
| 4 · Tool calling | 3 herramientas + 10 pedidos | Herramientas auditadas | Tests, Suite | `--modulo 4` |
| 5 · MCP | Servidor banco-qa + Playwright MCP | Servidor MCP + test E2E explorado | Herramienta_MCP | `--modulo 5` |
| 6 · Agentes | agente-qa-api sobre HU-01 | Agente + log de iteraciones | Agente | `--modulo 6` |
| 7 · Routing, evaluator y HITL | Triage con skill router, subagente revisor y HITL | Flujo controlado + registro HITL | Control | `--modulo 7` |
| 8 · Harness y guardrails | Permisos del host, protección de rama, CODEOWNERS, evals | Resultado final operable | Eval | `--modulo 8` |

Cada `modulo-N/README.md` tiene el ejemplo práctico, el ejercicio paso a paso y el entregable.
Si no terminaste una pieza, usa la de `soluciones/` para seguir con el siguiente módulo.

## Estructura

```text
app/                    BancoQA (FastAPI + web), reglas R-01..R-08 en app/reglas.py
docs/                   Historia HU-01 y notas del instructor (defectos sembrados)
trazabilidad/           Matriz de trabajo y verificador
tests/                  Suite base de BancoQA (unit, api, e2e, caracterizacion) y agente/ (lo escribe el agente)
modulo-1..8/            Ejemplos y plantillas de cada módulo
.github/skills/         Skills de QA: identificar-riesgos y disenar-casos-de-prueba (M3);
                        clasificar-fallo (router) y reportar-defecto (generador) (M7)
herramientas/           Herramientas y ciclo de tool calling (M4)
servidor_mcp/           Servidor MCP banco-qa (M5); .vscode/mcp.json y .mcp.json
agentes/                agente-qa-api con su ejemplo (M6); revisor-defectos (evaluador)
                        y orquestador-triage (M7)
control/                Fallos de muestra y plantilla del registro HITL (M7)
.claude/settings.json   Permisos del host: allow, ask (HITL) y deny (M7-M8)
AGENTS.md               Reglas que todo agente sigue en este repositorio (rutas, ambientes, datos, HITL)
harness/                Política del agente y protección de rama (M8)
.github/CODEOWNERS      QA aprueba cambios en tests y trazabilidad (M8)
.github/pull_request_template.md  Checklist del revisor de QA para cada PR (M8)
evals/                  Set de evals del sistema de agentes (M8)
.github/workflows/      Pipeline: tests + trazabilidad
anexo-avanzado/         Opcional: router, evaluador, HITL, guardrails y evals programados en Python
soluciones/             Solución de referencia de cada módulo
```

Carpetas que se generan al trabajar (Git las ignora):

```text
reports/                Resultados de ejecutar_suite (JUnit XML y ultimo-resultado.json)
logs/                   auditoria.jsonl: cada llamada a una herramienta, con actor y resultado
salidas/                registro-hitl.md (decisiones del QE) y defectos/borradores/ (DEF-xxx)
```

Antes de cada sesión, borra `salidas/defectos/borradores/` si quedaron borradores de pruebas
anteriores: la numeración DEF-xxx sigue desde el último que encuentre.

## Comandos útiles

```bash
python trazabilidad/verificar_trazabilidad.py --modulo 3     # ¿mi matriz está completa hasta el M3?
python servidor_mcp/probar_servidor.py                       # probar el servidor MCP sin host
python anexo-avanzado/evals/ejecutar_evals.py                # opcional: evals automatizadas
```

En Windows, define `PYTHONUTF8=1` si los acentos salen mal en la consola. La eval EV-05 del anexo
ejecuta `anexo-avanzado/harness/demo_trampa.sh`, que necesita bash y un `python3` real en el PATH.
