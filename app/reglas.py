"""Reglas de negocio de HU-01 · Transferencia a terceros (BancoQA, sistema de práctica).

Cada validación lleva el ID de la regla que implementa (R-01 a R-08), para mantener
la trazabilidad historia -> regla -> caso -> test.

Defectos sembrados (solo para el laboratorio): se activan con la variable de entorno
BANCOQA_DEFECTOS. Valores: "D1", "D2" o "D1,D2". Ver docs/DEFECTOS-INSTRUCTOR.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation

MONTO_MINIMO = Decimal("1.00")
LIMITE_DIARIO = {"PEN": Decimal("10000.00"), "USD": Decimal("3000.00")}
PREFIJO_OTRO_BANCO = "999-"
HORA_INICIO_INTERBANCARIA = 8
HORA_FIN_INTERBANCARIA = 20  # exclusiva: a las 20:00 ya no se procesa


@dataclass
class Cuenta:
    numero: str
    titular: str
    cliente: str
    moneda: str
    saldo: Decimal
    bloqueada: bool = False


class ReglaIncumplida(Exception):
    def __init__(self, regla: str, mensaje: str):
        super().__init__(mensaje)
        self.regla = regla
        self.mensaje = mensaje


def convertir_monto(valor) -> Decimal:
    try:
        monto = Decimal(str(valor))
    except (InvalidOperation, ValueError):
        raise ReglaIncumplida("R-01", "El monto mínimo es 1.00")
    if not monto.is_finite():
        raise ReglaIncumplida("R-01", "El monto mínimo es 1.00")
    return monto


def es_interbancaria(numero_destino: str) -> bool:
    return numero_destino.startswith(PREFIJO_OTRO_BANCO)


def en_horario_interbancario(ahora: datetime) -> bool:
    es_dia_habil = ahora.weekday() < 5  # lunes=0 ... viernes=4
    return es_dia_habil and HORA_INICIO_INTERBANCARIA <= ahora.hour < HORA_FIN_INTERBANCARIA


def validar_transferencia(
    origen: Cuenta,
    destino: Cuenta | None,
    monto: Decimal,
    acumulado_hoy: Decimal,
    ahora: datetime,
    defectos: frozenset[str] = frozenset(),
) -> None:
    """Lanza ReglaIncumplida con la primera regla que no se cumple."""
    # R-02 · máximo 2 decimales
    if monto.as_tuple().exponent < -2:
        raise ReglaIncumplida("R-02", "El monto admite como máximo 2 decimales")

    # R-01 · monto mínimo
    if monto < MONTO_MINIMO:
        raise ReglaIncumplida("R-01", "El monto mínimo es 1.00")

    # R-07 · destino existe y es de otro titular
    if destino is None or destino.cliente == origen.cliente:
        raise ReglaIncumplida("R-07", "La cuenta destino no es válida para esta operación")

    # R-05 · cuentas activas
    destino_bloqueado = destino.bloqueada
    if "D2" in defectos:
        destino_bloqueado = False  # D2 sembrado: no valida el destino
    if origen.bloqueada or destino_bloqueado:
        raise ReglaIncumplida("R-05", "La cuenta origen o destino no está habilitada")

    # R-06 · misma moneda
    if origen.moneda != destino.moneda:
        raise ReglaIncumplida("R-06", "Las cuentas deben tener la misma moneda")

    # R-08 · horario de interbancarias
    if es_interbancaria(destino.numero) and not en_horario_interbancario(ahora):
        raise ReglaIncumplida(
            "R-08",
            "Las transferencias interbancarias solo se procesan de lunes a viernes de 08:00 a 20:00",
        )

    # R-03 · saldo suficiente
    if monto > origen.saldo:
        raise ReglaIncumplida("R-03", "Saldo insuficiente para realizar la operación")

    # R-04 · límite diario acumulado por cliente y moneda
    limite = LIMITE_DIARIO[origen.moneda]
    total_del_dia = acumulado_hoy + monto
    if "D1" in defectos:
        total_del_dia = monto  # D1 sembrado: ignora lo acumulado
    if total_del_dia > limite:
        raise ReglaIncumplida("R-04", "La operación supera tu límite diario")
