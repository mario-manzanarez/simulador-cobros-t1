from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from model.charge_model import ChargeStatus


# ----------------------------
# DTO para crear charge
# ----------------------------
class ChargeCreateDto(BaseModel):
    customer_id: str
    card_id: str
    amount: float = Field(..., gt=0, description="Monto del cobro, debe ser mayor a 0")


# ----------------------------
# DTO para leer charge
# ----------------------------
class ChargeReadDto(BaseModel):
    id_charge: str
    customer_id: str
    card_id: str
    amount: float
    attempt_date: datetime
    status: ChargeStatus
    reason_code: Optional[str] = None
    is_refunded: bool
    refund_date: Optional[datetime] = None
    pan_mask: Optional[str] = None
    last_4: Optional[str] = None



