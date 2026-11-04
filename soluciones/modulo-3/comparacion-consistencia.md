# Módulo 3 · Plantilla de comparación de consistencia de skills

Ejecuta cada skill 2 veces sobre HU-01 en conversaciones nuevas y llena la tabla.
Los valores de la fila "Ejemplo" son ilustrativos: reemplázalos con tus resultados.

| Skill | Métrica | Ejecución 1 | Ejecución 2 | Matriz aprobada del M1 | Observación |
| --- | --- | --- | --- | --- | --- |
| identificar-riesgos | Riesgos identificados | | | n/a | ¿Salieron los mismos RSK? |
| disenar-casos-de-prueba | Casos generados | | | 15 | ¿Cuántos coinciden con la matriz? |
| disenar-casos-de-prueba | Reglas cubiertas (de 8) | | | 8 | |
| disenar-casos-de-prueba | `validar_casos.py` sin errores | | | Sí | |
| Ejemplo | Casos generados | 16 | 15 | 15 | 14 coinciden; la ejecución 1 agregó un caso duplicado de R-01 |

**Conclusión esperada:** con la skill, las dos ejecuciones cubren las 8 reglas y pasan el validador;
con el prompt suelto del M1 la variación entre ejecuciones es mayor.
