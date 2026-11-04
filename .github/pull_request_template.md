## Qué cambia
<!-- Historia, casos CP-xx y por qué -->

## Origen
- [ ] Lo hizo una persona
- [ ] Lo hizo un agente (rama `agente/...`): adjuntar log de iteraciones y registro HITL

## Checklist del revisor de QA (guardrail)
- [ ] No se eliminó, debilitó ni omitió (skip/xfail) ningún test existente
- [ ] Ninguna aserción existente cambió su valor esperado
- [ ] El agente solo escribió en `tests/agente/`, `trazabilidad/` o `salidas/`
- [ ] No hay datos reales (tarjetas, documentos, correos) ni URLs fuera de dev/qa
- [ ] Cada test nuevo tiene `@pytest.mark.caso("CP-xx")` y su fila en la matriz
- [ ] Los defectos encontrados se reportaron como borrador, no se "arreglaron" en el test
