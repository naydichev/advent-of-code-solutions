#!/usr/bin/env python3

from queue import Queue

dicerolls = Queue()

[dicerolls.put_nowait(x + 1) for x in range(100)]


def main():
    player_1_position, player_2_position = parse_input()

    player_1_score, player_2_score = 0, 0

    turns = 0

    on_deck = 1

    while player_1_score < 1000 and player_2_score < 1000:
        spaces, values = dice_value()

        turns += 1
        if on_deck == 1:
            player_1_position = ((player_1_position + spaces) % 10)
            player_1_score += player_1_position + 1
            on_deck = 2
            print(f"Player 1 rolls {'+'.join(values)} and moves to space {player_1_position + 1} for a total score of {player_1_score}")
        else:
            player_2_position = ((player_2_position + spaces) % 10)
            player_2_score += player_2_position + 1
            on_deck = 1
            print(f"Player 2 rolls {'+'.join(values)} and moves to space {player_2_position + 1} for a total score of {player_2_score}")


    loser = min(player_1_score, player_2_score)
    print(f"The thing {loser * turns * 3}")

def dice_value():
    s = []
    for _ in range(3):
        v = dicerolls.get()
        dicerolls.put_nowait(v)
        s.append(v)

    return sum(s), [str(k) for k in s]


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    processed = [int(x[-1]) - 1 for x in data]

    return processed


if __name__ == "__main__":
    main()
