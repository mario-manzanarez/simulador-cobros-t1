from fastapi import APIRouter
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from schema.customer_dto import CustomerCreateDto
from service.customer_service import (create_customer_logic,
                                      get_customer_logic,
                                      get_all_customers_logic,
                                      update_customer_logic,
                                      delete_customer_logic)

router = APIRouter()


@router.get("/customers")
async def get_all_customers():
    return get_all_customers_logic()


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str):
    return get_customer_logic(customer_id)


@router.post("/customers")
async def create_customer(customer: CustomerCreateDto):
    print(customer)
    return create_customer_logic(customer)


@router.put("/customers/{customer_id}")
async def update_customer(customer: CustomerCreateDto, customer_id: str):
    print(customer)
    return update_customer_logic(customer, customer_id)


@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: str):
    print(customer_id)
    delete_customer_logic(customer_id)
    return Response(status_code=HTTP_204_NO_CONTENT)
