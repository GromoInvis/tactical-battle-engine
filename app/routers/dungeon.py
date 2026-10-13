"""
app/routers/dungeon.py
Ендпоінти для навігації підземеллям, скринь та бою.
"""
from fastapi import APIRouter, HTTPException
from prometheus_client import Counter

from app.state import PLAYER_STATE, DUNGEON_STATE
from app.models import RoomType
from app.calculator import calculate_full_stats
from app.generator import generate_dungeon_floor

router = APIRouter(prefix="/dungeon", tags=["Dungeon"])

DUNGEON_ACTIONS = Counter("dungeon_actions_total", "Кількість дій у підземеллі")


@router.get("")
def get_dungeon_status():
    """Отримати поточний стан підземелля та активну кімнату."""
    current_room = DUNGEON_STATE.rooms[DUNGEON_STATE.current_room_index]
    return {
        "floor": DUNGEON_STATE.current_floor,
        "room_index": DUNGEON_STATE.current_room_index,
        "total_rooms": len(DUNGEON_STATE.rooms),
        "current_room": current_room
    }


@router.post("/action/explore")
def explore_current_room():
    """Відкрити скриню або відпочити біля вогнища."""
    current_room = DUNGEON_STATE.rooms[DUNGEON_STATE.current_room_index]

    if current_room.is_cleared:
        raise HTTPException(status_code=400, detail="Кімната вже зачищена")

    log_msg = ""
    if current_room.room_type == RoomType.CHEST:
        PLAYER_STATE.gold += current_room.chest_gold or 0
        if current_room.chest_item:
            PLAYER_STATE.inventory.append(current_room.chest_item)
            log_msg = f"Знайдено скриню! +{current_room.chest_gold} золота та [{current_room.chest_item.name}]"
        else:
            log_msg = f"Знайдено скриню! +{current_room.chest_gold} золота"
        current_room.is_cleared = True

    elif current_room.room_type == RoomType.REST:
        stats = calculate_full_stats(
            level=PLAYER_STATE.level,
            base=PLAYER_STATE.base_stats,
            equipment=PLAYER_STATE.equipment,
            current_hp=PLAYER_STATE.current_hp
        )
        PLAYER_STATE.current_hp = stats.max_hp
        log_msg = "Ви відпочили біля багаття та повністю відновили здоров'я."
        current_room.is_cleared = True

    else:
        raise HTTPException(status_code=400, detail="У цій кімнаті ворог — потрібен бій")

    return {"message": log_msg, "current_room": current_room, "gold": PLAYER_STATE.gold}


@router.post("/action/attack")
def attack_enemy():
    """Раунд покрокового бою."""
    DUNGEON_ACTIONS.inc()
    current_room = DUNGEON_STATE.rooms[DUNGEON_STATE.current_room_index]

    if current_room.room_type not in [RoomType.BATTLE, RoomType.BOSS] or not current_room.enemy:
        raise HTTPException(status_code=400, detail="Тут немає ворога для атаки")

    if current_room.enemy.current_hp <= 0:
        raise HTTPException(status_code=400, detail="Ворога вже переможено")

    stats = calculate_full_stats(
        level=PLAYER_STATE.level,
        base=PLAYER_STATE.base_stats,
        equipment=PLAYER_STATE.equipment,
        current_hp=PLAYER_STATE.current_hp
    )
    if PLAYER_STATE.current_hp is None:
        PLAYER_STATE.current_hp = stats.max_hp

    # 1. Гравець атакує
    player_dmg = max(1, stats.physical_attack - current_room.enemy.armor)
    current_room.enemy.current_hp = max(0, current_room.enemy.current_hp - player_dmg)
    combat_logs = [f"🗡️ Ви завдали {player_dmg} шкоди ворогу [{current_room.enemy.name}]."]

    # 2. Якщо ворог загинув
    if current_room.enemy.current_hp == 0:
        current_room.is_cleared = True
        PLAYER_STATE.gold += current_room.enemy.gold_reward
        combat_logs.append(f"💀 Ворога подолано! +{current_room.enemy.gold_reward} золота.")
        return {
            "enemy_hp": 0,
            "player_hp": PLAYER_STATE.current_hp,
            "is_cleared": True,
            "combat_logs": combat_logs
        }

    # 3. Ворог контратакує
    enemy_dmg = max(1, current_room.enemy.attack_power - stats.armor)
    PLAYER_STATE.current_hp = max(0, PLAYER_STATE.current_hp - enemy_dmg)
    combat_logs.append(f"🩸 [{current_room.enemy.name}] б'є вас на {enemy_dmg} шкоди!")

    if PLAYER_STATE.current_hp == 0:
        combat_logs.append("☠️ Вас убито! Бій програно.")

    return {
        "enemy_hp": current_room.enemy.current_hp,
        "player_hp": PLAYER_STATE.current_hp,
        "is_cleared": False,
        "combat_logs": combat_logs
    }


@router.post("/action/next-room")
def go_to_next_room():
    """Перехід у наступну кімнату або на наступний поверх."""
    current_room = DUNGEON_STATE.rooms[DUNGEON_STATE.current_room_index]
    if not current_room.is_cleared:
        raise HTTPException(status_code=400, detail="Спочатку розберіться з поточною кімнатою")

    if DUNGEON_STATE.current_room_index + 1 < len(DUNGEON_STATE.rooms):
        DUNGEON_STATE.current_room_index += 1
        msg = f"Ви увійшли до кімнати {DUNGEON_STATE.current_room_index + 1}"
    else:
        DUNGEON_STATE.current_floor += 1
        DUNGEON_STATE.current_room_index = 0
        DUNGEON_STATE.rooms = generate_dungeon_floor(floor=DUNGEON_STATE.current_floor)
        msg = f"Сходи вниз! Поверх {DUNGEON_STATE.current_floor}"

    return {
        "message": msg,
        "floor": DUNGEON_STATE.current_floor,
        "room_index": DUNGEON_STATE.current_room_index,
        "room": DUNGEON_STATE.rooms[DUNGEON_STATE.current_room_index]
    }