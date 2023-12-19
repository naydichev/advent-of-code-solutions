#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const grid = data.map(
    (line, y) => line.split("")
      .map((char, x) => ({
        space: char,
        type: "#O".includes(char) ? "rock" : "empty",
        moves: "O" === char,
        x,
        y,
      }))
  );

  if (partTwo) {
    performCycles(grid, 1000000000);
  } else {
    slideRocks(grid, "N");
  }

  const result = grid.reverse()
    .map((row, y) => (row.filter(v => v.space === "O").length * (y + 1)))
    .reduce((a, b) => a + b, 0);

    return result;
}

const str = (grid) => grid.map(row => row.map(({ space }) => space).join("")).join("");

function performCycles(grid, numRemaining) {
  const tracker = {};
  let i = 1;

  while (i <= numRemaining) {
    slideRocks(grid, "N");
    slideRocks(grid, "W");
    slideRocks(grid, "S");
    slideRocks(grid, "E");

    const _str = str(grid);
    if (_str in tracker) {
      const diff = i - tracker[_str];
      let newCycleCount = (numRemaining - i) % diff;
      return performCycles(grid, newCycleCount);
    } else {
      tracker[_str] = i;
    }

    i++;
  }
}

function printGrid(grid, msg = null) {
  if (msg) {
    console.log(msg);
  }
  grid.forEach(row => {
    const mapped = row.map(val => {
      switch (val.space) {
        case ".":
          return ".";
        case "#":
          return `${blue}#${white}`;
        case "O":
          return `${red}O${white}`;
      }
    }).join("");

    console.log(mapped);
  });
}

const DIRECTIONS = {
  N: {
    dyf: (grid) => grid.map((_, i) => i),
    dxf: (grid, y) => grid[y].map((_, i) => i),
    d: [0, -1]
  },
  E: {
    dyf: (grid) => grid.map((_, i) => i),
    dxf: (grid, y) => grid[y].map((_, i) => i).reverse(),
    d: [1, 0],
  },
  W: {
    dyf: (grid) => grid.map((_, i) => i),
    dxf: (grid, y) => grid[y].map((_, i) => i),
    d: [-1, 0],
  },
  S: {
    dyf: (grid) => grid.map((_, i) => i).reverse(),
    dxf: (grid, y) => grid[y].map((_, i) => i),
    d: [0, 1],
  },
};

function slideRocks(grid, dir) {
  const { d: [dx, dy], dyf, dxf } = DIRECTIONS[dir];

  for (let y of dyf(grid)) {
    const row = grid[y];
    for (let x of dxf(grid, y)) {
      const val = row[x];
      if (val.type === "empty" || !val.moves) {
        continue;
      }

      const inBounds = (bx, by) => (by >= 0 && by < grid.length)
        && (bx >= 0 && bx < grid[0].length);

      let ny = y;
      let nx = x
      while (inBounds(nx + dx, ny + dy)) {
        nx += dx;
        ny += dy;

        if (grid[ny][nx].type !== "empty") {
          nx -= dx;
          ny -= dy;
          break;
        }
      }

      if ((ny !== y || nx !== x) && inBounds(nx, ny) && grid[ny][nx].type === "empty") {
        grid[ny][nx] = grid[y][x];
        grid[y][x] = {
          space: ".",
          type: "empty",
          moves: false,
          x,
          y,
        };
      }
    }
  }
}

async function loadPuzzle() {
  const sampleData = `
  O....#....
  O.OO#....#
  .....##...
  OO.#O....O
  .O.....O#.
  O.#..O.#.#
  ..O..#O..O
  .......O..
  #....###..
  #OO..#....
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

const black = "\x1b[30m";
const red = "\x1b[31m";
const green = "\x1b[32m";
const yellow = "\x1b[33m";
const blue = "\x1b[34m";
const magenta = "\x1b[35m";
const cyan = "\x1b[36m";
const white = "\x1b[37m";
const bold = "\033[1m";
const underline = "\033[4m";
const normal = "\033[0m";

await main({ data: await loadPuzzle() })
