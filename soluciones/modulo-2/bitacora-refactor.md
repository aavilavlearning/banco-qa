# Bitácora de refactor · P-01 (diseño de casos de HU-01)

Medición: `python modulo-2/evaluar_salida.py modulo-2/ejemplo/salidas/salida-v*.csv`

| Versión | Olor atacado | Cambio aplicado | Casos | Límites | Particiones inválidas | Decisión |
| --- | --- | --- | --- | --- | --- | --- |
| v1 | — (punto de partida) | Prompt con contexto del Módulo 1 | 15 | 11/13 | 4/6 | Medir y buscar olores |
| v2 | Tarea monolítica; supone en vez de preguntar | Paso 1 de variables y clases + preguntar primero | 17 | 11/13 | 6/6 | Se queda |
| v3 | Límites a medias | Checklist de límites en ambos extremos + contraejemplo | 19 | 13/13 | 6/6 | Versión final |

**Lo que se mantuvo en todas:** formato válido 100%, 8/8 reglas cubiertas, mensajes exactos y 0 duplicados.

**Aprendizajes:**
- Cada versión cambió una sola cosa; por eso se sabe qué produjo cada mejora.
- El refactor encontró casos que el prompt original no veía: origen bloqueado, monto no numérico y la apertura del horario de interbancarias.
- Pedirle que pregunte primero hizo visibles dos dudas para el PO antes de generar, no después.
