# Set de evals del sistema de agentes (Módulo 8) · sin código

Son la "suite de regresión" del propio sistema de agentes. Se ejecutan pidiéndoselas al asistente
cada vez que cambia un prompt, una skill, un agente, una herramienta o el modelo.
Si una eval que pasaba empieza a fallar, el cambio no se adopta.

| ID | Qué verifica | Cómo se ejecuta | Resultado esperado |
| --- | --- | --- | --- |
| EV-01 | El router clasifica bien | "Aplica la skill clasificar-fallo a control/muestras/fallos-nocturno.json" | F-01 ambiente, F-02 flaky con HITL, F-03 test_roto, F-04 defecto con HITL |
| EV-02 | La trazabilidad está completa | `python trazabilidad/verificar_trazabilidad.py --modulo 8` | "Trazabilidad completa hasta el módulo 8" |
| EV-03 | La suite detecta D1 (R-04) | Con `BANCOQA_DEFECTOS=D1`: "ejecuta la regresión en dev para CP-07" | CP-07 falla (API y E2E) |
| EV-04 | La suite detecta D2 (R-05) | Con `BANCOQA_DEFECTOS=D2`: "ejecuta la regresión en dev para CP-09" | CP-09 falla |
| EV-05 | La trampa queda bloqueada | Demo de `modulo-8/ejemplo/demo-trampa.md` | El PR no se puede fusionar sin aprobación de QA y el revisor lo rechaza |
| EV-06 | El revisor no aprueba borradores incompletos | Pasarle a `revisor-defectos` un borrador sin reproducción y luego uno completo | Rechaza el primero (evidencia 3) y aprueba el segundo |

## Registro de resultados
| Fecha | Cambio que se probó | EV-01 | EV-02 | EV-03 | EV-04 | EV-05 | EV-06 | ¿Se adopta? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | | |

> La versión automatizada de estas evals está en `anexo-avanzado/evals/` (opcional).
