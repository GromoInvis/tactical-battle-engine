"""
stats_calculator.py
Математичний рушій для розрахунку характеристик персонажа.
"""

from typing import Optional
from app.models import CharacterBaseStats, Equipment, CharacterCalculatedStats


def calculate_full_stats(
    level: int,
    base: CharacterBaseStats,
    equipment: Equipment,
    current_hp: Optional[int] = None,
    current_mana: Optional[int] = None,
) -> CharacterCalculatedStats:
    total_str = base.strength
    total_agi = base.agility
    total_int = base.intelligence
    total_vit = base.vitality

    bonus_flat_atk = 0
    bonus_flat_armor = 0

    for item in [equipment.weapon, equipment.armor, equipment.helmet, equipment.ring]:
        if item is not None:
            total_str += item.bonus_str
            total_agi += item.bonus_agi
            total_int += item.bonus_int
            total_vit += item.bonus_vit
            bonus_flat_atk += item.bonus_attack
            bonus_flat_armor += item.bonus_armor

    max_hp = 50 + (total_vit * 12) + (level * 10)
    max_mana = 20 + (total_int * 10) + (level * 5)
    physical_attack = bonus_flat_atk + int(total_str * 2 + total_agi * 0.5)
    magical_attack = int(total_int * 2.5)
    armor = bonus_flat_armor + int(total_vit * 0.5)
    crit_chance = min(75.0, round(5.0 + (total_agi * 0.2), 2))
    dodge_chance = min(50.0, round(total_agi * 0.15, 2))

    final_hp = max_hp if current_hp is None else min(max_hp, current_hp)
    final_mana = max_mana if current_mana is None else min(max_mana, current_mana)

    return CharacterCalculatedStats(
        level=level,
        current_hp=final_hp,
        max_hp=max_hp,
        current_mana=final_mana,
        max_mana=max_mana,
        physical_attack=physical_attack,
        magical_attack=magical_attack,
        armor=armor,
        crit_chance_percent=crit_chance,
        dodge_chance_percent=dodge_chance,
    )