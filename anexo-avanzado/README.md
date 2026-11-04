# Anexo avanzado (opcional) · Controles programados en Python

Los módulos 7 y 8 se trabajan sin código: skills, subagentes y configuración del host y de GitHub.
Este anexo es para quien quiera automatizar los mismos controles en un pipeline.

| Carpeta | Qué hace | Equivale a |
| --- | --- | --- |
| `control/router.py` | Clasifica fallos con reglas | Skill `clasificar-fallo` |
| `control/evaluador.py` | Puntúa borradores con la rúbrica | Subagente `revisor-defectos` |
| `control/hitl.py` | Pide la decisión del QE y la registra | Puntos HITL + permisos `ask` del host |
| `control/flujo_triage.py` | Une todo el flujo | Agente `orquestador-triage` |
| `harness/verificar_guardrails.py` | Bloquea PRs que quitan aserciones, agregan skips, usan datos reales o URLs fuera de dev/qa | CODEOWNERS + checklist del PR |
| `harness/demo_trampa.sh` | Demo de la trampa bloqueada en el pipeline | `modulo-8/ejemplo/demo-trampa.md` |
| `evals/ejecutar_evals.py` | Ejecuta EV-01..EV-06 automáticamente | `evals/set-evals.md` |

## Comandos (desde la raíz del repo)
```bash
BANCOQA_DEFECTOS=D1 python anexo-avanzado/control/flujo_triage.py --muestras control/muestras/fallos-nocturno.json
./anexo-avanzado/harness/demo_trampa.sh
python anexo-avanzado/evals/ejecutar_evals.py
python anexo-avanzado/harness/verificar_guardrails.py --base main
```

Para activarlos en GitHub Actions, descomenta los pasos opcionales de `.github/workflows/qa.yml`.
