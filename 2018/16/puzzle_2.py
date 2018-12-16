#!/usr/bin/python

from collections import defaultdict

def main():
    with open("opcodes.pi") as f:
        raw_samples = f.read().split("\n")

    with open("instructions.pi") as f:
        raw_instructions = f.read().split("\n")[:-1]

    samples = parse_samples(raw_samples)
    instructions = parse_instructions(raw_instructions)

    opcodes = determine_opcodes(samples)

    out = execute_program(opcodes, instructions)

    print("the answer is", out[0])

def execute_program(opcodes, instructions):
    registers = [0] * 4

    for instruction in instructions:
        registers[instruction[-1]] = opcodes[instruction[0]](instruction[1], instruction[2], registers)

    return registers

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

    impossibles = defaultdict(set)
    for instruction in instructions:
        for name, inst in instrs.iteritems():
            out = inst(instruction['instruction'][1], instruction['instruction'][2], instruction['before'])

            if out != instruction['after'][instruction['instruction'][-1]]:
                impossibles[name].add(instruction['instruction'][0])

    all_opcodes = set(range(len(impossibles)))
    possibles = defaultdict(set)

    for k, v in impossibles.iteritems():
        possibles[k] = all_opcodes.difference(v)

    opcodes = {}

    while len(possibles):
        only_one = [k for k in possibles.keys() if len(possibles[k]) == 1]

        remove_from_possibles = set()
        for each in only_one:
            new_key = possibles[each].pop()
            opcodes[new_key] = instrs[each]
            remove_from_possibles.add(new_key)
            del possibles[each]

        for k, v in possibles.iteritems():
            possibles[k] = v.difference(remove_from_possibles)

    return opcodes


def parse_samples(raw):
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

def parse_instructions(raw):
    return [[int(i) for i in row.split()] for row in raw]

if __name__ == "__main__":
    main()
