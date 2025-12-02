#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  if (partTwo) { return ; }

  return dtos(
    data.map(s => stod(s))
      .reduce((acc, x) => acc + x, 0)
  );
}

function stod(snafu) {
  let place = 1;
  let total = 0;
  snafu.reverse().forEach(num => {
    if (num === "=") {
      num = -2;
    } else if (num === "-") {
      num = -1;
    }

    total += (num * place);
    place *= 5;
  });
  return total;
}

function dtos(decimal) {
  let place = 1;
  let digits = [];
  while (decimal > 0) {
    let n = decimal % 5;
    if (n <= 2) {
      digits.push(n);
      decimal -= n;
    } else if (n === 3) {
      digits.push("=");
      decimal += 2;
    } else if (n === 4) {
      digits.push("-");
      decimal += 1;
    }

    decimal = Math.floor(decimal / 5);
  }
  return digits.reverse().join("");
}

async function loadPuzzle() {
  const sampleData = `
  1=-0-2
  12111
  2=0=
  21
  2=01
  111
  20012
  112
  1=-1=
  1-12
  12
  1=
  122
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
    .map(s => s.split(""));

  return processed;
}

await main({ data: await loadPuzzle() })
