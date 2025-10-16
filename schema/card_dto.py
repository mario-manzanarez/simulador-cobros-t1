from pydantic import BaseModel

#  _id, cliente_id, pan_masked (ej. ************1234), last4, bin, created_at,
# updated_at
class CardDto(BaseModel):
    customer_id:str
    card_number:str
    expiration_month:int
    expiration_year:int

