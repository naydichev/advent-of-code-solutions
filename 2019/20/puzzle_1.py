#!/usr/bin/env python3

from collections import defaultdict, namedtuple

SPACE = "."
WALL = "#"
VOID = " "
PORTAL = "@"
D = [(0, 1), (0, -1), (1, 0), (-1, 0)]

Point = namedtuple("Point", ["x", "y"])
Space = namedtuple("Space", ["kind"], defaults=[VOID])
Portal = namedtuple("Portal", ["kind", "name", "points"], defaults=[PORTAL, None, None])


def main(raw):
    torus, portals = parse(raw)

    start = [v for v in torus.values() if v.kind == PORTAL and v.name == "AA"][0]
    end = [v for v in torus.values() if v.kind == PORTAL and v.name == "ZZ"][0]
    paths = find_paths(torus, portals)

    shortest = find_shortest_path(paths, start)

    print(f"shortest is {shortest}")


def find_paths(torus, portals):
    paths = defaultdict(list)
    for point, portal in portals.items():
        reachable = find_reachable_portals(torus, point)

        for r_portal, r_dist in reachable.items():
            print(f"{portal.name} -> {r_portal.name} = {r_dist}")
            paths[portal].append((r_portal, r_dist))

    for k, v in paths.items():
        print(k.name, [x[0].name for x in v])

    return paths

def find_reachable_portals(torus, current):
    queue = [current]
    distance = {current: 0}
    found_portals = {torus[current]: 0}

    while len(queue):
        inspect = queue.pop(0)
        for point in [Point(inspect.x + x, inspect.y + y) for x, y in D]:
            space = torus[point]

            if space.kind in [WALL, VOID] or point in distance:
                continue

            distance[point] = distance[inspect] + 1

            if space.kind == PORTAL and space not in found_portals:
                found_portals[space] = distance[point] + 1
            elif space.kind == SPACE:
                queue.append(point)

    # remove the starting portal
    del found_portals[torus[current]]

    return found_portals


def find_shortest_path(paths, current, traversed=[]):
    if current.name == "ZZ":
        return 0

    print(current, traversed)
    traversed.append(current.name)
    options = []
    for portal, distance in paths[current]:
        if portal.name in traversed:
            continue

        calc = find_shortest_path(paths, portal, traversed.copy())
        if calc is not None:
            options.append(distance + calc)

    print(options)
    if len(options) == 0:
        return None

    return min(options)


def flip_it(portals):
    flipped = {}
    for key, value in portals.items():
        for p in value.points:
            flipped[p] = value

    for k, v in flipped.items():
        print(k, v.name)
    return flipped


def parse(raw):
    torus = defaultdict(Space)
    rportals = defaultdict(list)

    height = len(raw)
    for y, line in enumerate(raw[:-1]):
        width = len(line)
        for x, c in enumerate(line):
            if c == " ":
                continue
            elif c in [SPACE, WALL]:
                torus[Point(x, y)] = Space(c)
            else:
                # it's a portal
                if y == 0:
                    name = f"{c}{raw[y + 1][x]}"
                    p = Point(x, y + 2)
                elif y == height - 2 or raw[y - 1][x] == SPACE:
                    name = f"{c}{raw[y + 1][x]}"
                    p = Point(x, y - 1)
                elif x == width - 2 or line[x - 1] == SPACE:
                    name = f"{c}{raw[y][x + 1]}"
                    p = Point(x - 1, y)
                elif (x == 0 or (x + 2 < len(line))) and line[x + 1] not in [WALL, SPACE, VOID]:
                    name = f"{c}{raw[y][x + 1]}"
                    p = Point(x + 2, y)

                rportals[name].append(p)

    portals = {}
    for name, points in rportals.items():
        portals[name] = Portal(PORTAL, name, frozenset(points))
        for p in points:
            torus[p] = portals[name]

    return torus, flip_it(portals)


if __name__ == "__main__":
    with open("sample1.pi") as f:
        # with open("torus.pi") as f:
        main(f.read().rstrip().split("\n"))
