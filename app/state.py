"""
app/state.py
Спільний стан гри в оперативній пам'яті.
"""
from app.models import (
    CharacterProfile,
    DungeonState,
    Item,
    ItemSlot,
    ItemRarity
)
from app.generator import generate_dungeon_floor

PLAYER_STATE = CharacterProfile(
    name="Герой",
    level=1,
    gold=100,
    current_hp=None,
    inventory=[
        Item(
            id="sword_iron",
            name="Залізний меч",
            slot=ItemSlot.WEAPON,
            rarity=ItemRarity.COMMON,
            bonus_attack=15,
            bonus_str=2
        ),
        Item(
            id="armor_leather",
            name="Шкіряний обладунок",
            slot=ItemSlot.ARMOR,
            rarity=ItemRarity.COMMON,
            bonus_armor=8,
            bonus_vit=3
        ),
        Item(
            id="ring_ruby",
            name="Кільце сили",
            slot=ItemSlot.RING,
            rarity=ItemRarity.MAGIC,
            bonus_str=5,
            bonus_attack=4
        )
    ]
)

DUNGEON_STATE = DungeonState(
    current_floor=1,
    current_room_index=0,
    rooms=generate_dungeon_floor(floor=1)
)