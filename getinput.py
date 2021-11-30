#!/usr/bin/env python3
import argparse
import requests
import os, os.path


def main(args):
    destination_parts = [
        args.aoc_path,
        str(args.year),
        f"{args.day:02}"
    ]

    destination = "/".join(destination_parts)
    print(f"Ensuring destination exists: {destination}")
    for i in range(len(destination_parts)):
        path = "/".join(destination_parts[0:i + 1])
        if not os.path.exists(path):
            os.mkdir(path, mode=0o755)

    session = requests.Session()

    requests.utils.add_dict_to_cookiejar(session.cookies, dict(session=args.session_token))

    event_url = f"https://adventofcode.com/{args.year}/day/{args.day}"

    print(f"Getting todays puzzle input")
    r = session.get(f"{event_url}/input", stream=True)
    r.raise_for_status()

    print(f"Saving to {destination}/input.aoc")
    with open(f"{destination}/input.aoc", "wb") as f:
        for content in r.iter_content():
            f.write(content)

    if args.open:
        os.system(f"open {event_url}")


def parse_args():
    parser = argparse.ArgumentParser(description="Utility to get input from Advent of Code")
    parser.add_argument("--aoc-path", help="The path to Advent of Code")
    parser.add_argument("--session-token", help="Session token override.")
    parser.add_argument("--day", "-d", type=int, help="Which day to get the input for, defaults to 'today'")
    parser.add_argument("--year", "-y", type=int, help="Which year to get the input for, defaults to 'this year'")
    parser.add_argument("--open", "-o", action="store_true", help="Whether or not to open the URL")

    args = parser.parse_args()

    fill_in_default_args(args)

    return args


def fill_in_default_args(args):
    from datetime import datetime

    today = datetime.today()

    if not args.year:
        args.year = today.year

    if not args.day:
        args.day = today.day

    if not args.session_token:
        with open(os.path.expanduser("~/.secrets")) as f:
            for line in f.readlines():
                parts = line.strip().split("=")
                key = parts[0]
                val = "=".join(parts[1:])

                if key == "ADVENT_OF_CODE_SESSION_TOKEN":
                    args.session_token = val

    if not args.aoc_path:
        args.aoc_path = "~/Projects/advent-of-code-solutions"

    args.aoc_path = os.path.expanduser(args.aoc_path)


if __name__ == "__main__":
    main(parse_args())
