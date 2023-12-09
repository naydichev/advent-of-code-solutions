#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const numbers = data.map(l => l.split(" ").map(Number));

  const result = numbers.map(processNumbers.bind(null, partTwo));
  return result.reduce((a, b) => a + b, 0);
}

function processNumbers(partTwo, numbers) {
  const history = [[...numbers]];

  // down
  while (!history.at(-1).every(n => n === 0)) {
    const current = history.at(-1);
    const next = [];
    for (let i = 1; i < current.length; i++) {
      next.push(current[i] - current[i - 1]);
    }

    history.push(next);
  }

  // up
  let idx = l => l.at(-1)
  let operation = (list, level) => list[level].at(-1) + list[level + 1].at(-1);
  let addValue = (list, value) => list.push(value);
  let result = (list) => list[0].at(-1);

  if (partTwo) {
    operation = (list, level) => list[level][0] - list[level + 1][0];
    addValue = (list, value) => list.unshift(value);
    result = (list) => list[0][0];
  }

  history.at(-1).push(0);
  for (let level = history.length - 2; level >= 0; level--) {
    addValue(history[level], operation(history, level));
  }

  return result(history);
}

async function loadPuzzle() {
  const sampleData = `
  0 3 6 9 12 15
  1 3 6 10 15 21
  10 13 16 21 30 45
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
