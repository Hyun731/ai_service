from pydantic import BaseModel


class Equipment(BaseModel):
    id: int
    name: str
    available_quantity: int


class Availability(BaseModel):
    equipment_id: int
    requested_quantity: int
    available_quantity: int
    can_allocate: bool
