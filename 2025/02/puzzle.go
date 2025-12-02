package main

import (
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

const INPUT_FILE = "input.aoc"
var DEBUG = os.Getenv("DEBUG") == "true"
var USE_SAMPLE = os.Getenv("SAMPLE") == "true"

var sample = `
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
`

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
	if USE_SAMPLE {
		return sample, nil
	}

	data, err := os.ReadFile(INPUT_FILE)
	if err != nil {
		return "", err
	}

	return string(data), nil
}

func sum(values []int) int {
	total := 0
	for _, v := range values {
		total += v
	}

	return total
}

func hasDuplicates(value string, partOne bool) bool {
	stringLength := len(value)
	splits := []int{2}

	if !partOne {
		splits = []int{}

		for i := 2; i <= stringLength; i++ {
			if stringLength % i == 0 {
				splits = append(splits, i)
			}
		}
	}

	for _, v := range splits {
		chunkLength := stringLength / v
		chunks := []string{}
		for i := 0; i < v; i++ {
			chunks = append(chunks, value[chunkLength * i:chunkLength * (i + 1)])
		}

		dbgf("value (%s) split into %d chunks of length %d = %s\n", value, v, chunkLength, chunks)
		if allEqual(chunks) {
			dbg("All equal!")
			return true
		}
	}

	return false
}

func allEqual(values []string) bool {
	for _, v := range values {
		if v != values[0] {
			return false
		}
	}

	return true
}


func solvePuzzle(data string, isPartOne bool) any {
	if isPartOne {
		dbg("Starting part 1")
	} else {
		dbg("Starting part 2")
	}

	data = strings.ReplaceAll(data, "\n", "")
	duplicates := []int{}
	for _, productIdRanges :=  range strings.Split(data, ",") {
		idParts := strings.Split(productIdRanges, "-")
		startId, err := strconv.Atoi(idParts[0])
		if err != nil {
			panic(err)
		}
		endId, err := strconv.Atoi(idParts[1])
		if err != nil {
			panic(err)
		}

		for i := startId; i <= endId; i++ {
			strVal := strconv.Itoa(i)
			if hasDuplicates(strVal, isPartOne) {
				dbgf("\t%s is a duper\n", strVal)
				duplicates = append(duplicates, i)
			}
		}
	}

	dbgf("duplicates = %v\n", duplicates)
	return sum(duplicates)
}

func main() {
	DEBUG = slices.Contains(os.Args, "debug")
	USE_SAMPLE = slices.Contains(os.Args, "sample")
	data, err := puzzleInput()
	if err != nil {
		panic(err)
	}

	data = strings.Trim(data, " \n")

	fmt.Println("Part 1:", solvePuzzle(data, true))
	fmt.Println("Part 2:", solvePuzzle(data, false))

}
