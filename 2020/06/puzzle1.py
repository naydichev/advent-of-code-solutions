#!/usr/bin/env python3


def main():
    with open("customs.pi") as f:
        groups = parse(f.readlines())

    total_questions = sum([len(group) for group in groups])

    print(f"{total_questions} were answered with a yes")


def parse(raw):
    groups = []
    group = set([])

    for row in raw:
        row = row.strip()
        if row == "":
            groups.append(group)
            group = set([])

            continue

        group.update(row)

    groups.append(group)
    return groups


if __name__ == "__main__":
    main()
