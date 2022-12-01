#!bun

import * as fs from "fs";

async function main(args) {
  console.log(`Part one: ${solvePuzzle(args.data)}`);
  console.log(`Part one: ${solvePuzzle(args.data, 3)}`);
}

function solvePuzzle(data, size = 1) {
  let sums = [];
  let sum = 0;

  data.forEach((value) => {
    if (value === "") {
      sums.push(sum);
      sum = 0;
      return;
    }

    sum += parseInt(value);
  });

  return sums
  .sort((a, b) => b - a)
  .slice(0, size)
  .reduce((acc, x) => acc + x, 0);
}

async function loadPuzzle() {
  const data = await fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  .split("\n")
  .map(s => s.trim());

  const processed = data;

  return processed;
}

await main({ data: await loadPuzzle() })
