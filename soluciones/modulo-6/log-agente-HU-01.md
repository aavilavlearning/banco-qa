# Log de referencia · AG-01 · HU-01 completa · ambiente dev sin defectos

> Forma esperada del log del ejercicio 6. Tu agente puede tomar otro camino o necesitar otras
> iteraciones: lo que se revisa es que cada paso esté registrado y que pare por la razón correcta.

| It. | Decisión del agente | Herramienta o skill | Resultado observado | ¿Sigue o para? |
| --- | --- | --- | --- | --- |
| 1 | Leer historia y matriz | resources `banco-qa://historia/HU-01` y `banco-qa://trazabilidad/matriz` | 8 reglas, 3 criterios; matriz con 19 casos | Sigue |
| 2 | Identificar riesgos y diseñar casos | skills `identificar-riesgos` y `disenar-casos-de-prueba` + `validar_casos.py` | 6 riesgos, 19 casos, validador sin errores | **Para: HITL-01 y HITL-02** (QE aprueba) |
| 3 | Escribir tests de API para los casos sin test de API | edición de `tests/agente/test_hu01_agente.py` | 9 tests nuevos con `@pytest.mark.caso` | Sigue |
| 4 | Ejecutar los tests nuevos | `ejecutar_suite(regresion, dev, [CP-02, CP-03, ...])` | 8 pasan; 1 falla: `KeyError: 'regla'` en CP-04 | Sigue: error del test (CP-04 es aprobada, no trae regla) |
| 5 | Corregir la aserción de CP-04 para verificar estado APROBADA y volver a ejecutar | edición + `ejecutar_suite` | 9 de 9 pasan | Sigue |
| 6 | Actualizar columnas Tests y Agente de la matriz | edición de `trazabilidad/matriz.csv` | `verificar_trazabilidad.py --modulo 6` sin brechas | **Para: objetivo cumplido** |

**Motivo de parada:** objetivo cumplido y verificado por la ejecución y por el verificador de trazabilidad.

**Revisión del QE:** la corrección de la iteración 5 cambió una aserción *del test que el propio agente
acababa de escribir* porque el caso esperaba "Aprobada"; no tocó tests existentes. Si hubiera cambiado
una aserción de un test aprobado, el guardrail del Módulo 8 lo habría bloqueado.
