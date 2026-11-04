# Prompt clasificador de fallos (cuando las reglas deterministas no deciden)

```markdown
<tarea>
Clasifica este fallo del pipeline de BancoQA en una sola categoría.
</tarea>
<categorias>
- defecto: el sistema no cumple la regla esperada (código HTTP, mensaje, saldo o movimiento incorrecto)
- flaky: el test pasa y falla sin cambios de código
- ambiente: caída de servicio, timeout de infraestructura, datos de prueba faltantes
- test_roto: el test quedó desactualizado por un cambio válido de la aplicación
</categorias>
<entrada>
Test: {nodo del test}
Caso y regla: {CP-xx · R-xx}
Error: {mensaje}
Historial: {últimas 5 ejecuciones}
Cambios recientes: {commits o archivos}
</entrada>
<reglas>
- Si dudas entre defecto y test_roto, elige defecto con confianza baja: un humano decide.
- No inventes datos que no estén en la entrada.
</reglas>
<formato>
{"categoria": "...", "confianza": 0.0-1.0, "evidencia": "frase que justifica la categoría"}
</formato>
```
