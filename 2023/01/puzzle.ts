#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

const regex = /(?=(zero|one|two|three|four|five|six|seven|eight|nine|\d))/g;

const numMap = {
  0: 0,
  1: 1,
  2: 2,
  3: 3,
  4: 4,
  5: 5,
  6: 6,
  7: 7,
  8: 8,
  9: 9,
  zero: 0,
  one: 1,
  two: 2,
  three: 3,
  four: 4,
  five: 5,
  six: 6,
  seven: 7,
  eight: 8,
  nine: 9,
};

function solvePuzzle(data, partTwo = false) {
  let puzzRegex = /\d/g;
  if (partTwo) {
    puzzRegex = regex;
  }

  const solution = data.map(
    line => {
      const matched = [...line.matchAll(puzzRegex)].map(num => numMap[num[0] || num[1]]);
      const num = Number(`${matched[0]}${matched.at(-1)}`);
      return num;
    }
  )
  .filter(line => line)
  .reduce(
    (acc, x) => acc + x,
    0
  );

  return solution;
}

async function loadPuzzle() {
  const sampleData = `
  two1nine
  eightwothree
  abcone2threexyz
  xtwone3four
  4nineeightseven2
  zoneight234
  7pqrstsixteen
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data;

  return processed;
}

await main({ data: await loadPuzzle() })
