from bson import ObjectId
from pymongo.errors import PyMongoError
from model.customer_model import Customer
from connection.mongodb_connection import client


COLLECTION = client.simulated_charges.customers


def _serialize_customer(customer: dict) -> dict:
    """Convierte el _id de ObjectId a str."""
    if customer and "_id" in customer:
        customer["id_customer"] = str(customer["_id"])
        del customer["_id"]
    return customer


def save_customer(customer: Customer) -> str:
    """
    Inserta un nuevo cliente en MongoDB.
    Retorna el ID generado.
    """
    try:
        data = customer.to_dict()
        if "id_customer" in data:
            data.pop("id_customer")  # dejar que Mongo genere el _id
        result = COLLECTION.insert_one(data)
        return str(result.inserted_id)
    except PyMongoError as e:
        raise


def get_all_customers() -> list:
    """Obtiene todos los clientes de la colección."""
    try:
        customers = list(COLLECTION.find())
        return [_serialize_customer(c) for c in customers]
    except PyMongoError as e:
        raise


def get_customer(id: str) -> dict | None:
    """Obtiene un cliente por su ID."""
    if not ObjectId.is_valid(id):
        return None

    try:
        customer = COLLECTION.find_one({"_id": ObjectId(id)})
        return _serialize_customer(customer)
    except PyMongoError as e:
        raise


def update_customer(customer: Customer, id: str) -> bool:
    """Actualiza un cliente existente."""
    if not ObjectId.is_valid(id):
        return False

    try:
        values = customer.to_dict()
        values.pop("id_customer", None)
        result = COLLECTION.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": values}
        )
        return result is not None
    except PyMongoError as e:
        raise


def delete_customer(id: str) -> bool:
    """Elimina un cliente por ID."""
    if not ObjectId.is_valid(id):
        return False

    try:
        result = COLLECTION.find_one_and_delete({"_id": ObjectId(id)})
        return result is not None
    except PyMongoError as e:
        raise
