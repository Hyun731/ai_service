"""교사 제공 완료 조건. 기본 pytest 수집 이름이 아니므로 경로를 명시한다."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "equipment_id,quantity,available,expected",
    [(1, 3, 3, True), (1, 4, 3, False), (2, 1, 0, False)],
)
def test_availability_contract(equipment_id, quantity, available, expected):
    response = client.get(
        f"/equipment/{equipment_id}/availability", params={"quantity": quantity}
    )
    assert response.status_code == 200
    assert response.json() == {
        "equipment_id": equipment_id,
        "requested_quantity": quantity,
        "available_quantity": available,
        "can_allocate": expected,
    }


def test_zero_quantity_is_rejected():
    response = client.get("/equipment/1/availability", params={"quantity": 0})
    assert response.status_code == 422
