#!/usr/bin/env python3

import sys
from collections import defaultdict
from copy import deepcopy
from recordtype import recordtype

Character = recordtype("Character", ["hp", "damage", "mana", "armor"], default=0)
Spell = recordtype("Spell", ["name", "cost", "effect", "duration"])


def magic_missle(_, boss):
    boss.hp -= 4


def drain(player, boss):
    boss.hp -= 2
    player.hp += 2


def shield(player, _):
    player.armor = 7


def poison(_, boss):
    boss.hp -= 3


def recharge(player, _):
    player.mana += 101


MAGIC_MISSLE = "Magic Missle"
DRAIN = "Drain"
SHIELD = "Shield"
POISON = "Poison"
RECHARGE = "Recharge"

SPELL_NAMES = [
    MAGIC_MISSLE,
    DRAIN,
    SHIELD,
    POISON,
    RECHARGE
]

SPELLS = {
    MAGIC_MISSLE: Spell(MAGIC_MISSLE, 53, magic_missle, 1),
    DRAIN: Spell(DRAIN, 73, drain, 1),
    SHIELD: Spell(SHIELD, 113, shield, 6),
    POISON: Spell(POISON, 173, poison, 6),
    RECHARGE: Spell(RECHARGE, 229, recharge, 5)
}


MIN_REQUIRED_MANA = 53


def main(boss):
    mana = fight(
        Character(50, 0, 500),
        boss
    )

    print(f"least amount of mana required to win: {mana}")


LEAST = sys.maxsize

def fight(player, boss, effects=defaultdict(int), turn=0, mana_spent=0):
    global LEAST
    if mana_spent > LEAST:
        return None

    if turn % 2 == 0:
        player.hp -= 1

        if player.hp <= 0:
            return None

    for key in effects.keys():
        if effects[key] > 0:
            SPELLS[key].effect(player, boss)
            effects[key] -= 1
        elif key == SHIELD:
            player.armor = 0

    if boss.hp <= 0:
        LEAST = min(LEAST, mana_spent)

        return mana_spent

    if turn % 2 == 1:
        player.hp -= max(1, boss.damage - player.armor)
        if player.hp <= 0:
            return None

        return fight(player, boss, effects, turn + 1, mana_spent)
    else:
        # pick a spell, if able (if not, return False, None)
        if player.mana < MIN_REQUIRED_MANA:
            return None

        available_spells = [
            spell for spell in SPELLS.values() \
                if effects[spell.name] == 0 \
                and spell.cost <= player.mana
        ]

        options = []
        for spell in available_spells:
            effects_copy = deepcopy(effects)
            player_copy = deepcopy(player)
            boss_copy = deepcopy(boss)
            effects_copy[spell.name] = spell.duration
            player_copy.mana -= spell.cost

            options.append(
                fight(
                    player_copy,
                    boss_copy,
                    effects_copy,
                    turn + 1,
                    mana_spent + spell.cost
                )
            )

        return min(filter(None, options + [sys.maxsize]))


def parse_boss(raw):
    parts = []
    for r in raw:
        n = int(r.split()[-1])
        parts.append(n)

    return Character(*parts)


if __name__ == "__main__":
    with open("boss.pi") as f:
        boss = parse_boss(f.read().strip().split("\n"))
        main(boss)

