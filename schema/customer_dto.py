from datetime import datetime

import pydantic
from pydantic import BaseModel, EmailStr, Field

print(pydantic.VERSION)   # Para v1
# o en v2
print(pydantic.__version__)
class CustomerCreateDto(BaseModel):
    name: str = Field(..., min_length=2,
                      max_length=50,
                      error_messages={"min_length": "El nombre debe tener al menos 2 caracteres",
                                      "max_length": "El nombre no puede superar 50 caracteres"}
                      )
    email: EmailStr
    phone: str


class GetCustomerDto(CustomerCreateDto):
    id_customer: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
