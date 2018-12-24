#!/usr/bin/python

import copy
import re

IMMUNE = "immune"
INFECTION = "infection"
I_SYS = "Immune System:"
IN_SYS = "Infection:"

class Group(object):
    def __init__(self, units, hp, weaknesses, immunity, attack, attack_type, initiative, type, id):
        self.units = units
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunity = immunity
        self.attack = attack
        self.attack_type = attack_type
        self.initiative = initiative
        self.type = type
        self.id = id
        self._boost = 0

    @property
    def effective_power(self):
        return self.units * (self.attack + self._boost)

    def __cmp__(self, other):
        if other.effective_power == self.effective_power:
            return other.initiative - self.initiative
        return other.effective_power - self.effective_power

    def __repr__(self):
        return "{}(units={}, hp={}, weaknesses={}, immunity={}, attack={}, attack_type={}, initiative={}, boost={}, id={})".format(
            self.__class__.__name__,
            self.units,
            self.hp,
            self.weaknesses,
            self.immunity,
            self.attack,
            self.attack_type,
            self.initiative,
            self._boost,
            self.id
        )

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def boost(self, b):
        pass

class ImmuneSystem(Group):
    ID = 0
    def __init__(self, units, hp, weaknesses, immunity, attack, attack_type, initiative):
        super(ImmuneSystem, self).__init__(
            units,
            hp,
            weaknesses,
            immunity,
            attack,
            attack_type,
            initiative,
            IMMUNE,
            ImmuneSystem.ID
        )

        ImmuneSystem.ID += 1

    def boost(self, b):
        self._boost = b

class Infection(Group):
    ID = 0
    def __init__(self, units, hp, weaknesses, immunity, attack, attack_type, initiative):
        super(Infection, self).__init__(
            units,
            hp,
            weaknesses,
            immunity,
            attack,
            attack_type,
            initiative,
            INFECTION,
            Infection.ID
        )

        Infection.ID += 1

PATTERN = re.compile("^(\d+) units each with (\d+) hit points (\([^\)]+\))?\s?with an attack that does (\d+) (\w+) damage at initiative (\d+)$")

IM_GROUPS = lambda g: filter(lambda k: isinstance(k, ImmuneSystem), g)
IN_GROUPS = lambda g: filter(lambda k: isinstance(k, Infection), g)

def main(original_groups):
    first = True
    boost = 41

    while first or len(IM_GROUPS(groups)) == 0:
        groups = copy.deepcopy(original_groups)
        first = False
        boost += 1
        [g.boost(boost) for g in groups]
        # print("Trying boost of {}".format(boost))
        while not only_one_type_left(groups):
            print_groups(groups)
            attackers = []
            targets = groups[:]
            # attacking  phase
            for attacker in sorted(groups):
                target = find_target(attacker, targets)
                if target:
                    attackers.append((attacker, target))
                    targets.remove(target)


            for attacker, defender in sorted(attackers,key=lambda k:  -k[0].initiative):
                print_attack(attacker, defender)
                if defender not in groups or attacker not in groups:
                    continue

                units_lost = compute_attack(attacker, defender) // defender.hp
                defender.units -= units_lost

                if defender.units <= 0:
                    groups.remove(defender)

            print("")

        break

    print_groups(groups)
    print(sum([g.units for g in groups]))

def only_one_type_left(groups):
    immune = IM_GROUPS(groups)
    infection = IN_GROUPS(groups)

    return len(immune) == 0 or len(infection) == 0

def find_target(attacker, group):
    enemies = [p for p in group if not isinstance(p, attacker.__class__)]

    most_damage = 0
    chosen = None
    for enemy in enemies:
        atk = compute_attack(attacker, enemy)

        if atk > most_damage:
            most_damage = atk
            chosen = enemy
        elif atk == most_damage:
            if chosen and enemy.effective_power > chosen.effective_power:
                chosen = enemy
            elif chosen and enemy.effective_power == chosen.effective_power and enemy.initiative > chosen.initiative:
                chosen = enemy

    return chosen

def compute_attack(attacker, defender):
    dmg = attacker.effective_power

    if defender.immunity and attacker.attack_type in defender.immunity:
        dmg = 0
    elif  defender.weaknesses and attacker.attack_type in defender.weaknesses:
        dmg = dmg * 2

    return dmg

def parse(raw):
    groups = []
    is_immune = None
    for row in raw:
        if row == I_SYS:
            is_immune = True
            continue
        elif row == IN_SYS:
            is_immune = False
            continue
        elif row == "":
            continue

        group = parse_row(row, ImmuneSystem if is_immune else Infection)
        groups.append(group)

    return groups

def parse_row(row, cls):
    match = PATTERN.match(row)

    if not match:
        print(row)
        raise ValueError("invalid row")

    weaknesses, immunity  =  parse_weaknesses(match.group(3))
    return cls(
        int(match.group(1)),
        int(match.group(2)),
        weaknesses,
        immunity,
        int(match.group(4)),
        match.group(5),
        int(match.group(6))
    )

def parse_weaknesses(raw):
    if raw is None:
        return None, None

    raw = raw[1:-1]
    if ";" in raw:
        return parse_parts(*raw.split("; "))
    else:
        return parse_parts(raw, None)

W = "weak to"
I = "immune to"
def parse_parts(part1, part2):
    weaknesses = None
    immunity = None
    if part1 and part1.startswith(I):
        immunity = [x.strip() for x in part1[len(I):].split(",")]
    elif part1 and part1.startswith(W):
        weaknesses = [x.strip() for x in part1[len(W):].split(",")]

    if part2 and part2.startswith(I):
        immunity = [x.strip() for x in part2[len(I):].split(",")]
    elif part2 and part2.startswith(W):
        weaknesses = [x.strip() for x in part2[len(W):].split(",")]

    return weaknesses, immunity


def print_attack(attacker, defender):
    units = max(compute_attack(attacker, defender) //  defender.hp, defender.units)
    print("{} group {} ({}) attacks defending group {}, killing {} units".format(attacker.__class__.__name__,  attacker.id + 1, attacker.initiative, defender.id + 1, units))

def print_groups(groups):
    print(I_SYS)
    for i in sorted(IM_GROUPS(groups), key=lambda k: k.id):
        print(format_group(i))

    print("")
    print(IN_SYS)
    for i in sorted(IN_GROUPS(groups), key=lambda k: k.id):
        print(format_group(i))
    print("")

def format_group(group):
    s = "{} units each with {} hit points {}with an attack that does {} {} damage at initiative {}"

    t = ""
    m = []
    if group.weaknesses:
        m.append(W + " " + ", ".join(sorted(group.weaknesses)))
    if group.immunity:
        m.append(I + " " + ", ".join(sorted(group.immunity)))

    if m:
        t = "({}) ".format("; ".join(m))

    return s.format(group.units, group.hp, t, (group.attack + group._boost), group.attack_type, group.initiative)


if  __name__ == "__main__":
    filename = "infection.pi"
#    filename = "sample.pi"
    with open(filename) as f:
        raw = f.read().split("\n")

    main(parse(raw))
