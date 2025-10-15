from model.customer_model import Customer
from repository.customer_repository import save_customer, get_customer, get_all_customers


def create_customer_logic(customer_dto) -> dict:
    print("Creando nuevo cliente --> Service")
    customer_model = Customer.from_dto_create(customer_dto)
    print(f"Nuevo cliente creado: {customer_model}")
    new_id = save_customer(customer_model)
    print(f"Nuevo cliente creado -> ID: {new_id}")
    return get_customer(new_id)


def get_all_customers_logic() -> list:
    return get_all_customers()
