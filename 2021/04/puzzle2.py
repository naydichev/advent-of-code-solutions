#!/usr/bin/env python3

class Box:
    def __init__(self, number):
        self.number = number
        self.marked = False

    def __repr__(self):
        return f"<Box number={self.number} marked={self.marked}>"


def main():
    numbers, boards = parse_input()

    for number in numbers:
        mark_boards(number, boards)

        to_remove = find_winner(boards)
        while to_remove:
            winner = to_remove
            boards.remove(to_remove)

            to_remove = find_winner(boards)

        if len(boards) == 0:
            print_board(winner)
            unmarked = sum_unmarked(winner)
            total = unmarked * number
            print(f"The winner is {total}")
            break

def print_board(board):
    for row in board:
        for val in row:
            if val.marked:
                print("\033[0;31m", end="")
            print(f"{val.number:2}\033[0m", end=" ")
        print("")


def mark_boards(number, boards):
    for board in boards:
        for row in board:
            for value in row:
                if value.number == number:
                    value.marked = True


def find_winner(boards):
    for board in boards:
        columns = [ [] for _ in range(len(board[0])) ]

        for row, values in enumerate(board):
            if all([v.marked for v in values]):
                return board

            for col, n in enumerate(values):
                columns[col].append(n)

        for col in columns:
            if all([v.marked for v in col]):
                return board

    return None


def sum_unmarked(board):
    total = 0

    for row in board:
        for col in row:
            if not col.marked:
                total += col.number

    return total


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()]

    numbers = [int(i) for i in data.pop(0).split(",")]
    data.pop(0)

    boards = []
    board = []

    for line in data:
        if line == "":
            boards.append(board)
            board = []
        else:
            board.append([Box(int(i)) for i in line.replace("  ", " ").split(" ")])

    boards.append(board)

    return numbers, boards


if __name__ == "__main__":
    main()
