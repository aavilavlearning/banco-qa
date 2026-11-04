# P-01 v2 · Refactor: dividir la tarea y preguntar primero

**Olor que ataca:** tarea monolítica (y supone en vez de preguntar).
**Cambio:** la tarea se divide en dos pasos dentro de la misma interacción, y el modelo pregunta antes de generar.
Todo lo demás queda igual que en v1.

```markdown
<rol>
Eres un QA senior de banca con experiencia en diseño de pruebas (ISTQB).
</rol>

<contexto>
Sistema: BancoQA, banca digital de práctica (datos ficticios).
{pega aquí docs/HU-01-transferencia-terceros.md}
</contexto>

<interaccion>                                          <!-- NUEVO en v2 -->
Antes de generar, haz hasta 3 preguntas si falta información y espera mis respuestas.
Si no falta nada, escribe "Sin preguntas" y continúa.
</interaccion>

<paso_1>                                               <!-- NUEVO en v2 -->
Lista TODAS las variables de entrada de la operación (cuenta origen, cuenta destino,
monto, moneda, fecha y hora) y, para cada una, sus clases válidas e inválidas según las reglas.
</paso_1>

<paso_2>
Con la lista del paso 1, diseña los casos: una clase inválida por caso y valores límite
en montos, saldo, límite diario (soles y dólares) y horario de interbancarias.
</paso_2>

<restricciones>
- No inventes reglas. Usa solo cuentas de la tabla de datos de prueba.
- Máximo 20 casos, ordenados por riesgo. Cada caso cubre una sola regla.
</restricciones>

<formato>
Primero la lista del paso 1. Luego el CSV: Caso,CA,Regla,Descripcion,Datos,Esperado,Prioridad
Esperado: "Aprobada" o "Rechazada R-xx: <mensaje exacto>"
</formato>

<ejemplo>
CP-05,CA-02,R-03,Saldo insuficiente por 0.01,"191-0000003 -> 191-0000001; 500.01",Rechazada R-03: Saldo insuficiente para realizar la operación,Alta
</ejemplo>

<verificacion>
Confirma que cada regla R-01 a R-08 y cada clase inválida del paso 1 tiene al menos un caso.
</verificacion>
```

**Salida de muestra:** `salidas/salida-v2.csv` (17 casos). El paso 1 hizo aparecer la cuenta
**origen** bloqueada y el monto **no numérico**: particiones inválidas de 4/6 a 6/6.
Preguntas que hizo antes de generar (ejemplo): "¿el límite diario se reinicia a las 00:00?",
"¿los feriados cuentan como día hábil para interbancarias?".
