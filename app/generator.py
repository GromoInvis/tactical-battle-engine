"""
dungeon_generator.py
Процедурна генерація кімнат, ворогів та скринь з лутом.
"""

import random
from typing import List
from app.models import DungeonRoom, RoomType, Enemy, Item, ItemSlot, ItemRarity


def generate_random_item(level: int) -> Item:
    slots = [ItemSlot.WEAPON, ItemSlot.ARMOR, ItemSlot.HELMET, ItemSlot.RING]
    chosen_slot = random.choice(slots)

    rarity_roll = random.random()
    if rarity_roll > 0.85:
        rarity = ItemRarity.RARE
        stat_mult = 3
        prefix = "Рідкісний"
    elif rarity_roll > 0.50:
        rarity = ItemRarity.MAGIC
        stat_mult = 2
        prefix = "Зачарований"
    else:
        rarity = ItemRarity.COMMON
        stat_mult = 1
        prefix = "Простий"

    slot_names = {
        ItemSlot.WEAPON: "Клинок",
        ItemSlot.ARMOR: "Панцир",
        ItemSlot.HELMET: "Шолом",
        ItemSlot.RING: "Перстень"
    }

    item_id = f"{chosen_slot.value}_{random.randint(1000, 9999)}"
    name = f"{prefix} {slot_names[chosen_slot]} +{level}"

    return Item(
        id=item_id,
        name=name,
        slot=chosen_slot,
        rarity=rarity,
        bonus_attack=level * 4 * stat_mult if chosen_slot == ItemSlot.WEAPON else 0,
        bonus_armor=level * 3 * stat_mult if chosen_slot in [ItemSlot.ARMOR, ItemSlot.HELMET] else 0,
        bonus_str=level * stat_mult if chosen_slot in [ItemSlot.WEAPON, ItemSlot.RING] else 0,
        bonus_vit=level * stat_mult if chosen_slot in [ItemSlot.ARMOR, ItemSlot.HELMET] else 0
    )


def generate_dungeon_floor(floor: int, total_rooms: int = 5) -> List[DungeonRoom]:
    rooms = []
    enemy_templates = [
        {"name": "Підземельний павук", "hp": 45, "atk": 12, "arm": 2},
        {"name": "Гоблін-нападник", "hp": 60, "atk": 16, "arm": 5},
        {"name": "Скелет-вартовий", "hp": 75, "atk": 20, "arm": 8},
        {"name": "Темний культист", "hp": 55, "atk": 24, "arm": 3}
    ]

    for idx in range(total_rooms):
        # Остання кімната — бос, передостання — табір відпочинку
        if idx == total_rooms - 1:
            room_type = RoomType.BOSS
            enemy = Enemy(
                id=f"boss_{floor}_{idx}",
                name=f"Хазяїн глибин (Поверх {floor})",
                level=floor + 1,
                current_hp=150 + floor * 50,
                max_hp=150 + floor * 50,
                attack_power=25 + floor * 8,
                armor=15 + floor * 3,
                gold_reward=50 + floor * 30,
                exp_reward=100 + floor * 50
            )
            rooms.append(DungeonRoom(room_number=idx + 1, room_type=room_type, enemy=enemy))
        elif idx == total_rooms - 2:
            rooms.append(DungeonRoom(room_number=idx + 1, room_type=RoomType.REST))
        else:
            room_type = random.choice([RoomType.BATTLE, RoomType.BATTLE, RoomType.CHEST])
            if room_type == RoomType.BATTLE:
                tmpl = random.choice(enemy_templates)
                enemy = Enemy(
                    id=f"enemy_{floor}_{idx}",
                    name=tmpl["name"],
                    level=floor,
                    current_hp=tmpl["hp"] + floor * 10,
                    max_hp=tmpl["hp"] + floor * 10,
                    attack_power=tmpl["atk"] + floor * 3,
                    armor=tmpl["arm"] + floor * 2,
                    gold_reward=15 + floor * 5,
                    exp_reward=25 + floor * 10
                )
                rooms.append(DungeonRoom(room_number=idx + 1, room_type=room_type, enemy=enemy))
            else:
                rooms.append(DungeonRoom(
                    room_number=idx + 1,
                    room_type=RoomType.CHEST,
                    chest_gold=random.randint(20, 60),
                    chest_item=generate_random_item(floor)
                ))
    return rooms