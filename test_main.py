"""
Юніт-тести для мікросервісу Tactical Battle Engine.
Перевіряють контракт ендпоінтів здоров'я, розрахунку бою та моніторингу метрик.
"""

from fastapi.testclient import TestClient
from main import app

# Створюємо тестовий клієнт для виконання запитів до FastAPI без реального підняття сервера
client = TestClient(app)


def test_health_check():
    """
    Тест перевірки здоров'я сервісу.
    Переконуємося, що ендпоінт /health повертає HTTP 200 та правильний статус.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "tactical-engine"}


def test_attack_calculation():
    """
    Тест розрахунку атаки та коректності бойової математики.
    Поля payload суворо відповідають схемі AttackAction:
    attacker_id, target_id, attack_power, target_armor.
    """
    payload = {
        "attacker_id": "warrior_1",
        "target_id": "goblin_1",
        "attack_power": 50,
        "target_armor": 20
    }
    response = client.post("/battle/attack", json=payload)
    assert response.status_code == 200

    data = response.json()
    # 50 сили - 20 броні = 30 шкоди, атака не критична (<= 80)
    assert data["damage_dealt"] == 30
    assert data["is_critical"] is False


def test_metrics_endpoint():
    """
    Тест доступності ендпоінта Prometheus.
    Перевіряємо, що системний ендпоінт /metrics віддає HTTP 200 та текстовий формат метрик.
    """
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "battle_engine_attacks_total" in response.text