#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePartTwo(left, right) {
  const counts = {};

  right.forEach(val => {
    if (!counts[val]) {
      counts[val] = 0;
    }

    counts[val]++;
  });

  let sum = 0;

  left.forEach(val => {
    sum += val * (counts[val] ?? 0);
  });

  return sum;
}

function solvePuzzle(data, partTwo = false) {
  let left = [];
  let right = [];

  data.forEach(([_l, _r]) => {
    left.push(_l);
    right.push(_r);
  });

  left.sort();
  right.sort();

  if (partTwo) {
    return solvePartTwo(left, right);
  }

  let dist = 0
  for (let i = 0; i < left.length; i++) {
    dist += Math.abs(left[i] - right[i]);
  }

  return dist;
}

async function loadPuzzle() {
  const sampleData = `
  > DATA HERE <
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim())
    .map(s => s.split(/\s+/).map(Number));

  const processed = data;

  return processed;
}

await main({ data: await loadPuzzle() })
