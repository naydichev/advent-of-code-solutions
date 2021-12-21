#!/usr/bin/env python3

from functools import lru_cache

def main():

    p1, p2 = parse_input()
    winner = max(play_game(p1, 0, p2, 0))
    print(winner)


@lru_cache(maxsize=None)
def play_game(p1position, p1score, p2position, p2score):
    p1wins, p2wins = 0, 0
    p1starting = p1position
    p1score_starting = p1score

    for s in [i + j + k for i in (1,2,3) for j in (1,2,3) for k in (1,2,3)]:
        p1position = (p1starting + s - 1) % 10 + 1
        p1score = p1score_starting + p1position

        if p1score >= 21:
            p1wins += 1
        else:
            sub2wins, sub1wins = play_game(p2position, p2score, p1position, p1score)
            p1wins += sub1wins
            p2wins += sub2wins

    return p1wins, p2wins


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    # process data
    processed = [int(x[-1]) for x in data]

    return processed


if __name__ == "__main__":
    main()
