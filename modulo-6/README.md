# Módulo 6 · Agentes

**Viene de:** skills (M3) + servidor `banco-qa` (M5). **Pieza 6:** `agente-qa-api` con log de iteraciones.
**Trazabilidad que agregas:** columna `Agente` (en qué iteración diseñó y ejecutó cada caso).

## Ejemplo práctico (instructor)
1. Definición: `agentes/agente-qa-api.md` (rol, objetivo verificable, pasos, límites, parada, entrega).
2. Log comentado: `agentes/ejemplo/log-ejemplo-R04.md` (R-04 con el defecto D1).
3. Salidas reales de cada paso: `BANCOQA_DEFECTOS=D1 python agentes/ejemplo/reproducir_ejemplo.py`
   El agente corrige su propio error de test, pero ante el posible defecto **para y lo reporta**.

## Ejercicio
1. Copia `agentes/agente-qa-api.md` a la carpeta de agentes de tu herramienta y ajusta el encabezado.
2. Ejecútalo sobre HU-01 en dev (sin defectos), con máximo 8 iteraciones; escribe en `tests/agente/`.
3. Aprueba o corrige en HITL-01 (riesgos) y HITL-02 (casos).
4. Registra el log con `agentes/plantilla-log.md` y revisa: ¿paró por la razón correcta?
5. Verifica: `python trazabilidad/verificar_trazabilidad.py --modulo 6`

## Entregable
Definición del agente, tests generados y log. **Referencia:** `soluciones/modulo-6/log-agente-HU-01.md`.
