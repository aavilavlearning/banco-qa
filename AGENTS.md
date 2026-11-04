# Reglas para agentes en este repositorio (BancoQA · laboratorio)

## Proyecto
BancoQA es un banco de práctica con datos ficticios. Historia principal: `docs/HU-01-transferencia-terceros.md`.
Trazabilidad: `trazabilidad/matriz.csv` (HU -> regla -> caso -> test -> herramienta -> agente -> control -> eval).

## Comandos
- Instalar: `pip install -r requirements.txt && playwright install chromium`
- Todos los tests: `pytest -q`
- Una suite: `pytest -q tests/api`
- Trazabilidad: `python trazabilidad/verificar_trazabilidad.py --modulo 2`
- Triage de fallos: agente `agentes/orquestador-triage.md` (skills clasificar-fallo y reportar-defecto)

## Reglas
- Trabaja siempre en una rama `agente/<tarea>`. Nunca hagas push a `main`.
- Nunca elimines, debilites ni marques como skip o xfail un test existente.
- Si un test falla por un posible defecto, repórtalo con `crear_borrador_defecto`; no lo corrijas.
- Todo test nuevo lleva `@pytest.mark.caso("CP-xx")` y su fila en la matriz.
- Selectores por rol o etiqueta en E2E; nunca clases CSS ni `time.sleep`.
- Solo datos ficticios de la historia. Nunca datos reales de clientes, cuentas ni tarjetas.
- Solo ambientes dev y qa. Nunca URLs ni bases de datos de producción.
- Escribes solo en `tests/agente/`, `trazabilidad/` y `salidas/`. No modificas `app/`.
- Antes de crear un borrador de defecto, pide aprobación del QE (HITL-03) y registra la decisión en `salidas/registro-hitl.md`.
- Nunca apruebas en nombre del QE. Si nadie responde, te detienes.
