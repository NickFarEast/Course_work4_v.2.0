from .skills import Skill, furious_kick, hard_shot
from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(
    name="Воин",
    max_health=60.0,
    max_stamina=30.0,
    attack=0.9,
    stamina=0.8,
    armor=1.2,
    skill=furious_kick
)

ThiefClass = UnitClass(
    name="Вор",
    max_health=50.0,
    max_stamina=25.0,
    attack=1.2,
    stamina=1.5,
    armor=1.0,
    skill=hard_shot
)

unit_classes: Dict[str, Type[UnitClass]] = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}
