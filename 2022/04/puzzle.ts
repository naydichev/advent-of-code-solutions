#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function difference(a, b) {
  return a.filter(i => !b.includes(i));
}

function solvePuzzle(data, partTwo = false) {
  return data.filter(
    ([first, second]) => {
      const diff1 = difference(first, second);
      const diff2 = difference(second, first);

      if (partTwo) {
        return (diff1.length !== first.length) ||
          (diff2.length !== second.length);
      }

      return diff1.length == 0 || diff2.length == 0;
    }).length;
}

async function loadPuzzle() {
  const sampleData = `
  2-4,6-8
  2-3,4-5
  5-7,7-9
  2-8,3-7
  6-6,4-6
  2-6,4-8
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
    .map(p => p.split(","))
    .map(
      p => p.map(
        i => i.split("-")
          .map(k => parseInt(k))
        )
        .map(([start, end]) => Array.from(
          { length: end - start + 1 },
          (v, k) => k + start
          )
        )
      );

  return processed;
}

await main({ data: await loadPuzzle() })
