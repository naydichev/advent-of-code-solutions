#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  let repeat = (value, sep) => value;
  if (partTwo) {
    repeat = (value, sep) => [0, 0, 0, 0, 0].fill(value, 0, 5).join(sep);
  }


  return data.map(
    line => {
      const [springs, report] = line.split(" ");
      return waysToMake(
        (repeat(springs, "?") + "?").split(""),
        "0," + repeat(report, ","),
      );
    }
  )
  .reduce((a, b) => a + b, 0);
}

function waysToMake(springs, report) {
  const groups = report.split(",").map(Number);
  let ways = [];
  springs.forEach((_, i) => {
    ways[i] = [];
  });

  const checkPrevious = (sIdx, gIdx) => {
    if (sIdx === -1 && gIdx === 0) {
      return 1;
    }

    if (ways[sIdx]) {
      return ways[sIdx][gIdx] ?? 0;
    }

    return 0;
  };

  for (let gIdx = 0; gIdx < groups.length; gIdx++) {
    for(let sIdx = 0; sIdx < springs.length; sIdx++) {
      let current = 0;
      if (springs[sIdx] !== "#") {
        current += checkPrevious(sIdx - 1, gIdx);
      }

      if (gIdx > 0) {
        let count = true;
        for (let p = 1; p <= groups[gIdx]; p++) {
          if (springs[sIdx - p] === ".") {
            count = false;
            break;
          }
        }

        if (springs[sIdx] === "#") {
          count = false;
        }

        if (count) {
          current += checkPrevious(sIdx - groups[gIdx] - 1, gIdx - 1);
        }
      }
      ways[sIdx][gIdx] = current;
    }
  }

  return ways.at(-1).at(-1);
}

function damageRuns(arrangement: string) {
  return [...arrangement.matchAll(/#+/g)].map(m => m[0].length);
}

function arrayEqual(a: number[], b: number[]) {
  return (a.length === b.length && a.every((e, i) => e === b[i]));
}

async function loadPuzzle() {
  const sampleData = `
  ???.### 1,1,3
  .??..??...?##. 1,1,3
  ?#?#?#?#?#?#?#? 1,3,1,6
  ????.#...#... 4,1,1
  ????.######..#####. 1,6,5
  ?###???????? 3,2,1
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
