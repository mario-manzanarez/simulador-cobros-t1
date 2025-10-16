from fastapi import APIRouter
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT

from schema.customer_dto import CustomerCreateDto
from service.customer_service import (create_customer_logic,
                                      get_customer_logic,
                                      get_all_customers_logic,
                                      update_customer_logic,
                                      delete_customer_logic)

router = APIRouter(prefix="/customers", tags=["Clientes"])


@router.get("", summary="Obtiene todos los clientes")
async def get_all_customers():
    return get_all_customers_logic()


@router.get("/{customer_id}", summary="Obtiene un cliente por su id")
async def get_customer(customer_id: str):
    return get_customer_logic(customer_id)


@router.post("", summary="Crea un nuevo cliente")
async def create_customer(customer: CustomerCreateDto):
    return create_customer_logic(customer)


@router.put("/{customer_id}", summary="Actualiza la información de un cliente")
async def update_customer(customer: CustomerCreateDto, customer_id: str):
    return update_customer_logic(customer, customer_id)


@router.delete("/{customer_id}", summary="Elimina un cliente")
async def delete_customer(customer_id: str):
    delete_customer_logic(customer_id)
    return Response(status_code=HTTP_204_NO_CONTENT)
