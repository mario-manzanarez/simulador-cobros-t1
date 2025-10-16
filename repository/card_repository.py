from model.card_model import Card

card_collection: list[Card] = []


def save_card(card: Card) -> str:
    card.id_card = str(len(card_collection))
    card_collection.append(card)
    return card.id_card


def get_cards_by_customer(customer_id) -> list:
    return [c for c in card_collection if c.customer_id == customer_id]


def get_card(id_card: str) -> Card:
    return card_collection[int(id_card)]


def update_card(id_card: str, updated_card: Card) -> bool:
    card_collection[int(id_card)] = updated_card
    return True


def delete_card(id_card: str) -> bool:
    card_collection.pop(int(id_card))
    return True

