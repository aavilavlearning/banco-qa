# Plantilla de prompt con contexto para QA

```markdown
<rol>
{Quién responde y con qué criterio. Ej.: QA senior de banca, técnicas ISTQB.}
</rol>

<contexto>
{Sistema, historia, criterios de aceptación, reglas, datos de prueba disponibles.}
</contexto>

<tarea>
{Un verbo concreto y su alcance. Ej.: Diseña casos de valores límite para R-04.}
</tarea>

<restricciones>
- {Qué no hacer. Ej.: no inventes reglas.}
- {Límites de cantidad, datos permitidos, prioridad.}
</restricciones>

<formato>
{Estructura exacta de la salida: CSV, tabla, JSON o Gherkin, con sus columnas.}
</formato>

<ejemplo>
{1 a 3 ejemplos bien hechos.}
</ejemplo>

<verificacion>
{Cómo debe autoevaluarse: supuestos, preguntas, cobertura de reglas.}
</verificacion>
```

## Checklist antes de usar la salida

- [ ] ¿Cada caso cita su regla o criterio?
- [ ] ¿Los resultados esperados son concretos y verificables?
- [ ] ¿Hay valores límite donde corresponde?
- [ ] ¿Inventó alguna regla? (compárala con la historia)
- [ ] ¿Revisé los supuestos y llevé las preguntas al PO?
