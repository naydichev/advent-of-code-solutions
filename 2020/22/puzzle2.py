#!/usr/bin/env python3

def main():
    with open("combat.pi") as f:
        player1, player2 = parse(f.readlines())

    winner, did_player1_win = play_game(player1, player2)

    score = 0
    for i, value in enumerate(reversed(winner)):
        score += (i + 1) * value

    print(f"the winner's score is {score}")


def play_game(player1, player2):
    seen = set()
    while len(player1) and len(player2):
        p1h = "|".join([str(s) for s in player1])
        p2h = "|".join([str(s) for s in player2])
        if (p1h, p2h) in seen:
            return player1, True
        seen.add((p1h, p2h))

        p1 = player1.pop(0)
        p2 = player2.pop(0)

        did_player1_win = False
        if len(player1) >= p1 and len(player2) >= p2:
            _, did_player1_win = play_game(player1[:][:p1], player2[:][:p2])
        elif p1 > p2:
            did_player1_win = True

        if did_player1_win:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    if len(player1):
        return player1, True
    return player2, False


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
