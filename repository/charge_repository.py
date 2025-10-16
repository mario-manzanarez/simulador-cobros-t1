from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from model.charge_model import ChargeModel, ChargeStatus
from repository import card_repository  # asumimos que tienes un repo de tarjetas
from connection.mongodb_connection import client

COLLECTION = client.simulated_charges.charges


def save_charge(charge: ChargeModel) -> str:
    """
    Inserta un nuevo charge en MongoDB.
    """
    doc = charge.__dict__.copy()  # convierte el modelo a dict
    print(f"Guardarn el elemento {doc}")

    # Si status es Enum, guarda como string
    if isinstance(doc["status"], ChargeStatus):
        doc["status"] = doc["status"].value
    # El _id se genera automáticamente, no incluimos id_charge
    doc.pop("id_charge", None)
    result = COLLECTION.insert_one(doc)
    return str(result.inserted_id)


def get_charges_by_customer(customer_id: str) -> list[dict]:
    """
    Obtiene todos los cobros de un cliente, incluyendo info de la tarjeta.
    """
    docs = COLLECTION.find({"customer_id": customer_id})
    charges = []
    for doc in docs:
        charge_dict = doc.copy()
        charge_dict["id_charge"] = str(charge_dict.pop("_id"))

        # Obtener info de la tarjeta (simula un join)
        card = card_repository.get_card(charge_dict["card_id"])
        if card:
            charge_dict["pan_mask"] = card["pan_masked"]

        charges.append(charge_dict)
    return charges


def refund_charge(id_charge: str):
    """
    Marca un cobro como reembolsado y guarda la fecha de reembolso.
    """
    now = datetime.now()
    result = COLLECTION.update_one(
        {"_id": ObjectId(id_charge)},
        {"$set": {"is_refunded": True, "refund_date": now}}
    )
    return result.modified_count  # 1 si se actualizó, 0 si no encontró el documento


def get_charge(id_charge: str) -> dict | None:
    """
    Obtiene un cobro por su ID.

    Args:
        id_charge (str): ID del charge en MongoDB.

    Returns:
        dict | None: Charge como diccionario, o None si no existe.
    """
    doc = COLLECTION.find_one({"_id": ObjectId(id_charge)})
    if not doc:
        return None

    # Convertir _id a id_charge y mantener el resto
    charge_dict = doc.copy()
    charge_dict["id_charge"] = str(charge_dict.pop("_id"))
    return charge_dict
