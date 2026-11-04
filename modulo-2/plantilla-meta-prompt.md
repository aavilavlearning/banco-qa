# Meta-prompt: pedirle a la IA que refactorice tu prompt

Úsalo en una conversación nueva. La IA propone; **tú decides** qué cambio aplicar y lo mides.

```markdown
<rol>
Eres un ingeniero de prompts que revisa prompts de QA para banca.
</rol>

<prompt_actual>
{pega tu prompt}
</prompt_actual>

<evidencia>
Salida que produjo: {pega la salida o un resumen}
Métricas: {pega el resultado de modulo-2/evaluar_salida.py}
Lo que no me gustó: {por ejemplo, "faltan límites de horario"}
</evidencia>

<tarea>
1. Identifica los olores del prompt usando este catálogo: tarea vaga, tarea monolítica,
   contexto de más o de menos, contradicciones, sin formato, sin ejemplos, supone en vez
   de preguntar, sin verificación, datos mezclados, instrucciones en negativo, límites a medias.
2. Elige el olor que más explica la evidencia.
3. Propón la versión siguiente cambiando SOLO ese olor.
</tarea>

<formato>
- Olor elegido y por qué (2 líneas)
- Diff entre la versión actual y la nueva
- Qué métrica debería mejorar
</formato>
```

# Patrones para mejorar la interacción (no solo el prompt)

| Patrón | Qué le dices | Para qué sirve |
| --- | --- | --- |
| Preguntar primero | "Antes de generar, haz hasta 3 preguntas si falta información y espera mi respuesta" | Evita supuestos escondidos |
| Confirmar entendimiento | "Resume en 5 líneas las reglas que vas a usar" | Detectas malentendidos antes de la salida |
| Feedback específico | "CP-05 no tiene el mensaje exacto; corrige solo ese caso" | Mejora sin regenerar todo |
| Autocrítica | "Revisa tu salida contra la checklist y corrige lo que falle" | La IA atrapa sus propios errores |
| Dividir la conversación | Un turno para variables, otro para casos | Menos olvidos en tareas grandes |
