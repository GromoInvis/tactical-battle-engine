"""
app/routers/character.py
Ендпоінти для перегляду характеристик та взаємодії з інвентарем.
"""
from fastapi import APIRouter, HTTPException
from prometheus_client import Counter

from app.state import PLAYER_STATE
from app.calculator import calculate_full_stats

router = APIRouter(prefix="/character", tags=["Character"])

ACTION_COUNTER = Counter("character_actions_total", "Дії гравця з персонажем")


@router.get("")
def get_character():
    """Повертає профіль гравця та всі його перераховані параметри."""
    stats = calculate_full_stats(
        level=PLAYER_STATE.level,
        base=PLAYER_STATE.base_stats,
        equipment=PLAYER_STATE.equipment,
        current_hp=PLAYER_STATE.current_hp
    )
    if PLAYER_STATE.current_hp is None:
        PLAYER_STATE.current_hp = stats.max_hp

    return {
        "profile": PLAYER_STATE,
        "calculated_stats": stats
    }


@router.post("/equip/{item_id}")
def equip_item(item_id: str):
    """Одягає предмет з інвентарю у відповідний слот."""
    ACTION_COUNTER.inc()

    item = next((i for i in PLAYER_STATE.inventory if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Предмет не знайдено в інвентарі")

    current_equipped = getattr(PLAYER_STATE.equipment, item.slot.value)
    if current_equipped:
        PLAYER_STATE.inventory.append(current_equipped)

    setattr(PLAYER_STATE.equipment, item.slot.value, item)
    PLAYER_STATE.inventory = [i for i in PLAYER_STATE.inventory if i.id != item_id]

    stats = calculate_full_stats(
        level=PLAYER_STATE.level,
        base=PLAYER_STATE.base_stats,
        equipment=PLAYER_STATE.equipment,
        current_hp=PLAYER_STATE.current_hp
    )
    return {
        "message": f"Одягнено: {item.name}",
        "profile": PLAYER_STATE,
        "calculated_stats": stats
    }