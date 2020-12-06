#!/usr/bin/env python3


def main():
    with open("customs.pi") as f:
        groups = parse(f.readlines())

    total_questions = sum([len(group) for group in groups])

    print(f"{total_questions} were answered by everyone in their group with a yes")


def parse(raw):
    groups = []
    group = set([])
    reset = True

    for row in raw:
        row = row.strip()
        if row == "":
            groups.append(group)
            group = set([])
            reset = True

            continue

        if reset:
            group.update(row)
            reset = False
        else:
            group.intersection_update(row)

    groups.append(group)
    return groups


if __name__ == "__main__":
    main()
