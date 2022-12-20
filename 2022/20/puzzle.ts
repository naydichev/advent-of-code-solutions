#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  let times = 1;

  if (partTwo) {
    times = 10;
    data = data.map(({ num, i }) => {
      return {
        num: num * 811589153,
        i,
      };
    });
  }

  return mix(data, times)
}

function mix(data, times = 1) {
  const zeroIdx = data.findIndex(({ num }) => num === 0);

  let copy = data.slice(zeroIdx + 1)
    .concat(data.slice(0, zeroIdx));

  let length = copy.length;
  while (times) {
    data.forEach(({ num, i }) => {
      if (num === 0) {
        return;
      }

      let index = copy.findIndex(({ i: x }) => x === i);
      let newIndex = (((index + num) % length) + (length * 999)) % length;
      let item = copy.splice(index, 1)[0];
      copy.splice(newIndex, 0, item);
    });
    times--;
  }
  copy.unshift({num: 0, i: -1});

  return [1000, 2000, 3000]
    .map(index => copy[index % length].num)
    .reduce((acc, x) => acc + x, 0);
}

async function loadPuzzle() {
  const sampleData = `
  1
  2
  -3
  3
  -2
  0
  4
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data.map(Number)
    .map((num, i) => ({
      num,
      i
    }));

  return processed;
}

await main({ data: await loadPuzzle() })
