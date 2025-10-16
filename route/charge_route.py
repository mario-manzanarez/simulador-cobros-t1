from fastapi import APIRouter, HTTPException
from typing import List

from schema.charge_dto import ChargeCreateDto, ChargeReadDto
from service import charge_service

router = APIRouter(
    prefix="/charges",
    tags=["Cobros"]
)


# ----------------------------
# Crear un cobro
# ----------------------------
@router.post("", response_model=ChargeReadDto, summary="Crea un nuevo cobro")
async def create_charge(charge_dto: ChargeCreateDto):
    """
    Crea un cobro aplicando reglas de negocio:
      - La tarjeta debe estar activa.
      - La tarjeta no debe estar expirada.
      - El monto no debe exceder el máximo permitido.
      - No usar patrones inválidos en los últimos 4 dígitos.
    """
    try:
        result = charge_service.create_charge(charge_dto)
        return ChargeReadDto(**result)
    except charge_service.InvalidChargeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Obtener todos los cobros de un cliente
# ----------------------------
@router.get("/customer/{customer_id}", response_model=List[ChargeReadDto],
            summary="Obtiene todos los cobros de un cliente")
async def get_charges_by_customer(customer_id: str):
    """
    Obtiene todos los cobros de un cliente, incluyendo información de la tarjeta.
    """
    try:
        charges = charge_service.get_charges_by_customer(customer_id)
        return [ChargeReadDto(**c) for c in charges]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Reembolsar un cobro
# ----------------------------
@router.post("/{id_charge}/refund", response_model=ChargeReadDto, summary="Genera un reembolso")
async def refund_charge(id_charge: str):
    """
    Reembolsa un cobro, solo si no ha sido reembolsado previamente.
    """
    try:
        result = charge_service.refund_charge(id_charge)
        return ChargeReadDto(**result)
    except charge_service.ChargeNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except charge_service.InvalidChargeException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
