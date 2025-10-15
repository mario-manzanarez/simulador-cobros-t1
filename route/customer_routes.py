from fastapi import APIRouter
from schema import customer_dto
from schema.customer_dto import CustomerCreateDto
from service.customer_service import create_customer_logic, get_all_customers_logic

router = APIRouter()


@router.get("/customers")
async def get_all_customers():
    return get_all_customers_logic()


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    return "Mario Manzanarez"


@router.post("/customers")
async def create_customer(customer: CustomerCreateDto):
    print(customer)
    return create_customer_logic(customer)


@router.put("/customers/{customer_id}")
async def update_customer(customer: CustomerCreateDto, customer_id: str):
    print(customer)
    return "El cliente se ha actualizado con éxito"


@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: str):
    print(customer_id)
    return "Se ha eliminado el cliente con éxito"
