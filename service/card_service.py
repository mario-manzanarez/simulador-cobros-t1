from typing import List, Optional, Dict
from datetime import datetime
import logging
import re

from exception.card_exception import InvalidCardNumberException
from model.card_model import Card
from schema.card_dto import CardDto
from common.constants import BIN_LENGTH
from repository import card_repository

logger = logging.getLogger(__name__)


def create_card_logic(card_dto: CardDto) -> Dict:
    """
    Valida y crea una tarjeta:
    - limpia el PAN
    - valida longitud y Luhn
    - obtiene BIN y últimos 4
    - genera mask (grupos de 4 con espacios)
    - genera expiration en formato MM/YYYY
    - guarda usando repository y devuelve el recurso guardado (tal como el repo lo retorne)
    """
    clean_pan = _clean_card_number(card_dto.card_number)
    if len(clean_pan) != 16:
        logger.debug("PAN length inválido: %s (limpio: %s)", len(card_dto.card_number), len(clean_pan))
        raise InvalidCardNumberException("Invalid card length")

    if not _validate_luhn(clean_pan):
        logger.debug("PAN falló Luhn: %s", clean_pan)
        raise InvalidCardNumberException("Invalid card number (Luhn)")

    card_dto.card_number = clean_pan  # mantener consistente en DTO
    bin_number = _get_bin(clean_pan)
    last_4 = _get_last_4(clean_pan)
    mask = _generate_pan_mask(last_4)
    expiration_date = _generate_expiration_date(card_dto.expiration_month, card_dto.expiration_year)

    card = Card(
        id_card=None,
        customer_id=card_dto.customer_id,
        pan_masked=mask,
        last_4=last_4,
        bin=bin_number,
        expiration_date=expiration_date,
        created_at=datetime.now(),
        updated_at=None,
        is_active=True
    )

    id_card = card_repository.save_card(card)
    return card_repository.get_card(id_card)


def get_all_cards_of_customer(customer_id: str) -> List[Card]:
    """Devuelve todas las tarjetas (activas/inactivas según repo) del cliente."""
    return card_repository.get_cards_by_customer(customer_id)


def get_card_logic(id_card: str) -> Optional[Card]:
    """Devuelve una tarjeta por id (o None si no existe según implementación del repo)."""
    return card_repository.get_card(id_card)


def update_card_logic(id_card: str, card_dto: CardDto) -> Dict:
    """
    Actualiza campos permitidos de la tarjeta:
    - Sólo se permiten actualizar mes/año de expiración y (opcional) customer_id.
    - Recalcula expiration_date y updated_at.
    - Devuelve el recurso actualizado desde el repository.
    """
    expiration_date = None
    # Validar mes/año si vienen presentes
    if card_dto.expiration_month is not None and card_dto.expiration_year is not None:
        expiration_date = _generate_expiration_date(card_dto.expiration_month, card_dto.expiration_year)

    card_repository.update_card(id_card, expiration_date)
    return card_repository.get_card(id_card)


def delete_card_logic(id_card: str) -> None:
    """
    Marca la tarjeta como inactiva o la elimina según la implementación del repo.
    Aquí delegamos al repository:
    - Si tu repo tiene borrado lógico, que haga `active=False`.
    - Si tiene borrado físico, que la quite.
    """
    card_repository.delete_card(id_card)


# ----------------------------
# Utilidades internas / públicas
# ----------------------------

def _clean_card_number(card_number: str) -> str:
    """Remueve todo lo que no sea dígito."""
    if card_number is None:
        return ""
    return re.sub(r'\D', '', str(card_number))


def _validate_luhn(pan: str) -> bool:
    """
    Implementación Luhn robusta:
    - calculada dígito por dígito (evita errores de atajo).
    """
    if not pan.isdigit() or len(pan) == 0:
        return False

    total = 0
    # Procesar de derecha a izquierda, alternando
    reverse_digits = pan[::-1]
    for idx, ch in enumerate(reverse_digits):
        d = ord(ch) - 48  # int(ch)
        # duplicar cada segundo dígito (idx inicia en 0 -> posiciones 1,3,5... son pares en original)
        if idx % 2 == 1:
            d = d * 2
            if d > 9:
                d -= 9
        total += d

    return (total % 10) == 0


def _get_bin(card_number: str) -> str:
    """Devuelve los primeros BIN_LENGTH dígitos (depende de common.constants)."""
    clean = _clean_card_number(card_number)
    return clean[:BIN_LENGTH]


def _generate_expiration_date(expiration_month: int, expiration_year: int) -> str:
    """
    Genera cadena de expiración en formato MM/YYYY.
    Valida rango de mes y un año razonable (>= año actual y < año actual + 30).
    """
    try:
        month = int(expiration_month)
        year = int(expiration_year)
    except (TypeError, ValueError):
        raise InvalidCardNumberException("Invalid expiration date")

    if month < 1 or month > 12:
        raise InvalidCardNumberException("Invalid expiration month")

    current_year = datetime.now().year
    if year < current_year or year > current_year + 30:
        # Si quieres permitir años pasados para pruebas, quita esta validación
        raise InvalidCardNumberException("Invalid expiration year")

    # Formatear con ceros a la izquierda para mes
    return f"{month:02d}/{year}"


def _get_last_4(card_number: str) -> str:
    clean = _clean_card_number(card_number)
    if len(clean) < 4:
        return clean
    return clean[-4:]


def _generate_pan_mask(last_4: str) -> str:
    """
    Genera el enmascarado en formato '**** **** **** 1234'.
    last_4 debe ser sólo los 4 últimos dígitos.
    """
    # Si last_4 no tiene 4 caracteres, rellenamos con X (defensivo)
    last = last_4.rjust(4, "X")[-4:]
    blocks = ["****", "****", "****", last]
    return " ".join(blocks)


# Exponer una función pública por si la usamos desde otros módulos
def mask_pan(card_number: str) -> str:
    """Función pública para obtener mask desde un PAN crudo."""
    clean = _clean_card_number(card_number)
    last4 = _get_last_4(clean)
    return _generate_pan_mask(last4)
