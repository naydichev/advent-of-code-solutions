#!/usr/bin/python

from collections import defaultdict, deque

def main():
    with open("game_specs.pi") as f:
        raw_specs = f.read()

    parts = raw_specs.split()
    num_players = int(parts[0])
    num_marbles = int(parts[-2])

    scores = play_game(num_players, num_marbles)

    max_score = max(scores.values())
    print(max_score)

def play_game(players, marbles):
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(marbles):
        marble += 1
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return scores

if __name__ == "__main__":
    main()
