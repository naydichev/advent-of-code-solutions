#!/usr/bin/env python3

from collections import namedtuple

Packet = namedtuple("Packet", "header, value")
Header = namedtuple("Header", "version, type, subpacket")
NumSubpacket = namedtuple("NumSubpacket", "kind, num_packets")
LenSubpacket = namedtuple("LenSubpacket", "kind, len_packets")
LiteralValue = namedtuple("LiteralValue", "kind")

numpacket = lambda x: NumSubpacket("num", x)
lenpacket = lambda x: LenSubpacket("len", x)
litpacket = lambda: LiteralValue("literal")

binary_index = 0

def main():
    binary = parse_input()

    version_total = 0
    for packet in process_packet(binary):
        version_total += packet.header.version

    print(f"The sum of versions is {version_total}")


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


def process_packet(binary):
    global binary_index

    while binary_index < len(binary):
        if binary[binary_index:].count("0") == len(binary[binary_index:]):
            break

        header = parse_header(binary)

        if header.subpacket.kind == "literal":
            value = extract_literal(binary)
            yield Packet(header, value)
        elif header.subpacket.kind == "len":
            length = header.subpacket.len_packets
            yield Packet(header, length)
            for subpacket in process_packet(binary[:binary_index + length]):
                yield subpacket

        elif header.subpacket.kind == "num":
            num = header.subpacket.num_packets
            yield Packet(header, num)

            for subpacket in process_packet(binary):
                yield subpacket

                num -= 1
                if num == 0:
                    break


def parse_input():
    with open("input.aoc") as f:
        data = [x.strip() for x in f.readlines()][0]

    hexint = int(data, 16)
    binint = bin(hexint)[2:].zfill(len(data) * 4)

    return binint


if __name__ == "__main__":
    main()
