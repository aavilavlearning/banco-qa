# Módulo 1 · Ejemplo · Prompt con contexto ("después")

Copia el bloque completo en el chat de tu asistente. Reemplaza `{...}` pegando el contenido de
`docs/HU-01-transferencia-terceros.md`.

```markdown
<rol>
Eres un QA senior de banca con experiencia en diseño de pruebas (ISTQB):
partición de equivalencia, valores límite y tablas de decisión.
</rol>

<contexto>
Sistema: BancoQA, banca digital de práctica (datos ficticios).
Historia, criterios de aceptación, reglas y datos de prueba:
{pega aquí docs/HU-01-transferencia-terceros.md}
</contexto>

<tarea>
Diseña los casos de prueba de HU-01 aplicando valores límite en montos, saldo,
límite diario (soles y dólares) y horario de interbancarias, y partición de
equivalencia para el resto de reglas.
</tarea>

<restricciones>
- No inventes reglas: si algo no está en el contexto, pregúntalo.
- Usa solo cuentas de la tabla de datos de prueba.
- Máximo 20 casos, ordenados por riesgo para el banco.
- Cada caso cubre una sola regla o criterio.
</restricciones>

<formato>
Tabla CSV con encabezado:
Caso,CA,Regla,Descripcion,Datos,Esperado,Prioridad
- Caso: CP-01, CP-02, ...
- Esperado: "Aprobada" o "Rechazada R-xx: <mensaje exacto>"
- Prioridad: Alta, Media o Baja
</formato>

<ejemplo>
CP-05,CA-02,R-03,Saldo insuficiente por 0.01,"191-0000003 -> 191-0000001; 500.01",Rechazada R-03: Saldo insuficiente para realizar la operación,Alta
</ejemplo>

<verificacion>
Al final, en una sección "Supuestos y preguntas para el PO", lista lo que
asumiste y lo que el PO debe aclarar. Confirma que cada regla R-01 a R-08
tiene al menos un caso.
</verificacion>
```

## Qué cambia en la salida

- Aparecen los límites: 0.99 / 1.00, 500.00 / 500.01, 6000 + 4000.00 / 6000 + 4000.01, 19:59 / 20:00.
- Cada caso trae su regla (`R-xx`) y el mensaje exacto: se puede automatizar tal cual.
- Salen preguntas que nadie había hecho, por ejemplo: ¿el límite diario es por cliente o por cuenta?
