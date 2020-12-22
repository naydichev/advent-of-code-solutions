#!/usr/bin/env python3

def main():
    with open("combat.pi") as f:
        player1, player2 = parse(f.readlines())

    while len(player1) and len(player2):
        p1 = player1.pop(0)
        p2 = player2.pop(0)

        if p1 > p2:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    winner = player1
    if len(player1) == 0:
        winner = player2

    score = 0
    for i, value in enumerate(reversed(winner)):
        score += (i + 1) * value

    print(f"the winner's score is {score}")


def parse(raw):
    output = []

    deck = []
    for line in raw:
        line = line.strip()
        if ":" in line:
            continue

        if line == "":
            output.append(deck)
            deck = []
        else:
            deck.append(int(line))

    output.append(deck)

    return output


if __name__ == "__main__":
    main()
