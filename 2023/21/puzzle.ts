#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  if (partTwo) { return ; }

  const [start, grid] = parseGrid(data);
  grid[start[1]][start[0]].garden = true;

  return walkSteps(grid, start, 64);
}

function walkSteps(grid, start, num) {
  const queue = [[...start, 0]];

  while (queue.length) {
    let [x, y, n] = queue.shift();

    if (y < 0 || y >= grid.length || x < 0 || x >= grid[y].length || n > num) {
      continue;
    }

    let p = grid[y][x];
    if (!p.garden) {
      continue;
    }

    p.visited = n;

    [[0, 1], [0, -1], [1, 0], [-1, 0]].forEach(([dx, dy]) => {
      queue.push([x + dx, y + dy, n + 1]);
    });
  }

  // printGrid(grid, `after ${num} steps`);

  return grid.map(
    row => row.filter(v => v.visited === num).length
  ).reduce((a, b) => a + b, 0);

}


function parseGrid(data) {
  let start = [];
  const grid = [];

  data.forEach((line, y) => {
    grid.push([]);
    line.split("")
      .forEach((val, x) => {
      if (val === "S") {
        start = [x, y];
      }

      grid[y].push({
        x,
        y,
        garden: val === ".",
        visited: undefined,
      });

    });
  });

  return [start, grid];
}

function printGrid(grid, msg = null) {
  if (msg) {
    console.log(msg);
  }
  grid.forEach(row => {
    const mapped = row.map(val => {
      if (!val.garden && val.visited !== 0) {
        return "#";
      }

      if (!isNaN(val.visited)) {
        return `${blue}${val.visited}${white}`;
      } else {
        return `${red}.${white}`;
      }
    }).join("");

    console.log(mapped);
  });
}

async function loadPuzzle() {
  const sampleData = `
  ...........
  .....###.#.
  .###.##..#.
  ..#.#...#..
  ....#.#....
  .##..S####.
  .##..#...#.
  .......##..
  .##.#.####.
  .##..##.##.
  ...........
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
