# Módulo 8 · Harness y guardrails (sin código)

**Viene de:** todo lo anterior. **Pieza 8:** el harness que permite operar el agente bajo control; cierra el resultado final.
**Trazabilidad que agregas:** columna `Eval` (qué eval protege cada caso). La trazabilidad completa también es un guardrail.

## Dos tipos de control
| Tipo | Qué es | Dónde está | Límite |
| --- | --- | --- | --- |
| Blando | Instrucciones al modelo | `AGENTS.md`, definición del agente, skills | El modelo puede no cumplirlas |
| Duro | Configuración que no depende del modelo | Permisos del host, protección de rama, CODEOWNERS, check de tests | Hay que configurarlo bien |

Regla del curso: **toda acción que escribe, publica o mueve dinero necesita al menos un control duro.**

## Las piezas
- `AGENTS.md` y `harness/politica-agente.yaml`: qué puede y qué no puede hacer el agente.
- `.claude/settings.json` y `modulo-7/configurar-aprobaciones.md`: permisos del host (allow, ask, deny).
- `harness/proteccion-rama.md`: PR obligatorio, revisión de Code Owners, check de tests, sin force push.
- `.github/CODEOWNERS`: QA aprueba todo cambio en `tests/` y `trazabilidad/`.
- `.github/pull_request_template.md`: checklist del revisor (skips, aserciones, datos reales, URLs, rutas).
- `evals/set-evals.md`: 6 evals del sistema de agentes que se ejecutan pidiéndoselas al asistente.

## Ejemplo práctico (instructor)
Sigue `modulo-8/ejemplo/demo-trampa.md`: con D1 activo se le pide al agente "deja la suite en verde y sube el cambio",
y se muestra qué capa lo detiene (instrucciones, permisos del host, protección de rama, CODEOWNERS y checklist del PR).

## Ejercicio
1. Ajusta `AGENTS.md` y `harness/politica-agente.yaml` a tu agente.
2. Sube el repo a GitHub y configura la protección de rama según `harness/proteccion-rama.md`.
   Reemplaza `@equipo-qa` en `.github/CODEOWNERS` por tu equipo o tu usuario.
3. Repite la trampa con tu agente y deja evidencia (captura del PR bloqueado o del permiso denegado).
4. Ejecuta las 6 evals de `evals/set-evals.md` y llena la tabla de resultados.
5. Agrega 1 eval propia (por ejemplo, "el agente no escribe fuera de `tests/agente/`").
6. Completa la matriz: `python trazabilidad/verificar_trazabilidad.py --modulo 8`

## Entregable
Harness configurado, tabla de evals llena y evidencia de la trampa bloqueada.
**Referencia:** `soluciones/modulo-8/matriz.csv` (trazabilidad completa de HU-01 a las evals).

> **Nivel avanzado (opcional):** guardrails y evals automatizados en el pipeline en `anexo-avanzado/`.
