#!/usr/bin/python

from collections import defaultdict

def main():
    with open("opcodes.pi") as f:
        raw_instructions = f.read().split("\n")

    instructions = parse(raw_instructions)

    more_than_three = determine_opcodes(instructions)

    print("the answer is", more_than_three)

def determine_opcodes(instructions):
    instrs = {}
    instrs['addr'] = lambda a, b, r: r[a] + r[b]
    instrs['addi'] = lambda a, b, r: r[a] + b
    instrs['mulr'] = lambda a, b, r: r[a] * r[b]
    instrs['muli'] = lambda a, b, r: r[a] * b
    instrs['banr'] = lambda a, b, r: r[a] & r[b]
    instrs['bani'] = lambda a, b, r: r[a] & b
    instrs['borr'] = lambda a, b, r: r[a] | r[b]
    instrs['bori'] = lambda a, b, r: r[a] | b
    instrs['setr'] = lambda a, b, r: r[a]
    instrs['seti'] = lambda a, b, r: a
    instrs['gtir'] = lambda a, b, r: 1 if a > r[b] else 0
    instrs['gtri'] = lambda a, b, r: 1 if r[a] > b else 0
    instrs['gtrr'] = lambda a, b, r: 1 if r[a] > r[b] else 0
    instrs['eqir'] = lambda a, b, r: 1 if a == r[b] else 0
    instrs['eqri'] = lambda a, b, r: 1 if r[a] == b else 0
    instrs['eqrr'] = lambda a, b, r: 1 if r[a] == r[b] else 0

    more_than_three = 0

    for instruction in instructions:
        n = 0
        for name, inst in instrs.iteritems():
            out = inst(instruction['instruction'][1], instruction['instruction'][2], instruction['before'])

            if out == instruction['after'][instruction['instruction'][-1]]:
                n += 1

        if n > 2:
            more_than_three += 1

    return more_than_three


def parse(raw):
    opcodes = []
    for i in range(len(raw) / 4):
        index = i * 4
        before = [int(x) for x in raw[index][9:-1].split(", ")]
        instruction = [int(x) for x in raw[index + 1].split()]
        after = [int(x) for x in raw[index + 2][9:-1].split(", ")]

        opcodes.append(dict(
            before=before,
            after=after,
            instruction=instruction
        ))

    return opcodes

if __name__ == "__main__":
    main()
