---
name: reportar-defecto
description: Redacta el borrador de un defecto de BancoQA con trazabilidad (HU, regla, caso),
  pasos reproducibles y evidencia, y lo pasa al revisor antes de pedir aprobación. Úsala cuando
  un fallo fue clasificado como defecto.
---

# Reportar un defecto (generador)

## Entradas
- El fallo clasificado como defecto (test, caso CP-xx, error).
- La fila del caso en `trazabilidad/matriz.csv` (regla, datos, esperado).
- La historia `docs/HU-01-transferencia-terceros.md` (mensaje exacto de la regla).

## Pasos
1. Llena `assets/plantilla-defecto.md`. Un borrador por caso, aunque fallen varios tests de ese caso.
2. Pasos: uno por operación, con cuentas y montos de la columna Datos.
3. Esperado: copia el mensaje EXACTO de la regla desde la historia.
4. Evidencia: el error del test, la ruta del reporte y la reproducción (request y response de
   cada paso). Si no tienes la reproducción, ejecuta el caso de nuevo con `banco-qa/ejecutar_suite`.
5. Severidad: Alta o Crítica si la regla mueve dinero.
6. Crea el borrador con `banco-qa/crear_borrador_defecto` (queda como BORRADOR; no se publica).
7. Pide la revisión al subagente `revisor-defectos`. Si no aprueba, corrige SOLO lo que indica su
   feedback y vuelve a pedir revisión. Máximo 3 vueltas; si no aprueba, escala al QE.
8. Con la aprobación del revisor, **detente en HITL-03**: muestra el borrador al QE y espera su
   decisión (aprobar, rechazar con feedback o editar). Regístrala en `salidas/registro-hitl.md`.
