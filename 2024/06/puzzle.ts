#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function findStart(data) {
  for (let y = 0; y < data.length; y++) {
    for (let x = 0; x < data[y].length; x++) {
      if (data[y][x] === "^") {
        return { x, y };
      }
    }
  }
}

const DIRECTIONS = [ "^", ">", "<", "v"];
const MOVE = {
  "^": { dx: 0, dy: -1 },
  ">": { dx: 1, dy: 0 },
  "<": { dx: -1, dy: 0 },
  "v": { dx: 0, dy: 1 },
};

const TURN = {
  "^": ">",
  ">": "v",
  "<": "^",
  "v": "<",
};

function countSpaces(data) {
  let count = 0;
  for (let y = 0; y < data.length; y++) {
    for (let x = 0; x < data[y].length; x++) {
      if (data[y][x] === "X") {
        count++;
      }
    }
  }

  return count;
}

const _key = (x, y) => `${x}-${y}`;

function findObstacles(data) {
  const obstacles = {};

  for (let y = 0; y < data.length; y++) {
    for (let x = 0; x < data[y].length; x++) {
      if (data[y][x] === "#") {
        obstacles[_key(x, y)] = [];
      }
    }
  }

  return obstacles;
}

function walkThePlank(original, [ox, oy] = [-1, -1]) {
  const data = JSON.parse(JSON.stringify(original));

  if (ox !== -1 && oy !== -1) {
    if (data[oy][ox] !== ".") {
      return "ALREADY THERE";
    }
    data[oy][ox] = "#";
  }

  const obstacles = findObstacles(data);

  let { x, y } = findStart(data);
  const height = data.length;
  const width = data[0].length;

  let direction = "^";

  while (true) {
    data[y][x] = "X";
    const { dx, dy } = MOVE[direction];
    const nx = x + dx;
    const ny = y + dy;


    if (nx < 0 || nx >= width || ny < 0 || ny >= height) {
      break;
    }

    const key = _key(nx, ny);
    if (data[ny][nx] === "#") {
      if (obstacles[key].includes(direction)) {
        return "LOOP";
      }

      obstacles[key].push(direction);
      direction = TURN[direction];
    } else {
      x = nx;
      y = ny;
    }
  }

  return data;
}


function solvePuzzle(data, partTwo = false) {
  if (partTwo) {
    let loopCount = 0;
    for (let y = 0; y < data.length; y++) {
      for (let x = 0; x < data[y].length; x++) {
        if (walkThePlank(data, [x, y]) === "LOOP") {
          loopCount++;
        }
      }
    }

    return loopCount;
  }

  const walked = walkThePlank(data);

  const count = countSpaces(walked);

  return count;
}

async function loadPuzzle() {
  const sampleData = `
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
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

  const processed = data;

  return processed;
}

await main({ data: await loadPuzzle() })
