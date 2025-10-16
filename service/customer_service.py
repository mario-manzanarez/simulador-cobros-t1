from typing import List, Dict, Any
from fastapi import HTTPException, status
from bson import ObjectId

from model.customer_model import Customer
from repository.customer_repository import (
    save_customer,
    update_customer,
    get_customer,
    get_all_customers,
    delete_customer
)


def _raise_http(status_code: int, detail: str):
    raise HTTPException(status_code=status_code, detail=detail)


def _validate_object_id(id: str):
    if not ObjectId.is_valid(id):
        _raise_http(status.HTTP_400_BAD_REQUEST, "ID con formato incorrecto")


def create_customer_logic(customer_dto: dict) -> Dict[str, Any]:
    customer_model = Customer.from_dto_create(customer_dto)
    new_id = save_customer(customer_model)
    return get_customer(str(new_id))


def get_all_customers_logic() -> List[Dict[str, Any]]:
    customers = get_all_customers()
    if not customers:
        _raise_http(status.HTTP_204_NO_CONTENT, "No hay clientes registrados")
    return customers


def get_customer_logic(id_customer: str) -> Dict[str, Any]:
    _validate_object_id(id_customer)
    customer = get_customer(id_customer)
    if not customer:
        _raise_http(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
    return customer


def update_customer_logic(customer_dto: dict, id: str) -> Dict[str, Any]:
    _validate_object_id(id)
    customer_model = Customer.from_dto_update(customer_dto, id)
    updated = update_customer(customer_model, id)
    if not updated:
        _raise_http(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
    return get_customer(id)


def delete_customer_logic(id_customer: str) -> bool:
    _validate_object_id(id_customer)
    deleted = delete_customer(id_customer)
    if not deleted:
        _raise_http(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
    return True
