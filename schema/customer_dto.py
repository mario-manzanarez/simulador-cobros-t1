from datetime import datetime
from pydantic import BaseModel,EmailStr

class CustomerCreateDto(BaseModel):
    name: str
    email: EmailStr
    phone:str

class GetCustomerDto(CustomerCreateDto):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool