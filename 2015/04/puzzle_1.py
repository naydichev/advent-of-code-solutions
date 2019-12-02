#!/usr/bin/env python3

import hashlib

prefix = "ckczppom"
count = 1
hexdigest = ""

while not hexdigest.startswith("00000"):
    md5 = hashlib.md5()
    md5.update(f"{prefix}{count}".encode("utf-8"))
    hexdigest = md5.hexdigest()

    count += 1

print(f"found it in {count - 1} thingies.")
