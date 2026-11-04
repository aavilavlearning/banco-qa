# Módulo 3 · Skills

**Viene del M2:** tu prompt refactorizado (v3). **Pieza 3:** skills `identificar-riesgos` y `disenar-casos-de-prueba`.
**Trazabilidad que agregas:** columna `Riesgo` (RSK-xx) en la matriz.

## Ejemplo práctico (instructor)
1. Se abre `.github/skills/disenar-casos-de-prueba/` y se muestra cómo salió del prompt v3 del M2:
   descripción (cuándo se activa), pasos, `references/`, `assets/` y `scripts/validar_casos.py`.
2. Se pide "necesito los casos de HU-01" sin nombrar la skill: el agente la activa.
3. Se cambia la descripción a "ayuda con testing" y se muestra que deja de activarse.
4. Se corre el validador sobre una salida: `python .github/skills/disenar-casos-de-prueba/scripts/validar_casos.py soluciones/modulo-1/matriz.csv`

## Ejercicio
1. Convierte tu prompt v3 del M2 en tu versión de `disenar-casos-de-prueba` (o ajusta la de referencia).
2. Revisa y ajusta `identificar-riesgos` para HU-01.
3. Ejecuta cada skill 2 veces en conversaciones nuevas y llena `soluciones/modulo-3/comparacion-consistencia.md`.
4. Agrega la columna Riesgo a tu matriz y verifica: `python trazabilidad/verificar_trazabilidad.py --modulo 3`

## Entregable
Las 2 skills versionadas, la matriz de riesgos y la comparación de consistencia.

**Solución de referencia:** `.github/skills/` y `soluciones/modulo-3/`.
