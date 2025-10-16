"""
 _id, cliente_id, tarjeta_id, monto, fecha_intento, status (approved / declined),
codigo_motivo, reembolsado (boolean), fecha_reembolso
"""
from enum import Enum


class ChargeStatus(str, Enum):
    DECLINED = "DECLINED"
    APPROVED = "APPROVED"


class ChargeModel:
    def __init__(self, id_charge, customer_id, card_id, amount,
                 attempt_date, status, reason_code, is_refunded,
                 refund_date):
        self.id_charge = id_charge
        self.customer_id = customer_id
        self.card_id = card_id
        self.amount = amount
        self.attempt_date = attempt_date
        self.status = status
        self.reason_code = reason_code
        self.is_refunded = is_refunded
        self.refund_date = refund_date

    @classmethod
    def by_dto(cls, charge_dto):
        return cls(
            id_charge=None,
            customer_id=charge_dto.customer_id,
            card_id=charge_dto.card_id,
            amount=charge_dto.amount,
            attempt_date=None,
            status=ChargeStatus.DECLINED,
            reason_code=None,
            is_refunded=False,
            refund_date=None
        )
