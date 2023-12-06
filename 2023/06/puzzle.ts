#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  let getNumbers = getNumbersPart1;
  if (partTwo) {
    getNumbers = getNumbersPart2;
  }

  const races = getNumbers(data[0])
    .map(n => ({ time: n }));

  getNumbers(data[1])
    .forEach((n, i) => {
      races[i].distance = n;
    });

  const ways = races.map(calculateWays);

  return ways.reduce((a, b) => a * b, 1);
}

function calculateWays({ time, distance }) {
  let ways = 0;
  for (let i = 0; i <= time; i++) {
    let speed = i;
    let myDistance = speed * (time - i);

    if (myDistance > distance) {
      ways++;
    }
  }

  return ways;
}

const getNumbersPart1 = l => l.split(":")[1]
  .trim()
  .split(" ")
  .filter(n => n)
  .map(Number);

const getNumbersPart2 = l => ([
  Number(
    l.split(":")[1]
    .trim()
    .replaceAll(/\W+/g, "")
  )
]);

async function loadPuzzle() {
  const sampleData = `
  Time:      7  15   30
  Distance:  9  40  200
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
