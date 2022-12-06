#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(Array.from(args.data))}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  let size = partTwo ?
    14 :
    4;
  const packets = data.splice(0, size);

  for (let i = 0; i < data.length; i++) {
    if (new Set(packets).size == size) {
      return i + size;
    }

    packets.shift()
    packets.push(data[i])
  }
}

async function loadPuzzle() {
  const sampleData = `
  mjqjpqmgbljsphdztnvjfqwrcgsmlb
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data[0].split("");

  return processed;
}

await main({ data: await loadPuzzle() })
