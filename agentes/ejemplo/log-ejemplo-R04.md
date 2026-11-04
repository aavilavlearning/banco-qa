# Log del agente · AG-EJ · HU-01 (solo R-04, límite diario) · ambiente dev con el defecto D1 activo

> Ejemplo práctico del Módulo 6. Para ver las salidas reales de cada paso de herramienta:
> `BANCOQA_DEFECTOS=D1 python agentes/ejemplo/reproducir_ejemplo.py`

| It. | Decisión del agente | Herramienta o skill | Resultado observado | ¿Sigue o para? |
| --- | --- | --- | --- | --- |
| 1 | Leer la historia y filtrar R-04 | resource `banco-qa://historia/HU-01` | R-04: límite S/ 10,000 y US$ 3,000, acumulado del día | Sigue |
| 2 | Diseñar casos de R-04 con valores límite | skill `disenar-casos-de-prueba` | CP-06 (exacto al límite), CP-07 (+0.01), CP-08 (dólares) | **Para: HITL-02**, el QE aprueba |
| 3 | Escribir 3 tests en `tests/agente/test_hu01_r04.py` | edición de archivo | 3 tests con `@pytest.mark.caso` | Sigue |
| 4 | Ejecutar los 3 casos | `ejecutar_suite(regresion, dev, [CP-06, CP-07, CP-08])` | 1 falla: `NameError: name 'transferir' is not defined` | Sigue: es error del test |
| 5 | Corregir el import del helper y volver a ejecutar | edición + `ejecutar_suite` | 2 pasan; CP-07 falla: `assert 201 == 422` | Sigue: posible defecto |
| 6 | No tocar el test; reportar | `crear_borrador_defecto(caso=CP-07, regla=R-04, ...)` | Borrador DEF-001 creado | **Para: defecto reportado** |

**Motivo de parada:** defecto reportado. El agente corrigió su propio error en la iteración 5 (un import),
pero no "arregló" el fallo de la iteración 5 porque el sistema no cumplía R-04.

**Lo que se enseña con este log:**
- Distinguir error del test (se corrige) de posible defecto (se reporta).
- La parada la decide el resultado de la ejecución, no la opinión del modelo.
- Cada paso queda registrado y es auditable (`logs/auditoria.jsonl`).
