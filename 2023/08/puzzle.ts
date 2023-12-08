#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const [steps, map] = parseData(data);

  if (!partTwo) {
    return findWayHomePartOne(steps, map);
  }

  return findWayHomePartTwo(steps, map);
}

function findWayHomePartOne(steps, map) {
  let current = "AAA";
  let destination = "ZZZ";
  let i = 0;
  while (current !== destination) {
    current = map[current][steps[i % steps.length]];
    i++;
  }

  return i;
}

function findWayHomePartTwo(steps, map) {
  let currents = Object.keys(map)
    .filter(node => node.at(-1) === "A");

  let cycles = currents.map(_ => null);

  let i = 0;
  while (true) {
    currents = currents.map(c => map[c][steps[i % steps.length]]);
    i++;

    currents.forEach((c, idx) => {
      if (c.at(-1) === "Z" && !cycles[idx]) {
        cycles[idx] = i;
      }
    });

    if (cycles.every(c => c)) {
      break;
    }
  }

  return cycles.reduce((a, b) => lcm(a, b), 1);
}

function lcm(a, b) {
  const numerator = a * b;
  const denominator = gcd(a, b);;

  return numerator / denominator;
}

function gcd(a, b) {
  for (let temp = b; b !== 0;) {
    b = a % b;
    a = temp;
    temp = b;
  }
  return a;
}

function parseData(data) {
  const steps = data[0].trim().split("");

  const map = {};
  data.slice(1).forEach(line => {
    if (line.trim() === "") {
      return;
    }

    const [id, conns] = line.split(" = ");
    const [L, R] = conns.slice(1, conns.length - 1).split(", ");

    map[id] = {
      L,
      R,
    };
  });

  return [steps, map];
}

async function loadPuzzle() {
  const sampleData = `
  LR

  11A = (11B, XXX)
  11B = (XXX, 11Z)
  11Z = (11B, XXX)
  22A = (22B, XXX)
  22B = (22C, 22C)
  22C = (22Z, 22Z)
  22Z = (22B, 22B)
  XXX = (XXX, XXX)
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
