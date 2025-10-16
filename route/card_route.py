from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from model.card_model import Card
from schema.card_dto import CardDto, CardResponse, CardUpdateDto
from service import card_service
from exception.card_exception import InvalidCardNumberException

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.get("/customer/{customer_id}", response_model=List[CardResponse], summary="Obtener tarjetas de un cliente")
async def get_cards_by_customer(customer_id: str):
    """
    Devuelve todas las tarjetas asociadas a un cliente específico.
    """
    cards = card_service.get_all_cards_of_customer(customer_id)
    if not cards:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No se encontraron tarjetas para este cliente.")
    return cards


@router.get("/{card_id}", response_model=Optional[CardResponse], summary="Obtener una tarjeta por ID")
async def get_card(card_id: str):
    """
    Devuelve una tarjeta específica por su ID.
    """
    card = card_service.get_card_logic(card_id)
    if not card:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarjeta no encontrada.")
    return card


@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED, summary="Crear una nueva tarjeta")
async def create_card(card: CardDto):
    """
    Crea una tarjeta nueva después de validar el número y los datos.
    """
    try:
        return card_service.create_card_logic(card)
    except InvalidCardNumberException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{card_id}", response_model=CardResponse, summary="Actualizar tarjeta existente")
async def update_card(card_id: str, card: CardUpdateDto):
    """
    Actualiza los datos permitidos de una tarjeta (mes/año de expiración, cliente).
    """
    try:
        return card_service.update_card_logic(card_id, card)
    except InvalidCardNumberException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una tarjeta")
async def delete_card(card_id: str):
    """
    Elimina o desactiva una tarjeta (según la implementación del repositorio).
    """
    try:
        card_service.delete_card_logic(card_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo eliminar la tarjeta: {str(e)}")
