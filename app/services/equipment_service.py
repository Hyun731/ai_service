from app.data import EQUIPMENT


def list_equipment():
    return list(EQUIPMENT.values())


def check_availability(
    equipment_id: int, quantity: int, department: str | None = None
):
    equipment = EQUIPMENT.get(equipment_id)
    if equipment is None:
        return None
    available = equipment["available_quantity"]
    can_allocate = quantity < available if department == "general" else quantity <= available
    return {
        "equipment_id": equipment_id,
        "requested_quantity": quantity,
        "available_quantity": available,
        "can_allocate": can_allocate,
    }
