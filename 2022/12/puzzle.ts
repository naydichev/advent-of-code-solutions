#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const { grid, start, end } = data;

  const visited = Array.from(
    { length: grid.length },
    (_, y) => Array.from(
      { length: grid[y].length },
      (_, x) => Number.MAX_SAFE_INTEGER
    )
  );

  const dimensions = {
    height: grid.length,
    length: grid[0].length,
  };

  const startingLocations = [[start.x, start.y]];
  const queue = [];
  if (partTwo) {
    grid.forEach((row, y) => {
      row.forEach((val, x) => {
        if (val === 0) {
          startingLocations.push([x, y]);
        }
      });
    });
  }

  startingLocations.forEach(([x, y]) => {
    visited[y][x] = 0;
    queue.push([x, y]);
  });
  visited[start.y][start.x] = 0;

  while (queue.length) {

    const [x, y] = queue.shift();
    const curVal = grid[y][x];
    const curScore = visited[y][x];

    for (let [nx, ny] of computeAdjacent([x, y], dimensions)) {
      const posVal = grid[ny][nx];
      const posScore = visited[ny][nx];

      if (canVisit(curVal, posVal) && curScore + 1 < posScore) {
        visited[ny][nx] = curScore + 1;
        queue.push([nx, ny]);
      }
    }

  }

  return visited[end.y][end.x];
}

function canVisit(current, possible) {
  return possible <= current || (possible - current) === 1;
}

function computeAdjacent([x, y], dimensions) {
  const directions = [
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0],
  ];

  const results = [];

  for (let [dx, dy] of directions) {
    let nx = x + dx;
    let ny = y + dy;

    if (nx >= 0 && ny >= 0 && ny < dimensions.height && nx < dimensions.length) {
      results.push([nx, ny]);
    }
  }

  return results;
}

async function loadPuzzle() {
  const sampleData = `
  Sabqponm
  abcryxxl
  accszExk
  acctuvwj
  abdefghi
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim())
    .map(s => s.split(""));

  let start = {};
  let end = {};
  for (let y = 0; y < data.length; y++) {
    for (let x = 0; x < data[y].length; x++) {
      let num = data[y][x].charCodeAt(0) - 97;

      if (data[y][x] === "S") {
        start = {x, y};
        num = 0;
      } else if (data[y][x] === "E") {
        end = {x, y};
        num = 25;
      }

      data[y][x] = num;
    }
  }

  return {
    grid: data,
    start,
    end,
  }
}

await main({ data: await loadPuzzle() })
