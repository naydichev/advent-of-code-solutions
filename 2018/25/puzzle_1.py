#!/usr/bin/python

def m_dist(a, b):
    d = 0
    for i in range(len(a)):
        d += abs(a[i] - b[i])

    # print("distance between {} and {} is {}".format(a, b, d))
    return d

def main(raw):
    data = []
    for row in raw:
        data.append([int(i) for i in row.split(",")])

    constellations = []
    while len(data):
        point  = data[0]
        this_constellation = [point]
        added = True
        while added:
            added = False
            for other in data:
                if other in this_constellation:
                    continue
                dist_map = map(lambda c: m_dist(other, c) <= 3, this_constellation)
                if any(dist_map):
                    this_constellation.append(other)
                    added = True

        constellations.append(this_constellation)
        for c in  this_constellation:
            data.remove(c)

    # print(len(constellations))
    return len(constellations)

if __name__ == "__main__":
    raw = """
    0,0,0,0
    3,0,0,0
    0,3,0,0
    0,0,3,0
    0,0,0,3
    0,0,0,6
    9,0,0,0
    12,0,0,0
    """.split("\n")[1:-1]

    assert main(raw) == 2

    raw = """
    -1,2,2,0
    0,0,2,-2
    0,0,0,-2
    -1,2,0,0
    -2,-2,-2,2
    3,0,2,-1
    -1,3,2,2
    -1,0,-1,0
    0,2,1,-2
    3,0,0,0
    """.split("\n")[1:-1]

    assert main(raw) == 4

    raw = """
    1,-1,0,1
    2,0,-1,0
    3,2,-1,0
    0,0,3,1
    0,0,-1,-1
    2,3,-2,0
    -2,2,0,0
    2,-2,0,-1
    1,-1,0,-1
    3,2,0,2
    """.split("\n")[1:-1]

    assert main(raw) == 3

    raw = """
    1,-1,-1,-2
    -2,-2,0,1
    0,2,1,3
    -2,3,-2,1
    0,2,3,-2
    -1,-1,1,-2
    0,-2,-1,0
    -2,2,3,-1
    1,2,2,0
    -1,-2,0,-2
    """.split("\n")[1:-1]

    assert main(raw) == 8

    with open("constellations.pi") as f:
        raw = f.read().split("\n")

    print(main(raw))
