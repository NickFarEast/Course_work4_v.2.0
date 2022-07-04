import os
from dataclasses import dataclass, asdict
from typing import List
from random import uniform
import marshmallow_dataclass
import marshmallow
import json

EQUIPMENT_PATH = os.path.join(os.path.join(os.path.join(os.getcwd(), 'game'), 'data'), 'equipment.json')


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        raise RuntimeError("Такое оружие не найдено")

    def get_armor(self, armor_name) -> Armor:
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        raise RuntimeError("Такая броня не найдена")

    def get_weapons_names(self) -> list:
        return [item.name for item in self.equipment.weapons]

    def get_armors_names(self) -> list:
        return [item.name for item in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:

        with open(EQUIPMENT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError








