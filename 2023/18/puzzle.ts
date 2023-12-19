#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const instructions = data.map(
    line => {
      const [_, d, n, hex, p2d] = line.match(/([RDLU]) (\d+) \(#(.{5})(.)\)/);

      return {
        d,
        n,
        hex: parseInt(hex, 16),
        p2d: ["R", "D", "L", "U"][p2d],
      };
    }
  );

  if (partTwo) { return calculateArea(instructions); }

  const grid = makeGrid(instructions);
  fillGrid(grid);

  return Object.values(grid)
    .map(row => Object.values(row).filter(value => value === "#").length)
    .reduce((a, b) => a + b, 0);
}

const D = {
  R: [1, 0],
  L: [-1, 0],
  U: [0, -1],
  D: [0, 1],
};

function calculateArea(instructions) {
  let area = 0;
  let perimeter = 0;
  let x = 0;
  let y = 0;

  instructions.forEach(({ hex, p2d }) => {
    perimeter += hex;
    let a = null;
    switch (p2d) {
      case "R":
        a = (y * hex / 2);
        x += hex;
        break;
      case "L":
        a = (y * -hex / 2);
        x -= hex;
        break;
      case "U":
        a = (x * hex / 2);
        y -= hex;
        break;
      case "D":
        a = (x * -hex / 2);
        y += hex;
        break;
    }

    area += a;
  });

  return Math.abs(area) + (perimeter / 2) + 1;
}

function makeGrid(instructions) {
  let current = [0, 0];
  let grid = { 0: { 0: "#" } };

  instructions.forEach(
    ({ d, n }) => {
      let i = n;
      while (i > 0) {
        current = [current[0] + D[d][0], current[1] + D[d][1]];
        if (!grid[current[1]]) {
          grid[current[1]] = {};
        }

        grid[current[1]][current[0]] = "#";
        i--;
      }
    }
  );

  return grid;
}

const min = (list) => list.reduce((a, b) => Math.min(a, b), Number.MAX_SAFE_INTEGER);
const max = (list) => list.reduce((a, b) => Math.max(a, b), Number.MIN_SAFE_INTEGER);

function bounds(grid) {
  const yKeys = Object.keys(grid);
  const yMin = min(yKeys);
  const yMax = max(yKeys);

  const xKeys = Object.values(grid)
    .map(row => Object.keys(row))
    .reduce((a, b) => a.concat(b), []);;
  const xMin = min(xKeys);
  const xMax = max(xKeys);

  return {
    xMin,
    xMax,
    yMin,
    yMax,
  };
}

function pad(val, num) {
  val = `${val} `;
  while (val.length < num) {
    val = ` ${val}`;
  }

  return val;
}

function printGrid(grid) {
  const {
    xMin,
    xMax,
    yMin,
    yMax,
  } = bounds(grid);

  for (let y = yMin; y <= yMax; y++) {
    if (!grid[y]) {
      grid[y] = {};
    }
    let line = [pad(y, 4)];

    for (let x = xMin; x <= xMax; x++) {
      line.push(grid[y][x] ?? ".");
    }

    console.log(line.join(""));
  }
}

function fillGrid(grid) {
  const {
    xMin,
    xMax,
    yMin,
    yMax,
  } = bounds(grid);

  const firstHash = Object.keys(grid[yMin])
    .sort((k1, k2) => k1 - k2)[0];

  const queue = [[parseInt(firstHash) + 1, yMin + 1]];

  let i = 0;
  while (queue.length) {
    i++;

    const [x, y] = queue.shift();

    if (!grid[y]) {
      grid[y] = {};
    }

    if (grid[y][x] === "#") {
      continue;
    }

    grid[y][x] = "#";

    [
      [0, 1],
      [0, -1],
      [-1, 0],
      [1, 0],
    ].forEach(([dx, dy]) => {
      let nx = x + dx;
      let ny = y + dy;

      queue.push([nx, ny])
    });
  }
}

async function loadPuzzle() {
  const sampleData = `
  R 6 (#70c710)
  D 5 (#0dc571)
  L 2 (#5713f0)
  D 2 (#d2c081)
  R 2 (#59c680)
  D 2 (#411b91)
  L 5 (#8ceee2)
  U 2 (#caa173)
  L 1 (#1b58a2)
  U 2 (#caa171)
  R 2 (#7807d2)
  U 3 (#a77fa3)
  L 2 (#015232)
  U 2 (#7a21e3)
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
