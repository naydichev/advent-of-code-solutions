#!/usr/bin/env python3

def main():
    # with open("sample.pi") as f:
    with open("jolts.pi") as f:
        jolts = parse(f.readlines())

    one_diff = 0
    three_diff = 0

    prev_joltage = 0

    for jolt in sorted(jolts):
        diff = jolt - prev_joltage
        if diff == 1:
            one_diff += 1
        elif diff == 3:
            three_diff += 1

        prev_joltage = jolt

    three_diff += 1

    print(f"1-jolts {one_diff}, 3-jolts {three_diff}, ansewr {one_diff * three_diff}")


def parse(raw):
    return map(int, raw)


if __name__ == "__main__":
    main()
