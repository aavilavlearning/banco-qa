---
name: disenar-casos-de-prueba
description: Diseña casos de prueba funcionales para historias de usuario bancarias aplicando
  valores límite, partición de equivalencia y tablas de decisión, con trazabilidad a reglas
  (R-xx) y criterios (CA-xx). Úsala cuando pidan casos, escenarios, cobertura o matriz de
  pruebas de una historia.
---

# Diseñar casos de prueba

## Entradas
- La historia con criterios de aceptación y reglas (por ejemplo `docs/HU-01-transferencia-terceros.md`).
- Opcional: la matriz de riesgos de la skill `identificar-riesgos` para priorizar.

## Pasos
1. Si falta información, haz hasta 3 preguntas y espera las respuestas. No supongas reglas.
2. Lista las reglas (R-xx), los criterios (CA-xx) y TODAS las variables de entrada
   (cuenta origen, cuenta destino, monto, moneda, fecha y hora), con sus clases válidas e inválidas.
3. Para cada rango aplica valores límite en AMBOS extremos: el valor justo en el límite y el
   inmediato fuera (1.00 y 0.99; saldo exacto y +0.01; acumulado exacto y +0.01;
   apertura 07:59 y 08:00; cierre 19:59 y 20:00; fin de semana).
4. Para el resto, aplica partición de equivalencia: un caso por clase inválida de cada variable.
5. Si dos o más condiciones se combinan, usa una tabla de decisión.
6. Usa solo cuentas de la tabla de datos de prueba de la historia.
7. Asigna prioridad según la matriz de riesgos si existe; si no, Alta para todo lo que mueve dinero.
8. Escribe la salida con el formato de `assets/plantilla-matriz.csv`.
9. Ejecuta `python .github/skills/disenar-casos-de-prueba/scripts/validar_casos.py <archivo.csv>` y corrige lo que reporte.

> Esta skill es el prompt P-01 v3 del Módulo 2 empaquetado (ver `modulo-2/ejemplo/prompt-v3.md`).

## Criterios de calidad
- Cada caso cubre una sola regla y cita su `R-xx` y su `CA-xx`.
- El esperado es "Aprobada" o "Rechazada R-xx: <mensaje exacto de la historia>".
- Todas las reglas de la historia tienen al menos un caso.
- Sin casos duplicados. Máximo 20 casos.
- Detalle del estándar: `references/estandar-casos.md`.

## Cierre
Presenta la matriz, la lista de supuestos y las preguntas para el PO.
**Detente y espera la aprobación del QE** antes de pasar los casos a automatización.
