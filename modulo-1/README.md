# Módulo 1 · Prompts con contexto

**Pieza 1 del resultado final:** matriz de casos aprobada + preguntas para el PO.
**Trazabilidad que agregas:** columnas `HU, CA, Regla, Caso, Descripcion, Datos, Esperado, Prioridad`.

## Ejemplo práctico (instructor)
1. `modulo-1/ejemplo/prompt-basico.md`: se pega el prompt de una línea y se revisa la salida típica.
2. `modulo-1/ejemplo/prompt-con-contexto.md`: mismo pedido con rol, historia, reglas, formato CSV y verificación.
3. Se comparan: límites (0.99/1.00, 500.00/500.01, 19:59/20:00), reglas citadas y preguntas para el PO.

## Ejercicio
1. Arma tu prompt con `modulo-1/plantilla-prompt.md` y la historia `docs/HU-01-transferencia-terceros.md`.
2. Ejecútalo y pega la salida en `trazabilidad/matriz.csv` (columnas del M1).
3. Revisa cada caso con el checklist de la plantilla: acepta, corrige o descarta.
4. Ajusta el prompt una vez y mide si sube el porcentaje de casos aceptados.
5. Verifica: `python trazabilidad/verificar_trazabilidad.py --modulo 1`

## Entregable
- Tu prompt final y `trazabilidad/matriz.csv` con las 8 reglas cubiertas.
- Lista de supuestos y preguntas para el PO.

**Solución de referencia:** `soluciones/modulo-1/` (matriz de 15 casos y preguntas al PO).
