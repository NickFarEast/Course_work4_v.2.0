from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    damage: float
    stamina: float


furious_kick = Skill(name="Свирепый пинок", damage=22, stamina=6)
hard_shot = Skill(name="Мощный укол", damage=15, stamina=5)
