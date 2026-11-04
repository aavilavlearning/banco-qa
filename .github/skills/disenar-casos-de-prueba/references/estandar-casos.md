# Estándar de casos de prueba del equipo (BancoQA)

| Campo | Regla | Ejemplo |
| --- | --- | --- |
| Caso | `CP-` + dos dígitos, único | CP-07 |
| CA | Criterio de aceptación que cubre | CA-02 |
| Regla | Regla de negocio que cubre (una sola) | R-04 |
| Descripcion | Qué demuestra, en una línea, sin pasos | Acumulado supera el límite en soles por 0.01 |
| Datos | Cuenta origen -> destino; monto; hora si aplica | 191-0000001 -> 191-0000003; 6000.00 + 4000.01 |
| Esperado | `Aprobada` o `Rechazada R-xx: <mensaje exacto>` | Rechazada R-04: La operación supera tu límite diario |
| Prioridad | Alta, Media o Baja | Alta |

## Valores límite obligatorios en banca
- Montos: mínimo exacto y mínimo − 0.01; saldo exacto y saldo + 0.01.
- Límites acumulados: llegar exacto al límite y pasarlo por 0.01, en cada moneda.
- Horarios: primer y último minuto válidos, y el minuto siguiente o anterior.
- Decimales: 2 decimales (válido) y 3 decimales (inválido).

## Lo que no es un buen caso
- "Probar la transferencia" (no dice qué regla).
- "Muestra error" (no dice qué error ni qué regla).
- Datos reales de clientes: siempre ficticios.
