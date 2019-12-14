#!/usr/bin/env python3

from collections import defaultdict
from itertools import combinations
from recordtype import recordtype

Character = recordtype("Character", ["hp", "damage", "armor"])
Item = recordtype("Item", ["kind", "name", "cost", "damage", "armor"])

EMPTY = Item("EMPTY", "EMPTY", 0, 0, 0)
WEAPONS = "Weapons"
ARMOR = "Armor"
RINGS = "Rings"

def main(store, boss):
    max_gold = 0
    for ring1, ring2 in combinations(store[RINGS] + [EMPTY, EMPTY], 2):
        for weapon in store[WEAPONS]:
            for armor in store[ARMOR] + [EMPTY]:

                boss_copy = Character(boss.hp, boss.damage, boss.armor)
                items = [weapon, armor, ring1, ring2]
                player = Character(100, sum(i.damage for i in items), sum(i.armor for i in items))

                if not fight(boss_copy, player):
                    cost = sum(i.cost for i in items)
                    max_gold = max(max_gold, cost)

    print(f"maximum gold to win {max_gold}")


def fight(boss, player):
    turn = 0
    while player.hp > 0 and boss.hp > 0:
        attack_damage = player.damage if turn % 2 == 0 else boss.damage
        defend_armor = player.armor if turn % 2 == 1 else boss.armor
        dmg = max(1, attack_damage - defend_armor)

        if turn % 2 == 0:
            boss.hp -= dmg
        else:
            player.hp -= dmg

        turn += 1

    return player.hp > 0


def parse_store(raw):
    items = defaultdict(list)

    kind = None
    for line in raw:
        if not len(line):
            continue

        if ":" in line:
            kind = line.split(":")[0]
            continue

        while "  " in line:
            line = line.replace("  ", " ")

        if kind == "Rings":
            line = line.replace(" ", "_", 1)

        parts = line.split()

        items[kind].append(
            Item(kind, parts[0], int(parts[1]), int(parts[2]), int(parts[3]))
        )

    return items


def parse_boss(raw):
    parts = []
    for r in raw:
        n = int(r.split()[-1])
        parts.append(n)

    return Character(*parts)


if __name__ == "__main__":
    with open("store.pi") as f:
        store = parse_store(f.read().strip().split("\n"))
    with open("boss.pi") as f:
        boss = parse_boss(f.read().strip().split("\n"))

    main(store, boss)
