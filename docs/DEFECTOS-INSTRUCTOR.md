# Defectos sembrados · solo para el instructor

Se activan con la variable de entorno `BANCOQA_DEFECTOS` antes de levantar BancoQA o correr tests.

| ID | Regla | Qué hace mal | Casos que lo detectan |
| --- | --- | --- | --- |
| D1 | R-04 | Ignora el acumulado del día: solo compara el monto de la operación con el límite | CP-07 (API y E2E) |
| D2 | R-05 | No valida que la cuenta destino esté bloqueada | CP-09 (API) |

```bash
BANCOQA_DEFECTOS=D1,D2 pytest -q                 # 4 fallos: CP-07 (x2), CP-09 y caracterización
BANCOQA_DEFECTOS=D1 uvicorn app.main:app --port 8000
```

## Uso por módulo
- **Suite base:** la caracterización detecta cualquiera de los dos como "cambio de comportamiento".
- **M6:** ejemplo práctico con D1 (`agentes/ejemplo/reproducir_ejemplo.py`).
- **M7:** ejercicio con D1 y D2 usando el agente `orquestador-triage` (resultado esperado en `modulo-7/ejemplo/decisiones-esperadas.md`).
- **M8:** las evals EV-03 y EV-04 de `evals/set-evals.md` verifican que la suite siga detectándolos.

No compartas este archivo con los participantes antes del Módulo 7.
