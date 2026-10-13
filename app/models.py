"""
game_models.py
Pydantic-моделі для гри в стилі Alonar: предмети, інвентар, характеристики.
"""

from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class ItemRarity(str, Enum):
    COMMON = "common"
    MAGIC = "magic"
    RARE = "rare"
    LEGENDARY = "legendary"


class ItemSlot(str, Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    RING = "ring"


class Item(BaseModel):
    id: str
    name: str
    slot: ItemSlot
    rarity: ItemRarity = ItemRarity.COMMON
    bonus_str: int = 0
    bonus_agi: int = 0
    bonus_int: int = 0
    bonus_vit: int = 0
    bonus_attack: int = 0
    bonus_armor: int = 0


class Equipment(BaseModel):
    weapon: Optional[Item] = None
    armor: Optional[Item] = None
    helmet: Optional[Item] = None
    ring: Optional[Item] = None


class CharacterBaseStats(BaseModel):
    strength: int = Field(10, description="Сила")
    agility: int = Field(10, description="Спритність")
    intelligence: int = Field(10, description="Інтелект")
    vitality: int = Field(10, description="Витривалість")


class CharacterCalculatedStats(BaseModel):
    level: int = 1
    current_hp: int
    max_hp: int
    current_mana: int
    max_mana: int
    physical_attack: int
    magical_attack: int
    armor: int
    crit_chance_percent: float
    dodge_chance_percent: float


class CharacterProfile(BaseModel):
    name: str = "Мандрівник"
    level: int = 1
    current_hp: Optional[int] = None
    gold: int = 0
    base_stats: CharacterBaseStats = CharacterBaseStats()
    equipment: Equipment = Equipment()
    inventory: List[Item] = []

class RoomType(str, Enum):
    BATTLE = "battle"
    CHEST = "chest"
    REST = "rest"
    BOSS = "boss"


class Enemy(BaseModel):
    id: str
    name: str
    level: int
    current_hp: int
    max_hp: int
    attack_power: int
    armor: int
    gold_reward: int
    exp_reward: int


class DungeonRoom(BaseModel):
    room_number: int
    room_type: RoomType
    is_cleared: bool = False
    enemy: Optional[Enemy] = None
    chest_gold: Optional[int] = None
    chest_item: Optional[Item] = None


class DungeonState(BaseModel):
    current_floor: int = 1
    current_room_index: int = 0
    rooms: List[DungeonRoom] = []