# HU-01 · Transferencia a terceros

> Sistema de práctica BancoQA. Todos los datos son ficticios.

## Historia de usuario

**Como** cliente de banca por internet
**quiero** transferir dinero desde una de mis cuentas a la cuenta de otra persona
**para** pagarle sin ir a una agencia.

## Criterios de aceptación

- **CA-01** Si la operación cumple todas las reglas, se aprueba: se debita la cuenta origen, se abona la cuenta destino, se registra un movimiento en cada cuenta y se devuelve un número de operación.
- **CA-02** Si la operación incumple alguna regla, se rechaza con un mensaje claro, sin mover dinero ni registrar movimientos.
- **CA-03** Las transferencias interbancarias solo se procesan en horario hábil.

## Reglas de negocio

| ID | Regla | Mensaje de rechazo |
| --- | --- | --- |
| R-01 | El monto mínimo es 1.00 (en la moneda de la cuenta) | El monto mínimo es 1.00 |
| R-02 | El monto admite como máximo 2 decimales | El monto admite como máximo 2 decimales |
| R-03 | La cuenta origen debe tener saldo suficiente | Saldo insuficiente para realizar la operación |
| R-04 | Límite diario acumulado por cliente: S/ 10,000.00 en soles y US$ 3,000.00 en dólares (incluye la operación actual) | La operación supera tu límite diario |
| R-05 | Las cuentas origen y destino deben estar activas (no bloqueadas) | La cuenta origen o destino no está habilitada |
| R-06 | Origen y destino deben tener la misma moneda | Las cuentas deben tener la misma moneda |
| R-07 | La cuenta destino debe existir y pertenecer a otro titular | La cuenta destino no es válida para esta operación |
| R-08 | Interbancarias (destino de otro banco, número que empieza con 999) solo de lunes a viernes de 08:00 a 20:00 | Las transferencias interbancarias solo se procesan de lunes a viernes de 08:00 a 20:00 |

## Datos de prueba (ficticios)

| Cuenta | Titular | Moneda | Saldo | Estado |
| --- | --- | --- | --- | --- |
| 191-0000001 | Ana Torres (CLI-001) | PEN | 15,000.00 | Activa |
| 191-0000002 | Ana Torres (CLI-001) | USD | 5,000.00 | Activa |
| 191-0000003 | Bruno Díaz (CLI-002) | PEN | 500.00 | Activa |
| 191-0000004 | Carla Ríos (CLI-003) | PEN | 0.00 | Bloqueada |
| 191-0000005 | Diego Paz (CLI-004) | USD | 100.00 | Activa |
| 999-0000006 | Elena Soto (otro banco) | PEN | 0.00 | Activa |
| 191-0000007 | (titular con texto malicioso, demo del Módulo 5) | PEN | 10.00 | Activa |
