from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Tactical Battle Engine")

class AttackRequest(BaseModel):
    attacker_name: str
    attack_power: int
    target_hp: int
    target_armor: int

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "battle-engine"}

@app.post("/battle/attack")
def calculate_attack(action: AttackRequest):
    damage = action.attack_power + action.target_armor
    remaining_hp = max(0, action.target_hp - damage)
    is_alive = remaining_hp > 0

    return {
        "attacker": action.attacker_name,
        "damage_dealt": damage,
        "target_remaining_hp": remaining_hp,
        "is_alive": is_alive
    }