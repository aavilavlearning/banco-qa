# Módulo 1 · Solución de referencia · Supuestos y preguntas para el PO

| # | Pregunta | Supuesto usado en BancoQA | Riesgo si se asume mal |
| --- | --- | --- | --- |
| P-01 | ¿El límite diario se reinicia a las 00:00 (día calendario) o son 24 horas móviles? | Día calendario | Clientes bloqueados o límite burlable cerca de medianoche |
| P-02 | ¿El límite diario es por cliente o por cuenta? | Por cliente y por moneda | Un cliente con varias cuentas podría superar el límite |
| P-03 | ¿Las operaciones rechazadas suman al límite diario? | No suman | Bloqueo indebido después de un rechazo |
| P-04 | ¿Los feriados cuentan como días hábiles para interbancarias? | No está definido | Interbancarias procesadas en feriado |
| P-05 | ¿Las interbancarias tienen comisión? | No hay comisión | Saldo final distinto al esperado |
| P-06 | ¿Qué mensaje ve el cliente si la cuenta origen no existe? | 404 "La cuenta origen no existe" | Mensaje técnico expuesto al cliente |

Las respuestas del PO se registran aquí y, si cambian una regla, se actualiza `docs/HU-01-transferencia-terceros.md`
y la matriz de trazabilidad.
