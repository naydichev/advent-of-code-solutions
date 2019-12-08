#!/usr/bin/env python3


def main(raw, width=25, height=6):
    layers = parse(raw, width, height)

    fewest_zeroes = min(layers, key=lambda x: x.count('0'))
    ones = fewest_zeroes.count('1')
    twos = fewest_zeroes.count('2')

    print(f"I guess they want {ones * twos}")


def parse(raw, width, height):
    layers = []
    dlayer = width * height

    i = 0
    while i < len(raw):
        layers.append(raw[i:i + dlayer])
        i += dlayer

    return layers


if __name__ == "__main__":
    with open("layers.pi") as f:
        main(f.read().rstrip())
