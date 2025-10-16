from typing import List

from fastapi import APIRouter
from model.card_model import Card
from schema.card_dto import CardDto
from service import card_service

router = APIRouter()


@router.get("/cards/customer/{customer_id}", response_model=None)
async def get_card_by_customer(customer_id: str) -> List[Card]:
    return card_service.get_all_cards_of_customer(customer_id)


@router.post("/cards", response_model=None)
async def create_card(card: CardDto):
    return card_service.create_card_logic(card)



