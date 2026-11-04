# Guardrail duro sin código: protección de la rama main en GitHub

Esto se configura en GitHub, no se programa. Es el control que bloquea un cambio aunque el agente
"obedezca" o no sus instrucciones.

## Configuración (Settings → Branches → regla para `main`, o Rulesets)
1. **Exigir pull request antes de hacer merge**: nadie, ni personas ni agentes, escribe directo en `main`.
2. **Exigir al menos 1 aprobación.**
3. **Exigir revisión de Code Owners**: los cambios en `tests/`, `trazabilidad/` y `.github/` los aprueba QA (ver `.github/CODEOWNERS`).
4. **Descartar aprobaciones si llegan commits nuevos.**
5. **Exigir que pase el check de tests** (`.github/workflows/qa.yml`).
6. **Bloquear force push y borrado de la rama.**

## Qué controla cada pieza
| Pieza | Qué impide |
| --- | --- |
| Pull request obligatorio | Que un agente haga push directo a main |
| Revisión de Code Owners | Que se cambien tests o la matriz sin que QA lo vea |
| Plantilla de PR | Que el revisor olvide revisar skips, aserciones, datos reales y rutas |
| Check de tests | Hacer merge con la suite en rojo |
| Permisos del host (`.claude/settings.json` o aprobaciones de Copilot) | Que el agente haga push, borre o edite `app/` sin preguntar |

> Para automatizar además el conteo de aserciones y skips en el pipeline, ver `anexo-avanzado/harness/` (opcional).
