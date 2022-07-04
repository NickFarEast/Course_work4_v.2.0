from __future__ import annotations
from abc import ABC, abstractmethod
from .equipment import Weapon, Armor
from .classes import UnitClass
from random import randint
from typing import Optional

BASE_STAMINA_PER_ROUND = 0.4


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass, weapon: Weapon, armor: Armor):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self._hp = unit_class.max_health
        self._stamina = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self._is_skill_used: bool = False

    @property
    def hp(self):
        return round(self._hp, 1)

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def stamina(self):
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value):
        self._stamina = value

    @property
    def total_armor(self) -> float:  # логику расчета брони цели
        if self.stamina - self.armor.stamina_per_turn >= 0:  # если у защищающегося нехватает выносливости - его
            # броня игнорируется
            return self.armor.defence * self.unit_class.armor
        return 0

    def _count_damage(self, target: BaseUnit) -> Optional[float]:
        if self.stamina - self.weapon.stamina_per_hit < 0:
            return None

        hero_damage = self.weapon.damage * self.unit_class.attack  # логику расчета урона игрока
        damage = hero_damage - target.total_armor
        if damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit  # здесь же происходит уменьшение выносливости атакующего при ударе
        return round(damage, 1)

    def get_damage(self, damage: float):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> Optional[float]:
        """
        Этот метод будет переопределен ниже
        """
        pass

    def use_skill(self) -> Optional[float]:
        if not self._is_skill_used and self.stamina - self.unit_class.skill.stamina > 0:
            self._is_skill_used = True
            self.stamina -= self.unit_class.skill.stamina
            return round(self.unit_class.skill.damage, 1)
        return None

    def regenerate_stamina(self):
        delta_stamina = BASE_STAMINA_PER_ROUND * self.unit_class.stamina
        if self.stamina + delta_stamina <= self.unit_class.max_stamina:
            self.stamina += delta_stamina
        else:
            self.stamina = self.unit_class.max_stamina


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> Optional[float]:
        return self._count_damage(target)


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> Optional[float]:
        if 10 > randint(0, 100) and self.stamina >= self.unit_class.skill.stamina and not self._is_skill_used:
            self.use_skill()
        return self._count_damage(target)

