# Módulo 2 · Refactor de prompts

**Viene del M1:** tu prompt y tu matriz. **Pieza 2:** prompt refactorizado (v3) + bitácora con métricas.
**Trazabilidad que agregas:** columna `Prompt` (qué versión produjo cada caso: P-01 v1, v2, v3).

## Ejemplo práctico (instructor)
1. Medir el punto de partida: `python modulo-2/evaluar_salida.py modulo-2/ejemplo/salidas/salida-v1.csv`
2. Detectar olores con `modulo-2/catalogo-olores.md` (en el ejemplo: tarea monolítica, supone en vez de preguntar, límites a medias).
3. Refactor 1 (`modulo-2/ejemplo/prompt-v2.md`): dividir la tarea y preguntar primero. Medir.
4. Refactor 2 (`modulo-2/ejemplo/prompt-v3.md`): checklist de límites en ambos extremos. Medir.
5. Comparar las tres versiones:
   ```bash
   python modulo-2/evaluar_salida.py modulo-2/ejemplo/salidas/salida-v1.csv modulo-2/ejemplo/salidas/salida-v2.csv modulo-2/ejemplo/salidas/salida-v3.csv
   ```
   | | v1 | v2 | v3 |
   | --- | --- | --- | --- |
   | casos | 15 | 17 | 19 |
   | límites | 11/13 | 11/13 | 13/13 |
   | particiones inválidas | 4/6 | 6/6 | 6/6 |
6. Mostrar el meta-prompt (`modulo-2/plantilla-meta-prompt.md`): la IA propone el siguiente refactor y el QE decide.

Las salidas de `ejemplo/salidas/` son muestras ilustrativas para que la medición se pueda mostrar sin modelo.

## Ejercicio
1. Guarda la salida de tu prompt del M1 como `mi-salida-v1.csv` y mídela con `evaluar_salida.py`.
2. Identifica 2 olores con el catálogo (o con el meta-prompt).
3. Aplica un refactor por versión (v2, v3); guarda y mide cada salida con las mismas entradas.
4. Usa al menos 2 patrones de interacción (preguntar primero, confirmar entendimiento, feedback específico, autocrítica).
5. Llena tu bitácora (plantilla: `modulo-2/ejemplo/bitacora-refactor.md`).
6. Agrega los casos nuevos y la columna Prompt a tu matriz: `python trazabilidad/verificar_trazabilidad.py --modulo 2`

## Entregable
Prompt v3, bitácora con métricas y matriz con la columna Prompt.

**Solución de referencia:** `soluciones/modulo-2/`.
