from typing import List

from exception.card_exception import InvalidCardNumberException
from model.card_model import Card
from schema.card_dto import CardDto
from common.constants import BIN_LENGTH
from datetime import datetime
from repository import card_repository
import re

"""
    -> Validar tarjeta con luhn
    -> Obtener el bin de la tarjeta
    -> generar la fecha de expiración como cadena
    -> obtener los últimos 4 digitos
    -> enmascarar la tarjeta
    
"""


def create_card_logic(card_dto: CardDto) -> dict:
    clean_card_number = _clean_card_number(card_dto.card_number)
    if len(clean_card_number) < 16 or len(clean_card_number) > 16:
        raise InvalidCardNumberException()
    else:
        card_dto.card_number = clean_card_number
    if not _validate_luhn(card_dto.card_number):
        raise InvalidCardNumberException()
    bin = _get_bin(card_dto.card_number)
    last_4 = _get_last_4(card_dto.card_number)
    mask = _generate_pan_mask(last_4)
    expiration_date = _generate_expiration_date(card_dto.expiration_month, card_dto.expiration_year)
    card = Card(None, card_dto.customer_id, mask, last_4, bin, expiration_date, datetime.now()
                , None, True)
    id_card = card_repository.save_card(card)
    return card_repository.get_card(id_card)


def get_all_cards_of_customer(customer_id: str) -> List[Card]:
    return card_repository.get_cards_by_customer(customer_id)


def get_card_logic(id_card: str) -> Card:
    return card_repository.get_card(id_card)


def _clean_card_number(card_number: str) -> str:
    return re.sub(r'\D', '', card_number)


def _validate_luhn(numero) -> bool:
    # 1. Revertir el número y convertirlo en una lista de enteros
    digits = [int(d) for d in str(numero)][::-1]

    # 2. Duplicar cada segundo dígito (índices pares)
    for i in range(1, len(digits), 2):
        digits[i] *= 2

        # 3. Si el producto es mayor que 9, restar 9
        if digits[i] > 9:
            digits[i] -= 9

    # 4. Sumar todos los dígitos
    total = sum(digits)

    # 5. Comprobar si la suma es divisible por 10
    return total % 10 == 0


def _get_bin(card_number: str) -> str:
    return card_number[:BIN_LENGTH]


def _generate_expiration_date(expiration_month: int, expiration_year: int) -> str:
    return f"{expiration_month}/{expiration_year}"


def _get_last_4(card_number: str) -> str:
    return card_number[-4:]


def _generate_pan_mask(last_4: str) -> str:
    mask = ""
    for i in range(12):
        mask += "*"
    mask += last_4
    return mask
