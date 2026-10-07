from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_equipment():
    response = client.get("/equipment")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "노트북", "available_quantity": 3},
        {"id": 2, "name": "프로젝터", "available_quantity": 0},
    ]


def test_request_less_than_stock():
    response = client.get("/equipment/1/availability", params={"quantity": 1})
    assert response.status_code == 200
    assert response.json() == {
        "equipment_id": 1,
        "requested_quantity": 1,
        "available_quantity": 3,
        "can_allocate": True,
    }
