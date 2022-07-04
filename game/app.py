from functools import wraps
from flask import Flask, render_template, request, redirect, url_for
from .hero import BaseUnit, PlayerUnit, EnemyUnit
from .classes import unit_classes
from .equipment import Equipment
from typing import Dict
from .base import Arena

app = Flask(__name__)

heroes: Dict[str, BaseUnit] = dict()

arena = Arena()


def game_processing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if arena.game_is_running:
            return func(*args, **kwargs)
        if arena.battle_result:
            return render_template("fight.html", heroes=heroes, result=arena.battle_result)
        return redirect(url_for("menu_page"))

    return wrapper


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    if "player" in heroes and "enemy" in heroes:
        arena.start_game(**heroes)
        return render_template("fight.html", heroes=heroes, result="Fight")
    return redirect(url_for("menu_page"))


@app.route("/fight/hit")
@game_processing
def hit():
    return render_template("fight.html", heroes=heroes, result=arena.player_hit())


@app.route("/fight/use-skill")
@game_processing
def use_skill():
    return render_template("fight.html", heroes=heroes, result=arena.player_use_skill())


@app.route("/fight/pass-turn")
@game_processing
def pass_turn():
    return render_template("fight.html", heroes=heroes, result=arena.next_turn())


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == "GET":
        return render_template(
            "hero_choosing.html",
            header="Выберите героя",
            classes=unit_classes.values(),
            weapons=Equipment().get_weapons_names(),
            armors=Equipment().get_armors_names(),
            next_button="Выбрать врага"
        )

    heroes["player"] = PlayerUnit(
        unit_class=unit_classes[request.form["unit_class"]],
        weapon=Equipment().get_weapon(request.form["weapon"]),
        armor=Equipment().get_armor(request.form["armor"]),
        name=request.form["name"]
    )

    return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        return render_template(
            "hero_choosing.html",
            header="Выберите врага",
            classes=unit_classes.values(),
            weapons=Equipment().get_weapons_names(),
            armors=Equipment().get_armors_names(),
            next_button="Начать битву"
        )

    heroes["enemy"] = EnemyUnit(
        unit_class=unit_classes[request.form["unit_class"]],
        weapon=Equipment().get_weapon(request.form["weapon"]),
        armor=Equipment().get_armor(request.form["armor"]),
        name=request.form["name"]
    )

    return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run()
