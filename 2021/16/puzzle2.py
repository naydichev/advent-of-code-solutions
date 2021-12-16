#!/usr/bin/env python3

from collections import namedtuple
from functools import reduce


Packet = namedtuple("Packet", "header, value, depth")
Header = namedtuple("Header", "version, type, subpacket")
NumSubpacket = namedtuple("NumSubpacket", "kind, num_packets")
LenSubpacket = namedtuple("LenSubpacket", "kind, len_packets")
LiteralValue = namedtuple("LiteralValue", "kind")

numpacket = lambda x: NumSubpacket("num", x)
lenpacket = lambda x: LenSubpacket("len", x)
litpacket = lambda: LiteralValue("literal")

binary_index = 0

def main(override=None):
    global binary_index

    binary = parse_input(override)

    binary_index = 0
    for packet in process_packet(binary):
        print(packet)

    print(f"The final value is {packet.value}")


def gslice(length, take=True):
    global binary_index

    s = slice(binary_index, binary_index + length)
    if take:
        binary_index += length

    return s


def parse_header(binary):
    version = int(binary[gslice(3)], 2)

    packet_type = int(binary[gslice(3)], 2)

    subpacket = litpacket()
    if packet_type != 4:
        subpacket_type = int(binary[gslice(1)])

        if subpacket_type == 0:
            subpacket = lenpacket(int(binary[gslice(15)], 2))
        else:
            subpacket = numpacket(int(binary[gslice(11)], 2))

    return Header(version, packet_type, subpacket)


def extract_literal(binary):

    bits = []
    while True:
        section = binary[gslice(5)]

        bits.extend(section[1:])
        if section[0] == "0":
            break

    return int("".join(bits), 2)


def process_packet(binary, depth=0):
    global binary_index

    while binary_index < len(binary):
        if binary[binary_index:].count("0") == len(binary[binary_index:]):
            break

        header = parse_header(binary)

        if header.subpacket.kind == "literal":
            value = extract_literal(binary)
            yield Packet(header, value, depth)
        elif header.subpacket.kind == "len":
            length = header.subpacket.len_packets
            values = []
            for subpacket in process_packet(binary[:binary_index + length], depth + 1):
                if subpacket.depth == depth + 1:
                    values.append(subpacket.value)
                yield subpacket

            yield Packet(header, calculate_value_for_type(header, values), depth)

        elif header.subpacket.kind == "num":
            num = header.subpacket.num_packets

            values = []
            for subpacket in process_packet(binary, depth + 1):
                if subpacket.depth == depth + 1:
                    values.append(subpacket.value)
                    num -= 1
                yield subpacket

                if num == 0:
                    break

            yield Packet(header, calculate_value_for_type(header, values), depth)


def calculate_value_for_type(header, values):
    packet_type = header.type
    if packet_type == 0:
        return sum(values)
    elif packet_type == 1:
        return reduce(lambda x, y: x * y, values, 1)
    elif packet_type == 2:
        return min(values)
    elif packet_type == 3:
        return max(values)
    # 4 is literal and handled above
    elif packet_type == 5:
        if len(values) != 2:
            raise ValueError(header, values)

        if values[0] > values[1]:
            return 1
        else:
            return 0
    elif packet_type == 6:
        if len(values) != 2:
            raise ValueError(header, values)

        if values[0] < values[1]:
            return 1
        else:
            return 0
    elif packet_type == 7:
        if len(values) != 2:
            raise ValueError(header, values)

        if values[0] == values[1]:
            return 1
        else:
            return 0



def parse_input(override=None):
    if override:
        print(f"Override: {override}")
        data = override
    else:
        with open("input.aoc") as f:
            data = [x.strip() for x in f.readlines()][0]

    hexint = int(data, 16)
    binint = bin(hexint)[2:].zfill(len(data) * 4)

    return binint


if __name__ == "__main__":

    main("C200B40A82")
    main("04005AC33890")
    main("880086C3E88112")
    main("CE00C43D881120")
    main("D8005AC2A8F0")
    main("F600BC2D8F")
    main("9C005AC2F8F0")
    main("9C0141080250320F1802104A08")
    main()
