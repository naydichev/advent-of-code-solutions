#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  if (partTwo) { return ; }

  console.log(data);
}

async function loadPuzzle() {
  const sampleData = `
  >>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data[0].split("");

  return processed;
}

await main({ data: await loadPuzzle() })
