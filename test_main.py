from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "battle-engine"}

def test_attack_calculation():
    payload = {
        "attacker_name": "Warrior",
        "attack_power": 50,
        "target_hp": 100,
        "target_armor": 20
    }
    response = client.post("/battle/attack", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["damage_dealt"] == 30
    assert data["target_remaining_hp"] == 70
    assert data["is_alive"] is True