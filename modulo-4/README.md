# Módulo 4 · Tool calling

**Usa:** la suite base de BancoQA (`tests/`). **Pieza 4:** herramientas `ejecutar_suite`, `obtener_resultados_ci`, `crear_borrador_defecto`.
**Trazabilidad que agregas:** columnas `Tests` y `Suite`: qué test de la suite base cubre cada caso (los tests llevan
`@pytest.mark.caso("CP-xx")`) y dónde corre. `ejecutar_suite` acepta `casos=["CP-xx"]`.

## Ejemplo práctico (instructor)
```bash
python herramientas/demo_ciclo.py '{"name": "ejecutar_suite", "arguments": {"suite": "api-transferencias", "ambiente": "dev"}}'
python herramientas/demo_ciclo.py '{"name": "ejecutar_suite", "arguments": {"suite": "api-transferencias", "ambiente": "produccion"}}'
BANCOQA_DEFECTOS=D1,D2 python herramientas/demo_ciclo.py '{"name": "ejecutar_suite", "arguments": {"suite": "regresion", "ambiente": "dev", "casos": ["CP-07", "CP-09"]}}'
```
Se ve la solicitud, la validación contra el esquema (`herramientas/definiciones.json`), la ejecución y el
resultado; el ambiente "produccion" se rechaza con un error que explica qué es válido.

## Ejercicio
1. Revisa `herramientas/definiciones.json` y `herramientas/qa_tools.py`; mejora descripciones si hace falta.
2. Registra las 3 herramientas en tu asistente (o úsalas vía MCP en el M5).
3. Lanza los 10 pedidos de `herramientas/pedidos-seleccion.md` y llena la tabla de aciertos.
4. Mejora las descripciones donde falló y repite. Meta: 9 de 10.
5. Busca qué tests cubren cada caso (`grep -rn 'caso("CP-07")' tests/`) y llena Tests y Suite:
   `python trazabilidad/verificar_trazabilidad.py --modulo 4`

## Entregable
Herramientas definidas e implementadas, y tabla de aciertos. Cada llamada queda en `logs/auditoria.jsonl`.
