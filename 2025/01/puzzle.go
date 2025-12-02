package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

const INPUT_FILE = "input.aoc"

var DEBUG = os.Getenv("DEBUG") == "true"
var SAMPLE = os.Getenv("SAMPLE") == "true"

var sample = `L68
L30
R48
L5
R60
L55
L1
L99
R14
L82`

func dbg(args... any) {
	if (DEBUG) {
		fmt.Println(args...)
	}
}

func dbgf(format string, args... any) {
	if (DEBUG) {
		fmt.Printf(format, args...)
	}
}

func puzzleInput() (string, error) {
	if SAMPLE {
		return sample, nil
	}

	data, err := os.ReadFile("input.aoc")
	if err != nil {
		return "", err
	}

	return string(data), nil
}

func mod(a, b int) int {
	return (a % b + b) % b
}

func part1(data string) any {
	dial := 50
	timesPointedAtZero := 0

	for _, line := range strings.Split(data, "\n") {
		dir := string(line[0])
		amount, err := strconv.Atoi(line[1:])
		if err != nil {
			panic(err)
		}

		dbgf("(%-4s) going from %2d %s by %3d", line, dial, dir, amount)
		if dir == "L" {
			dial -= amount
			if dial < 0 {
				dial = mod(dial, 100)
			}
		} else {
			dial += amount
			dial %= 100
		}
		dbg(" ->", dial)

		if dial == 0 {
			timesPointedAtZero += 1
		}
	}

	return timesPointedAtZero
}

func part2(data string) any {
	dial := 50
	timesPointedAtZero := 0

	for _, line := range strings.Split(data, "\n") {
		dir := string(line[0])
		amount, err := strconv.Atoi(line[1:])
		if err != nil {
			panic(err)
		}

		result := dial
		if dir == "L" {
			if result == 0 {
				timesPointedAtZero += amount / 100
			} else if amount >= result {
				timesPointedAtZero += 1 + (amount-result) / 100
			}

			result = mod(result - amount, 100)
		} else if dir == "R" {
			result += amount
			if result > 99 {
				timesPointedAtZero += int(result / 100)
			}
			result %= 100
		}

		dbgf("(%-4s) going from %2d %s by %3d -> %2d (%3d)\n", line, dial, dir, amount, result, timesPointedAtZero)

		dial = result
	}

	return timesPointedAtZero

}


func main() {
	data, err := puzzleInput()
	if err != nil {
		panic(err)
	}

	data = strings.Trim(data, " \n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
