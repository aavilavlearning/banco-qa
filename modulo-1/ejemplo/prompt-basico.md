# Módulo 1 · Ejemplo · Prompt básico ("antes")

```text
Genera casos de prueba para una transferencia a terceros.
```

## Qué suele devolver (salida típica, ilustrativa)

1. Transferir con datos válidos → la transferencia se realiza.
2. Transferir sin saldo → muestra error.
3. Transferir a una cuenta que no existe → muestra error.
4. Dejar campos vacíos → muestra error de validación.
5. Transferir un monto negativo → muestra error.

## Por qué no sirve así

| Problema | Consecuencia |
| --- | --- |
| No conoce las reglas de BancoQA | No prueba el límite diario, el horario de interbancarias ni las monedas |
| No hay valores límite | "Sin saldo" no dice si probó 500.00 vs 500.01 |
| Resultados esperados vagos ("muestra error") | No se pueden automatizar ni verificar |
| No hay trazabilidad | No se sabe qué regla cubre cada caso |
| No declara supuestos | Inventa comportamiento sin avisar |
