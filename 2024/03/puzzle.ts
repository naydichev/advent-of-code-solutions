#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function cleanData(data) {
  let cleaned = "";
  let start = 0;
  let dontIdx = data.indexOf("don't()");

  while (dontIdx !== -1) {
    let doIdx = data.indexOf("do()", dontIdx);
    let newData = data.slice(0, dontIdx);
    if (doIdx !== -1) {
      newData += data.slice(doIdx + 4);
    }
    data = newData;
    dontIdx = data.indexOf("don't()");
  }

  return data;
}

function solvePuzzle(data, partTwo = false) {
  if (partTwo) {
    data = cleanData(data);
  }

  const processed = [...data.matchAll(/mul\((\d+),(\d+)\)/g)].map(([_, x, y]) => ([x, y]));;

  return processed.reduce(
    (acc, [x, y]) => {
      acc += (parseInt(x) * parseInt(y));
      return acc;
    },
    0
  );
}

async function loadPuzzle() {
  const sampleData = `
  xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
  .trim();

  return data;

}

await main({ data: await loadPuzzle() })
