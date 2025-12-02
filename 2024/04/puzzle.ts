#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function buildOptions(data, x, y, partTwo) {
  let startI = partTwo ? -1 : 0;
  let endI = partTwo ? 2 : 4;
  let targetLength = partTwo ? 3 : 4;
  const rows = data.length;
  const cols = data[0].length;

  let options = [];

  let xtempf = [];
  let xtempb = [];
  let ytempf = [];
  let ytempb = [];
  let pdtempf = [];
  let pdtempb = [];
  let ndtempf = [];
  let ndtempb = [];

  for (let i = startI; i < endI; i++) {
    // horizontal
    let pdx = x + i;
    let ndx = x - i;
    if (pdx >= 0 && pdx < cols) {
      xtempf.push(data[y][pdx]);
    }

    if (ndx >= 0 && ndx < cols) {
      xtempb.push(data[y][ndx]);
    }

    // vertical
    let pdy = y + i;
    let ndy = y - i;

    if (pdy >= 0 && pdy < rows) {
      ytempf.push(data[pdy][x]);
    }

    if (ndy >= 0 && ndy < rows) {
      ytempb.push(data[ndy][x]);
    }
    // positive diagonal
    if (pdx >= 0 && pdy >= 0 && pdx < cols && pdy < rows) {
      pdtempf.push(data[pdy][pdx]);
    }

    if (ndx >= 0 && ndy >= 0 && ndx < cols && ndy < rows) {
      pdtempb.push(data[ndy][ndx]);
    }

    // negative diagonal
    if (pdx >= 0 && ndy >= 0 && pdx < cols && ndy < rows) {
      ndtempf.push(data[ndy][pdx]);
    }

    if (ndx >= 0 && pdy >= 0 && ndx < cols && pdy < rows) {
      ndtempb.push(data[pdy][ndx]);
    }
  }

  let hvOptions = [];
  if (!partTwo) {
    hvOptions = [
      xtempf,
      xtempb,
      ytempf,
      ytempb,
    ];
  }

  hvOptions = hvOptions.concat([
    pdtempf,
    pdtempb,
    ndtempf,
    ndtempb
  ]);

  let reversed = hvOptions.map(s => s.toReversed());

  options = options
    .concat(
      hvOptions.map(s => s.join(""))
    )
    .concat(
      reversed.map(s => s.join(""))
    )
    .filter(s => s.length === targetLength);


  return options;
}

function findXMAS(data, x, y) {
  const options = buildOptions(data, x, y, false);

  return options.filter(s => s === "XMAS")
    .length;
}

function findCrossedMAS(data, x, y) {
  const options = buildOptions(data, x, y, true);
  return options.filter(s => s === "MAS").length > 2 ? 1 : 0;
}

function solvePartTwo(data) {
  let count = 0;
  for (let y = 0; y < data.length; y++) {
    for (let x = 0; x < data[y].length; x++) {
      if (data[y][x] === "A") {
        count += findCrossedMAS(data, x, y);
      }
    }
  }

  return count;
}

function solvePuzzle(data, partTwo = false) {
  let partOneCount = 0;
  let partTwoCount = 0;
  for (let y = 0; y < data.length; y++) {
    for (let x = 0; x < data[y].length; x++) {
      if (data[y][x] === "X") {
        partOneCount += findXMAS(data, x, y);
      } else if (data[y][x] === "A") {
        partTwoCount += findCrossedMAS(data, x, y);
      }
    }
  }

  if (partTwo) {
    return partTwoCount;
  }

  return partOneCount;
}

async function loadPuzzle() {
  const sampleData = `
  MMMSXXMASM
  MSAMXMSMSA
  AMXSXMAAMM
  MSAMASMSMX
  XMASAMXAMM
  XXAMMXXAMA
  SMSMSASXSS
  SAXAMASAAA
  MAMMMXMMMM
  MXMXAXMASX
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
