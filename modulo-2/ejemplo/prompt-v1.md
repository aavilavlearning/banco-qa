# P-01 v1 · Punto de partida del refactor

Es el prompt con contexto del Módulo 1, sin cambios: `modulo-1/ejemplo/prompt-con-contexto.md`.

**Salida de muestra:** `salidas/salida-v1.csv` (15 casos).

**Medición:**
```bash
python modulo-2/evaluar_salida.py modulo-2/ejemplo/salidas/salida-v1.csv
# límites 11/13 · particiones inválidas 4/6
# falta probar: interbancaria 07:59, interbancaria 08:00, origen bloqueado, monto no numérico
```

**Olores que se detectan:**
- **Tarea monolítica:** pide "diseña los casos" de una vez; el modelo solo piensa en el destino y olvida variables (cuenta origen, formato del monto).
- **Supone en vez de preguntar:** no hay espacio para dudas antes de generar; los supuestos aparecen al final, cuando ya influyeron en los casos.
- **Límites a medias:** en el horario prueba el cierre (19:59/20:00) pero no la apertura (07:59/08:00).
