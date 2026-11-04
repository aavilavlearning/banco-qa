# HITL duro: que el host pida aprobación antes de actuar

Las instrucciones "detente y pide aprobación" en una skill o un agente son un control **blando**:
el modelo podría saltárselas. La configuración del host es un control **duro**: la herramienta
no se ejecuta hasta que una persona la confirma.

## Claude Code
El repositorio trae `.claude/settings.json`:
- `allow`: se ejecutan sin preguntar (ejecutar la suite, leer resultados).
- `ask`: piden confirmación cada vez (`crear_borrador_defecto`, `git commit`).
- `deny`: nunca se ejecutan (`git push`, borrar archivos, editar `app/`, leer `.env`).

## GitHub Copilot en VS Code
- Las herramientas de servidores MCP piden confirmación antes de ejecutarse.
- Para `crear_borrador_defecto` elige siempre **permitir una vez**; nunca "permitir siempre".
- Revisa la configuración de aprobación automática de herramientas y de comandos de terminal:
  deja fuera de la aprobación automática todo lo que escriba, publique o borre.

## Regla del laboratorio
| Tipo de herramienta | Aprobación |
| --- | --- |
| Lectura (resultados, historia, matriz) | Automática |
| Ejecución en dev/qa (suite) | Automática |
| Escritura (borrador de defecto, commit) | Siempre con confirmación (HITL) |
| Publicar, borrar, desplegar, push | Prohibida |
