# Módulo 7 · Ejemplo · Qué debería decidir cada control

Entrada: los 4 fallos de `control/muestras/fallos-nocturno.json` (pipeline nocturno de muestra).

## 1. Router (skill `clasificar-fallo`)

Pedido al asistente:
```text
Aplica la skill clasificar-fallo a los fallos de control/muestras/fallos-nocturno.json.
```

| Fallo | Caso | Señal | Categoría | Confianza | ¿HITL? | Quién sigue |
| --- | --- | --- | --- | --- | --- | --- |
| F-01 | CP-13 | ConnectTimeout a qa.bancoqa.local | ambiente | 0.9 | No | Infraestructura |
| F-02 | CP-01 | Pasó y falló en el mismo commit | flaky | 0.5 | **Sí** (confianza baja) | QE |
| F-03 | CP-05 | No encuentra el botón "Transferir" tras un cambio de UI | test_roto | 0.9 | No | Agente de mantenimiento |
| F-04 | CP-07 | `assert 201 == 422` (se aprobó lo que R-04 rechaza) | defecto | 0.9 | **Sí** (toca dinero) | Skill `reportar-defecto` |

## 2. Generador + evaluador (skill `reportar-defecto` + subagente `revisor-defectos`)

- **Vuelta 1:** el borrador trae pasos, esperado exacto y el error del test, pero no la reproducción.
  ```text
  puntajes: trazabilidad=5, reproducibilidad=5, esperado=5, evidencia=3, severidad=5
  aprobado: no
  feedback:
  - La evidencia no incluye la reproducción HTTP (request y response de cada paso)
  ```
- El generador vuelve a ejecutar CP-07 y agrega los dos request/response (6000.00 → 201 y 4000.01 → 201).
- **Vuelta 2:** 5 en todos los criterios → aprobado por el revisor.

## 3. HITL-03
El orquestador muestra el borrador y **espera**. El QE aprueba; la decisión queda en `salidas/registro-hitl.md`.
Resultado esperado del borrador: `soluciones/modulo-7/DEF-001.md`.

> Para comparar, la versión programada de este mismo flujo está en `anexo-avanzado/control/` (opcional).
