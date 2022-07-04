from .hero import BaseUnit
from typing import Optional


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_is_running = False
        self.battle_result = ""

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self) -> Optional[str]:
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            return self._end_game(results="Ничья")
        if self.player.hp > 0 and self.enemy.hp <= 0:
            return self._end_game(results="Игрок выиграл битву")
        if self.player.hp <= 0 and self.enemy.hp > 0:
            return self._end_game(results="Игрок проиграл битву")
        return None

    def _stamina_regeneration(self):
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()

    def next_turn(self):
        if results := self._check_players_hp():
            return results

        if not self.game_is_running:
            return self.battle_result

        delta_damage: Optional[float] = self.enemy.hit(self.player)
        if delta_damage is not None:
            self.player.get_damage(delta_damage)
            results = f"{self.enemy.name} используя {self.enemy.weapon.name} пробивает {self.player.armor.name} и наносит Вам {delta_damage} урона. "
        else:
            results = f"{self.enemy.name} попытался использовать {self.enemy.weapon.name}, но у него не хватило выносливости. "
        self._stamina_regeneration()
        return results


    def _end_game(self, results) -> str:
        self.game_is_running = False
        self.battle_result = results
        return results


    def player_hit(self):
        delta_damage: Optional[float] = self.player.hit(self.enemy)
        if delta_damage is not None:
            self.enemy.get_damage(delta_damage)
            return f"<p>{self.player.name} используя {self.player.weapon.name} пробивает {self.enemy.armor.name} соперника и наносит {delta_damage} урона.</p><p>{self.next_turn()}</p>"
        else:
            return f"<p>{self.player.name} попытался использовать {self.player.weapon.name}, но у него не хватило выносливости.</p><p>{self.next_turn()}</p>"


    def player_use_skill(self):
        delta_damage: Optional[float] = self.player.use_skill()
        if delta_damage is not None:
            self.enemy.get_damage(delta_damage)
            return f"<p>{self.player.name} используя {self.player.unit_class.skill.name} пробивает {self.enemy.armor.name} соперника и наносит {delta_damage} урона.</p><p>{self.next_turn()}</p>"

        elif delta_damage is None and self.player.stamina < self.player.unit_class.skill.stamina:
            return f"<p>{self.player.name} попытался использовать {self.player.unit_class.skill.name}, но у него не хватило выносливости.</p><p>{self.next_turn()}</p>"

        else:
            return f"<p>{self.player.name} уже использовал свое умение.</p><p>{self.next_turn()}</p>"