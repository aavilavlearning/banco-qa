# Módulo 7 · Routing, evaluator y HITL (sin código)

**Viene del M6:** tu agente. **Pieza 7:** flujo de triage con router, evaluador y puntos HITL construidos
como skills, subagentes y configuración del host.
**Trazabilidad que agregas:** columna `Control` (qué control pasó cada caso y qué se decidió).

## Las piezas
| Control | Cómo se construye | Archivo |
| --- | --- | --- |
| Router | Skill con tabla de señales, categoría y confianza | `.github/skills/clasificar-fallo/SKILL.md` |
| Generador | Skill que redacta el borrador de defecto | `.github/skills/reportar-defecto/` |
| Evaluador | Subagente con rúbrica de 5 criterios (aprueba con ≥ 4 en todos) | `agentes/revisor-defectos.md` |
| Orquestador | Agente que une router → generador → evaluador → HITL | `agentes/orquestador-triage.md` |
| HITL blando | "Detente y pide decisión" dentro de skills y agentes | las mismas skills y agentes |
| HITL duro | El host pide confirmación antes de crear el borrador | `modulo-7/configurar-aprobaciones.md`, `.claude/settings.json` |
| Registro | Tabla markdown de decisiones del QE | `control/registro-hitl.md` → `salidas/registro-hitl.md` |

## Ejemplo práctico (instructor)
1. Levanta BancoQA con `BANCOQA_DEFECTOS=D1`.
2. Pide al asistente, con el agente `orquestador-triage`:
   ```text
   Haz el triage de control/muestras/fallos-nocturno.json.
   ```
3. Muestra cada paso contra `modulo-7/ejemplo/decisiones-esperadas.md`:
   - el router clasifica los 4 fallos y escala F-02 (flaky, confianza 0.5) y F-04 (defecto que toca dinero);
   - el revisor rechaza el primer borrador de CP-07 (evidencia 3: falta la reproducción HTTP) y aprueba el segundo;
   - el host pide confirmación antes de `crear_borrador_defecto` y el QE aprueba (HITL-03).

## Ejercicio
1. Activa los dos defectos sembrados: `BANCOQA_DEFECTOS=D1,D2`.
2. Ejecuta el flujo con `orquestador-triage` sobre tus propios fallos (corre la regresión de tu agente del M6).
3. Decide en cada punto HITL y deja tus decisiones en `salidas/registro-hitl.md`.
4. Calibra el revisor: puntúa tú los borradores con la misma rúbrica y compara. Si no coinciden, ajusta las
   descripciones de la rúbrica en `agentes/revisor-defectos.md`.
5. Agrega una señal nueva a la tabla de `clasificar-fallo` (por ejemplo, "datos de prueba consumidos") y pruébala.
6. Agrega la columna Control a tu matriz: `python trazabilidad/verificar_trazabilidad.py --modulo 7`

## Entregable
Borradores DEF-001 y DEF-002 aprobados por el revisor y por ti, y el registro de decisiones.
**Referencia:** `soluciones/modulo-7/`.

> **Nivel avanzado (opcional):** el mismo flujo programado en Python está en `anexo-avanzado/control/`.
