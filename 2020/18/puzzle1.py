#!/usr/bin/env python3

def main():
    with open("math.pi") as f:
        equations = parse(f.readlines())

    values = []
    for eq in equations:
        values.append(solve(eq))

    print(f"the sum of all answers is {sum(values)}")


def solve(equation):

    while "(" in equation:
        close_idx = equation.find(")")
        open_idx = equation.rfind("(", 0, close_idx)

        val = solve(equation[open_idx + 1:close_idx])
        equation = f"{equation[:open_idx]}{val}{equation[close_idx + 1:]}"

    pieces = equation.split(" ")
    start = int(pieces.pop(0))

    while len(pieces):
        op = pieces.pop(0)
        val = int(pieces.pop(0))

        if op == "+":
            start += val
        else:
            start *= val

    return start


def parse(raw):
    output = []

    for line in raw:
        output.append(line.strip())

    return output


if __name__ == "__main__":
    main()
