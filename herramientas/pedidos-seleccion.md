# Módulo 4 · Ejercicio · 10 pedidos para evaluar la selección de herramientas

Lanza cada pedido en una conversación nueva con las 3 herramientas disponibles.
Llena las columnas "Herramienta elegida" y "Argumentos" con lo que pidió el modelo.

| # | Pedido en lenguaje natural | Herramienta esperada | Argumentos esperados | Herramienta elegida | Argumentos | ¿Acertó? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ¿Pasa la suite de transferencias en dev? | ejecutar_suite | suite=api-transferencias, ambiente=dev | | | |
| 2 | Corre todo antes del merge | ejecutar_suite | suite=regresion, ambiente=dev | | | |
| 3 | ¿Cómo terminó la última corrida? | obtener_resultados_ci | — | | | |
| 4 | Verifica solo el límite diario en soles | ejecutar_suite | casos=[CP-06, CP-07] | | | |
| 5 | Prueba la pantalla de transferir | ejecutar_suite | suite=e2e-banca-web | | | |
| 6 | Córrelo en producción | ninguna (o error de ambiente) | — | | | |
| 7 | CP-07 falló con 201 en vez de 422, regístralo | crear_borrador_defecto | caso=CP-07, regla=R-04 | | | |
| 8 | El test falló por timeout del servidor, ¿lo reportamos? | obtener_resultados_ci (no crear defecto) | — | | | |
| 9 | ¿El servicio sigue respondiendo igual que antes del refactor? | ejecutar_suite | suite=caracterizacion | | | |
| 10 | Revisa los casos de horario de interbancarias en qa | ejecutar_suite | ambiente=qa, casos=[CP-13..CP-17] | | | |

**Meta:** 9 de 10 aciertos. Si falla, mejora la descripción de la herramienta (no el pedido) y repite.
