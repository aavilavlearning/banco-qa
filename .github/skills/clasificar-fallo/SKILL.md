---
name: clasificar-fallo
description: Clasifica fallos de tests de BancoQA (defecto, flaky, ambiente, test roto) y decide
  quién los atiende. Úsala cuando haya tests fallidos en una ejecución, en el pipeline nocturno
  o cuando pidan hacer triage. Es el ROUTER del flujo de QA.
---

# Clasificar fallos (router)

## Entradas
Por cada fallo: test, caso CP-xx, mensaje de error, historial de las últimas ejecuciones y
cambios recientes (si los hay). Fuente: `banco-qa/obtener_resultados_ci` o un archivo de fallos.

## Pasos
1. Agrupa los fallos por caso CP-xx: dos tests que fallan por el mismo caso son UN solo problema.
2. Clasifica cada caso con la primera señal de esta tabla que aplique:

   | Señal en el error o el historial | Categoría | Confianza base | Quién sigue |
   | --- | --- | --- | --- |
   | Timeout, conexión rechazada, servicio no disponible (503) | ambiente | 0.9 | Avisar a infraestructura; no crear defecto |
   | Pasa y falla en el mismo commit, sin cambios de código | flaky | 0.5 | QE decide (HITL) |
   | No encuentra un elemento de la pantalla después de un cambio de UI | test_roto | 0.9 | Agente de mantenimiento, en su rama |
   | Código HTTP, mensaje, saldo o movimiento distinto a lo que dice la regla | defecto | 0.9 | Skill `reportar-defecto` |
   | Ninguna de las anteriores, o el fallo no tiene caso CP-xx | desconocido | 0.3 | QE decide (HITL) |

3. Ajusta la confianza: baja 0.2 si la evidencia es parcial o contradictoria.
4. **Regla de banca:** si la confianza es menor a 0.7, o si es un defecto en una regla que mueve
   dinero (todas las de HU-01), **detente y pide la decisión del QE**. No continúes sin respuesta.
5. Escribe tu decisión en `salidas/registro-hitl.md` con el formato de `control/registro-hitl.md`.

## Salida
Una tabla: fallo | caso | categoría | confianza | evidencia (una frase) | quién sigue | ¿requiere HITL?

## Lo que nunca haces
- Crear un defecto por un fallo de ambiente o flaky.
- Corregir un test para que pase.
- Decidir por el QE cuando la regla dice que hay que preguntar.
