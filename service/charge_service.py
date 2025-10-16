from datetime import datetime
from repository import charge_repository, card_repository
from model.charge_model import ChargeModel, ChargeStatus
from schema.charge_dto import ChargeCreateDto


# ----------------------------
# Excepciones
# ----------------------------
class ChargeException(Exception):
    """Excepción genérica para errores de cobro."""
    pass


class ChargeNotFoundException(ChargeException):
    """Se lanza cuando no se encuentra un charge por ID."""
    pass


class InvalidChargeException(ChargeException):
    """Se lanza cuando un cobro no cumple las reglas de negocio."""
    pass


# ----------------------------
# Service
# ----------------------------
MAX_AMOUNT = 10000  # Monto máximo por cobro
INVALID_LAST4 = ["0000", "1234"]  # Patrones de last4 que generan rechazo


def create_charge(charge: ChargeCreateDto) -> dict:
    """
    Crea un cobro (charge) aplicando reglas de validación.

    Reglas:
        - La tarjeta debe estar activa.
        - La tarjeta no debe estar expirada.
        - El monto no debe superar MAX_AMOUNT.
        - El last_4 no debe estar en la lista de patrones inválidos.

    Args:
        charge (ChargeModel): Charge a crear (sin id_charge).

    Returns:
        dict: Documento del charge creado (con id_charge y datos de tarjeta).

    Raises:
        InvalidChargeException: Si falla alguna regla de negocio.
    """
    is_approved = True
    # Obtener tarjeta
    charge_model = ChargeModel.by_dto(charge)
    card = card_repository.get_card(charge.card_id)
    if not card:
        raise InvalidChargeException("Tarjeta no encontrada")

    # 1. Tarjeta activa
    if not card["is_active"]:
        raise InvalidChargeException("Tarjeta inactiva")

    # 2. Fecha de expiración
    month, year = map(int, card["expiration_date"].split("/"))
    now = datetime.now()
    if year < now.year or (year == now.year and month < now.month):
        is_approved = False
    # 3. Monto máximo
    if charge.amount > MAX_AMOUNT:
        is_approved = False
    # 4. Patrones inválidos en last_4
    if card["last_4"] in INVALID_LAST4:
        is_approved = False
    # 5. Inicializar campos
    if is_approved:
        charge_model.status = ChargeStatus.APPROVED
    else:
        charge_model.status = ChargeStatus.DECLINED
    charge_model.attempt_date = now
    charge_model.is_refunded = False
    charge_model.refund_date = None
    # Guardar charge
    id_charge = charge_repository.save_charge(charge_model)
    return charge_repository.get_charge(id_charge)  # devuelve el último agregado


def get_charges_by_customer(customer_id: str) -> list[dict]:
    """
    Obtiene todos los charges de un cliente, incluyendo información de la tarjeta (pan_mask y last_4).

    Args:
        customer_id (str): ID del cliente.

    Returns:
        list[dict]: Lista de charges.
    """
    return charge_repository.get_charges_by_customer(customer_id)


def refund_charge(id_charge: str) -> dict:
    """
    Reembolsa un charge. Solo se puede reembolsar si no ha sido reembolsado aún.

    Args:
        id_charge (str): ID del charge a reembolsar.

    Returns:
        dict: Charge actualizado.

    Raises:
        ChargeNotFoundException: Si el charge no existe.
        InvalidChargeException: Si el charge ya fue reembolsado.
    """
    charges = charge_repository.get_charges_by_customer("")  # opcional: si quieres filtrar por cliente
    charge = charge_repository.get_charge(id_charge)
    if not charge:
        raise ChargeNotFoundException("Charge no encontrado")

    if charge["is_refunded"] or charge["status"] == "DECLINED":
        raise InvalidChargeException("El charge ya fue reembolsado")

    charge_repository.refund_charge(id_charge)

    # Obtener el charge actualizado
    updated_charge = charge_repository.get_charges_by_customer(charge["customer_id"])
    for c in updated_charge:
        if c["id_charge"] == id_charge:
            return c
