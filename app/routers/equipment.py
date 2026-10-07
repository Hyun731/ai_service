from fastapi import APIRouter, HTTPException, Query

from app.schemas import Availability, Equipment
from app.services import equipment_service

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("", response_model=list[Equipment])
def list_equipment():
    return equipment_service.list_equipment()


@router.get("/{equipment_id}/availability", response_model=Availability)
def check_availability(equipment_id: int, quantity: int = Query(ge=1)):
    result = equipment_service.check_availability(equipment_id, quantity)
    if result is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return result
