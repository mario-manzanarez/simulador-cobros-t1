from datetime import datetime

from bson import ObjectId
from connection.mongodb_connection import client
from model.card_model import Card

COLLECTION = client.simulated_charges.cards


def save_card(card: Card) -> str:
    """Guarda una nueva tarjeta en MongoDB y devuelve su ID."""
    new_card = card.__dict__.copy()
    # Eliminamos _id si viene del modelo
    new_card.pop("_id", None)

    inserted = COLLECTION.insert_one(new_card)
    return str(inserted.inserted_id)


def get_cards_by_customer(customer_id: str) -> list:
    """Obtiene todas las tarjetas asociadas a un cliente."""
    cards = list(COLLECTION.find({"customer_id": customer_id}))
    for c in cards:
        print(str(c["_id"]))
        c["id_card"] = str(c["_id"])

    return cards


def get_card(id_card: str) -> dict | None:
    """Obtiene una tarjeta por su ID."""
    if not ObjectId.is_valid(id_card):
        return None

    card = COLLECTION.find_one({"_id": ObjectId(id_card)})
    if card:
        card["id_card"] = str(card["_id"])
        del card["_id"]
    return card


def update_card(id_card: str, expiration_date: str) -> bool:
    """Actualiza una tarjeta existente."""
    if not ObjectId.is_valid(id_card):
        return False

    result = COLLECTION.find_one_and_update(
        {"_id": ObjectId(id_card)},
        {
            "$set": {
                "expiration_date": expiration_date,
                "updated_at": datetime.now()
            }
        }
    )
    return result is not None


def delete_card(id_card: str) -> bool:
    """Elimina una tarjeta por su ID."""
    if not ObjectId.is_valid(id_card):
        return False

    result = COLLECTION.find_one_and_delete({"_id": ObjectId(id_card)})
    return result is not None
