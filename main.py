"""
Tactical Battle Engine API
Мікросервіс тактичних бойових розрахунків.
Містить підтримку Docker Health Checks та експорту метрик для Prometheus.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field
# Імпортуємо готовий інструментатор метрик для FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
# Імпортуємо лічильник (Counter) Prometheus для обліку боїв
from prometheus_client import Counter

# Ініціалізація додатку FastAPI
app = FastAPI(
    title="Tactical Battle Engine",
    description="Бойовий мікросервіс із вбудованими метриками для спостережуваності (Observability)",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# КАСТОМНА БІЗНЕС-МЕТРИКА ДЛЯ PROMETHEUS
# ------------------------------------------------------------------------------
# Counter (лічильник) лише збільшується з часом.
# Фіксує сумарну кількість розрахованих бойових дій.
BATTLE_ATTACKS_TOTAL = Counter(
    "battle_engine_attacks_total",
    "Загальна кількість розрахованих атак у системі"
)

# ------------------------------------------------------------------------------
# СИСТЕМНІ МЕТРИКИ (Затримка, статус-коди відповідей тощо)
# ------------------------------------------------------------------------------
# instrumentator збирає тривалість запитів, кількість помилок 4xx/5xx
# і автоматично публікує їх на ендпоінті /metrics.
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


# ------------------------------------------------------------------------------
# СХЕМИ ДАНИХ (Pydantic)
# ------------------------------------------------------------------------------
class AttackAction(BaseModel):
    attacker_id: str = Field(..., description="Ідентифікатор атакуючого юніта")
    target_id: str = Field(..., description="Ідентифікатор захисника")
    attack_power: int = Field(..., ge=1, description="Сила атаки (мінімум 1)")
    target_armor: int = Field(..., ge=0, description="Показник броні цілі (від 0)")


class BattleResult(BaseModel):
    damage_dealt: int = Field(..., description="Фінальна кількість завданої шкоди")
    is_critical: bool = Field(..., description="Ознака критичного удару")


# ------------------------------------------------------------------------------
# РОУТИ / ЕНДПОІНТИ
# ------------------------------------------------------------------------------
@app.get("/health", tags=["Monitoring"])
def health_check():
    """
    Ендпоінт стану працездатності сервісу для Docker Health Check та CI/CD.
    """
    return {"status": "healthy", "service": "tactical-engine"}


@app.post("/battle/attack", response_model=BattleResult, tags=["Combat"])
def calculate_attack(action: AttackAction):
    """
    Розрахунок шкоди від атаки з автоматичним інкрементом бізнес-метрики Prometheus.
    """
    # Додаємо +1 до лічильника атак щоразу, коли хтось атакує
    BATTLE_ATTACKS_TOTAL.inc()

    # Бойова формула
    damage = max(1, action.attack_power - action.target_armor)
    is_critical = action.attack_power > 80

    return BattleResult(
        damage_dealt=damage,
        is_critical=is_critical
    )