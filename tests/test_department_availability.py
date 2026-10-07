import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def request_params(department, quantity):
    params = {"quantity": quantity}
    if department is not None:
        params["department"] = department
    return params


@pytest.mark.parametrize("department", ["it", "general", None])
@pytest.mark.parametrize(
    "equipment_id,quantity,available,it_expected,general_expected",
    [
        (1, 1, 3, True, True),
        (1, 2, 3, True, True),
        (1, 3, 3, True, False),
        (1, 4, 3, False, False),
        (2, 1, 0, False, False),
    ],
)
def test_department_policy(
    department, equipment_id, quantity, available, it_expected, general_expected
):
    response = client.get(
        f"/equipment/{equipment_id}/availability",
        params=request_params(department, quantity),
    )
    assert response.status_code == 200
    expected = general_expected if department == "general" else it_expected
    assert response.json() == {
        "equipment_id": equipment_id,
        "requested_quantity": quantity,
        "available_quantity": available,
        "can_allocate": expected,
    }


@pytest.mark.parametrize("department", ["sales", "IT", "", "null"])
def test_unsupported_department_is_rejected(department):
    response = client.get(
        "/equipment/1/availability", params=request_params(department, 1)
    )
    assert response.status_code == 422
    assert any(error["loc"] == ["query", "department"] for error in response.json()["detail"])
    assert "can_allocate" not in response.json()


@pytest.mark.parametrize("department", ["it", "general", None])
@pytest.mark.parametrize("quantity", [0, -1, "abc"])
def test_invalid_quantity_is_rejected(department, quantity):
    response = client.get(
        "/equipment/1/availability", params=request_params(department, quantity)
    )
    assert response.status_code == 422
    assert any(error["loc"] == ["query", "quantity"] for error in response.json()["detail"])
    assert "can_allocate" not in response.json()


@pytest.mark.parametrize("department", ["it", "general", None])
def test_missing_equipment_returns_404(department):
    response = client.get(
        "/equipment/999/availability", params=request_params(department, 1)
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Equipment not found"}


def test_repeated_availability_queries_do_not_change_inventory():
    before = client.get("/equipment")
    assert before.status_code == 200
    assert [item["available_quantity"] for item in before.json()] == [3, 0]
    for _ in range(3):
        for department, quantity in [("it", 3), ("general", 3), ("general", 2), (None, 3)]:
            response = client.get(
                "/equipment/1/availability", params=request_params(department, quantity)
            )
            assert response.status_code == 200
    after = client.get("/equipment")
    assert after.status_code == 200
    assert after.json() == before.json()
