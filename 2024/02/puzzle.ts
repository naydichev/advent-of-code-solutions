#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function isSafe(row) {
  let ascending = row[1] - row[0] > 0;
  for (let i = 1; i < row.length; i++) {
    let step = row[i] - row[i - 1];
    if ((step > 0) !== ascending) {
      return false;
    }

    if (1 <= Math.abs(step) && Math.abs(step) <= 3) {
      continue;
    }
    return false;
  }

  return true;
}

function isSafeDampen(row) {
  for (let i = 0; i < row.length; i++) {
    let subRow = row.slice(0, i).concat(row.slice(i + 1));
    if (isSafe(subRow)) {
      return true;
    }
  }

  return false;
}

function solvePuzzle(data, partTwo = false) {
  if (partTwo) {

    return data.filter(row => isSafe(row) || isSafeDampen(row)).length;
  }

  return data.filter(row => isSafe(row)).length;
}

async function loadPuzzle() {
  const sampleData = `
  7 6 4 2 1
  1 2 7 8 9
  9 7 6 2 1
  1 3 2 4 5
  8 6 4 4 1
  1 3 6 7 9
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim())
    .map(line => line.split(" ").map(Number));

  const processed = data;

  return processed;
}

await main({ data: await loadPuzzle() })
