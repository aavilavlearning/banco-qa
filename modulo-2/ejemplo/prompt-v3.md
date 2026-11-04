# P-01 v3 · Refactor: checklist de límites en ambos extremos

**Olor que ataca:** límites a medias.
**Cambio:** se agrega una checklist explícita de valores límite y un contraejemplo. Todo lo demás queda igual que en v2.

```markdown
<!-- ... rol, contexto, interaccion, paso_1, paso_2, restricciones y formato iguales a v2 ... -->

<checklist_limites>                                    <!-- NUEVO en v3 -->
Para cada rango, incluye el valor justo en el límite y el inmediato fuera, en AMBOS extremos:
- Montos: mínimo (1.00 / 0.99) y decimales (2 / 3).
- Saldo: exacto / exacto + 0.01.
- Límite diario: acumulado exacto / + 0.01, en soles y en dólares.
- Horario de interbancarias: apertura (07:59 / 08:00), cierre (19:59 / 20:00) y fin de semana.
</checklist_limites>

<contraejemplo>                                        <!-- NUEVO en v3 -->
Caso incompleto: probar solo 20:00 para el horario. Falta 19:59 (cierre válido),
07:59 y 08:00 (apertura) y el fin de semana.
</contraejemplo>

<verificacion>
Confirma que cada regla, cada clase inválida del paso 1 y cada punto de la checklist de
límites tiene al menos un caso. Si alguno falta, agrégalo antes de entregar.
</verificacion>
```

**Salida de muestra:** `salidas/salida-v3.csv` (19 casos). Aparecen 07:59 y 08:00: límites de 11/13 a 13/13.
Esta es la versión que pasa a ser skill en el Módulo 3.
