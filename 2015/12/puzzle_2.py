#!/usr/bin/env python3

import json
import re



def main(blob):
    numbers = traverse(blob)
    print(f"the sum of all the numbers: {numbers}")


def traverse(blob):
    t = type(blob)
    print(t)

    if t == int:
        return blob
    elif t == list or t == tuple:
        return sum(traverse(x) for x in blob)
    elif t == dict:
        if "red" in blob.values():
            print("found red!")
            return 0
        else:
            return sum(traverse(x) for x in blob.values())

    return 0

if __name__ == "__main__":
    with open("json.pi") as f:
        main(json.load(f))
