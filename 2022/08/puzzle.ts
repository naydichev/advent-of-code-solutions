#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  const { partOne, partTwo } = solvePuzzle(args.data);
  console.log(`Part One: ${partOne}`);
  console.log(`Part Two: ${partTwo}`);
}

function solvePuzzle(data, partTwo = false) {
  let visible = 0;
  let maxScore = 0;

  for (let y = 0; y < data.length; y++) {
    for (let x = 0; x < data[y].length; x++) {
      if (isVisible(data, x, y)) {
        visible++;
      }

      const score = calculateScore(data, x, y);
      console.log(`(${x}, ${y})[${data[y][x]}] = ${score}`);

      maxScore = Math.max(maxScore, score);
    }
  }

  return {
    partOne: visible,
    partTwo: maxScore
  };
}

function isEdge(grid, x, y) {
  return (
    x === 0 ||
    y === 0 ||
    x === grid[y].length - 1 ||
    y === grid.length - 1
  );
}

function isValid(grid, x, y, value) {
  return value < grid[y][x];
}

function isVisible(grid, x, y) {
  if (isEdge(grid, x, y)) {
    return true;
  }

  const _localValid = isValid.bind(null, grid, x, y);

  const cols = Array.from({ length: grid.length }, (_, i) => grid[i][x]);

  return [
    grid[y].slice(0, x),
    grid[y].slice(x + 1),
    cols.slice(0, y),
    cols.slice(y + 1)
  ]
    .map(v => v.every(_localValid))
    .some(Boolean);

}

function scoreReducer(grid, x, y, { score, shouldStop }, value) {
  if (shouldStop) {
    return { score, shouldStop };
  }

  shouldStop = value >= grid[y][x];
  score++;

  return {
    score,
    shouldStop,
  };
}

function calculateScore(grid, x, y) {
  if (isEdge(grid, x, y)) {
    return 0;
  }

  const _localScoreReducer = scoreReducer.bind(null, grid, x, y);

  const cols = Array.from({ length: grid.length }, (_, i) => grid[i][x]);

  return [
    grid[y].slice(0, x).reverse(),
    grid[y].slice(x + 1),
    cols.slice(0, y).reverse(),
    cols.slice(y + 1)
  ]
    .map(v => v.reduce(_localScoreReducer, { score: 0, shouldStop: false }))
    .map(v => v.score)
    .reduce((acc, x) => acc * x, 1);
}


async function loadPuzzle() {
  const sampleData = `
  30373
  25512
  65332
  33549
  35390
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data
    .map(s => {
      return s.split("")
        .map(Number);
    });;

  return processed;
}

await main({ data: await loadPuzzle() })
