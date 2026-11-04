---
name: identificar-riesgos
description: Identifica y prioriza riesgos de calidad de una historia de usuario bancaria
  (dinero, límites, monedas, horarios, cuentas no habilitadas, datos inválidos) y los vincula
  a reglas R-xx. Úsala cuando pidan riesgos, análisis de riesgo, priorización o "qué puede salir
  mal" en una historia, antes de diseñar casos.
---

# Identificar riesgos de calidad

## Entradas
- La historia con criterios de aceptación y reglas.

## Pasos
1. Lee la historia y lista qué puede salir mal para el cliente y para el banco.
2. Recorre las categorías de `references/catalogo-riesgos-banca.md` y descarta las que no apliquen.
3. Redacta cada riesgo como "<qué falla> provoca <impacto>", con ID RSK-xx.
4. Vincula cada riesgo a las reglas R-xx que lo controlan. Un riesgo sin regla es una pregunta para el PO.
5. Califica impacto y probabilidad (Alto, Medio, Bajo) y calcula la prioridad con la tabla del catálogo.
6. Escribe la salida con el formato de `assets/plantilla-riesgos.csv`.

## Criterios de calidad
- Todo lo que mueve dinero tiene impacto Alto.
- Cada riesgo cita al menos una regla, o queda marcado como pregunta para el PO.
- No hay riesgos genéricos ("la aplicación falla"): cada uno es verificable con casos.

## Cierre
Presenta la matriz de riesgos ordenada por prioridad.
**Detente y espera la aprobación del QE (punto HITL-01)** antes de diseñar casos.
