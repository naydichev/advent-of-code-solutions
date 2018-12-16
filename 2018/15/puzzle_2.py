#!/usr/bin/python

from collections import defaultdict
from collections import deque

WALL = "#"
SPACE = "."
ELF = "E"
GOBLIN = "G"

def main(caverns, monsters):

    rounds = 0
    while not one_monster_type_left(monsters):
        # print(rounds)
        # print_cavern(caverns, monsters)

        try:
            perform_round(caverns, monsters)
        except StopIteration:
            print("round ends early")
            break

        rounds += 1

    print("there were {} rounds".format(rounds))
    print_cavern(caverns, monsters)

    print("the answer for part 2 is {}".format((rounds) * sum(m.health for m in monsters)))
    return True

def perform_round(caverns, monsters):
    to_remove = []
    early_end = False
    for m in sorted(monsters, key=lambda x: x.position):
        # in case we were killed in a previous turn
        if m in to_remove:
            continue

        move_target = find_move_target(caverns, m, monsters)
        if move_target:
            move_closer_to_target(caverns, m, move_target)

        attack_target = find_attack_target(caverns, m, monsters)
        if attack_target:
            attack(m, attack_target)

            if attack_target.health <= 0:
                caverns[attack_target.position].monster = None
                if attack_target.type == ELF:
                    raise ValueError
                to_remove.append(attack_target)

                if one_monster_type_left(set(monsters) - set(to_remove)):
                    early_end = True
                    break

    for m in to_remove:
        monsters.remove(m)

    if early_end:
        raise StopIteration

def find_move_target(caverns, monster, monsters):
    adjacent_enemies = caverns[monster.position].adjacent_enemies(caverns)
    if len(adjacent_enemies):
        return None

    adjacent_to_enemy = []
    for enemy in [m for m in monsters if m.type != monster.type and m.health > 0]:
        adjacent_to_enemy.extend(caverns[enemy.position].adjacent_empty_positions(caverns))

    shortest_paths = find_shortest_paths(caverns, monster.position, adjacent_to_enemy)
    if not shortest_paths:
        return None

    return sorted(shortest_paths, key=lambda k: k[-1])[0]

def find_shortest_paths(caverns, start, possible_ends):
    visited = set([start])
    distances = defaultdict(list)
    queue = deque((p, 1, start) for p in sorted(caverns[start].adjacent_non_wall_positions(caverns)))

    paths = {}
    while len(queue):
        position, distance, previous = queue.popleft()
        if position in visited:
            continue

        visited.add(position)

        if caverns[position].type == WALL or caverns[position].monster is not None:
            continue

        if position not in paths or distance < paths[position]["distance"]:
            paths[position] = dict(distance=distance, previous=previous)
        elif position in paths and distance == paths[position]["distance"] and previous < paths[position]["previous"]:
            paths[position] = dict(distance=distance, previous=previous)

        if position in possible_ends:
            distances[distance].append(position)
        else:
            queue.extend((p, distance + 1, position) for p in sorted(caverns[position].adjacent_empty_positions(caverns)))

    if not len(distances):
        return None

    min_key = min(distances.keys())
    paths_to_targets = []
    for target in distances[min_key]:
        # walk it back
        my_path = []
        path_key = target
        while path_key != start:
            my_path.append(path_key)
            path_key = paths[path_key]["previous"]

        paths_to_targets.append(list(reversed(my_path)))

    return paths_to_targets


def find_attack_target(caverns, monster, monsters):
    enemies = caverns[monster.position].adjacent_enemies(caverns)
    if len(enemies):
        min_health = min(enemies, key=lambda k: k.health).health
        min_health_enemies = filter(lambda k: k.health == min_health, enemies)

        if len(min_health_enemies) > 1:
            return sorted(min_health_enemies, key=lambda k: k.position)[0]

        return min_health_enemies[0]

    return None

def move_closer_to_target(caverns, monster, path_to_target):
    next_step = path_to_target.pop(0)
    caverns[monster.position].monster = None
    caverns[next_step].monster = monster
    monster.position = next_step

def attack(attacker, target):
        target.health -= attacker.attack

def one_monster_type_left(monsters):
    return all(m.type == ELF for m in monsters) or all(m.type == GOBLIN for m in monsters)

def parse(raw, elf_power):
    monsters = []
    caverns = {}

    for y, row in enumerate(raw):
        for x, el in enumerate(row):
            position = Position(x, y)
            if el == ELF or el == GOBLIN:
                if el == ELF:
                    monster = Elf(position, attack=elf_power)
                else:
                    monster = Goblin(position)

                monsters.append(monster)
                caverns[position] = Cavern(position, SPACE, monster)
            else:
                caverns[position] = Cavern(position, el)

    return caverns, monsters


def print_cavern(caverns, monsters):
    y = 0
    row = []
    monsters_in_row = []
    for position in sorted(caverns.keys()):
        if position.y != y:
            monsters = []
            for m in monsters_in_row:
                monsters.append("{}({})".format(m.id, m.health))
            row.append(" ")
            row.append(",".join(monsters))
            print("".join(row))
            row = []
            monsters_in_row = []
            y = position.y
        if caverns[position].monster is not None:
            row.append(caverns[position].monster.type)
            monsters_in_row.append(caverns[position].monster)
        else:
            row.append(caverns[position].type)
    print("".join(row))

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __cmp__(self, other):
        if self.y == other.y:
            return self.x - other.x
        return self.y - other.y

    def __hash__(self):
        return hash("{},{}".format(self.x, self.y))

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def is_adjacent(self, other):
        return (abs(self.x - other.x) + abs(self.y - other.y)) == 1


class Monster(object):
    ID = 0
    def __init__(self, position, type):
        self.id = "{}{}".format(type, Monster.ID)
        self.position = position
        self.type = type
        self.health = 200
        self.attack = 3

        Monster.ID += 1

    def __eq__(self, other):
        return self.id == other.id

    def __cmp__(self, other):
        if self.position.y == other.position.y:
            return self.position.x - other.position.x
        return self.position.y - other.position.y

    def is_enemy(self, other):
        return self.type != other.type

    def __repr__(self):
        return "{}(position={}, health={}, id={})".format(self.__class__.__name__, self.position, self.health, self.id)

class Elf(Monster):
    def __init__(self, position, attack):
        super(Elf, self).__init__(position, ELF)

        self.attack = attack

class Goblin(Monster):
    def __init__(self, position):
        super(Goblin, self).__init__(position, GOBLIN)

class Cavern:
    def __init__(self, position, type, monster=None):
        self.position = position
        self.type = type
        self.monster = monster

    @property
    def adjacent_positions(self):
        return [Position(self.position.x+x, self.position.y+y) for x, y in ((0, 1), (0, -1), (1, 0), (-1, 0))]

    def adjacent_non_wall_positions(self, caverns):
        non_walls = []
        for adjacent in self.adjacent_positions:
            if caverns[adjacent].type != WALL:
                non_walls.append(adjacent)

        return non_walls

    def adjacent_empty_positions(self, caverns):
        empty = []
        for adjacent in self.adjacent_non_wall_positions(caverns):
            if caverns[adjacent].monster is None:
                empty.append(adjacent)

        return empty

    def adjacent_enemies(self, caverns):
        enemies = []
        my_type = self.monster.type if self.monster else None
        for adjacent in self.adjacent_non_wall_positions(caverns):
            if caverns[adjacent].monster is not None and caverns[adjacent].monster.type != my_type:
                enemies.append(caverns[adjacent].monster)

        return enemies

    def __eq__(self, other):
        return self.position == other.position and self.type == other.type and self.monster == other.monster

if __name__ == "__main__":
    with open("caverns.pi") as f:
        raw_caverns = f.read().split("\n")

    elves_win = False
    elf_power = 3
    while not elves_win:
        try:
            Monster.ID = 0
            caverns, monsters = parse(raw_caverns, elf_power)
            elves_win = main(caverns, monsters)
        except ValueError:
            # increase elf power and try again
            elf_power += 1
            print("We lost an elf, increasing attack power to {} and trying again".format(elf_power))
            for m in monsters:
                if m.type == ELF:
                    m.attack = elf_power

