from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


#  _id, cliente_id, pan_masked (ej. ************1234), last4, bin, created_at,
# updated_at
class CardDto(BaseModel):
    customer_id: str
    card_number: str
    expiration_month: int
    expiration_year: int


class CardResponse(BaseModel):
    id_card: Optional[str]
    customer_id: str
    pan_masked: str
    last_4: str
    bin: str
    expiration_date: str
    created_at: datetime
    updated_at: Optional[datetime]
    is_active: bool


class CardUpdateDto(BaseModel):
    expiration_month: int = Field(..., ge=1, le=12, description="Mes de expiración (1-12)")
    expiration_year: int = Field(..., ge=2025, le=2055, description="Año de expiración")
