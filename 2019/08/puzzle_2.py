#!/usr/bin/env python3

BLACK  = '\33[40m'
WHITE  = '\33[47m'
END    = '\33[0m'


def main(raw, width=25, height=6):
    layers = parse(raw, width, height)

    composite = make_composite(layers, width * height)
    i = 0
    while i < len(composite):
        row = composite[i:i+width]
        line = []
        for x in row:
            color = WHITE
            if x == '0':
                color = BLACK

            line.extend([color, " "])

        line.append(END)
        print("".join(line))

        i += width


def make_composite(layers, layer_length):
    final = []
    n_layers = len(layers)

    for i in range(layer_length):
        this_layer = '2'
        for j in range(n_layers):
            if layers[j][i] in '01':
                this_layer = layers[j][i]
                break

        final.append(this_layer)

    return final


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
