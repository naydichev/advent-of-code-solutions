#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  const seedNumbers = args.data.shift().split(": ").pop().split(" ").map(Number);
  console.log(`Part One: ${await solvePuzzle([...seedNumbers], args.data)}`);
  console.log(`Part Two: ${await solvePuzzle([...seedNumbers], args.data, true)}`);
}

async function solvePuzzle(seedNumbers, data, partTwo = false) {
  const ranges = [];
  while (seedNumbers.length) {
    const start = seedNumbers.shift();
    const amount = partTwo ? seedNumbers.shift() : 1;
    ranges.push({ start, end: start + amount, kind: "seed" });
  }

  return processRanges(ranges, [...data]);
}

function processRanges(ranges, data) {
  let resultingRanges = [...ranges];

  let source = "seed";
  let dest = "";
  while (data.length) {
    const line = data.shift();
    if (!line) { continue; }

    if (line.includes(":")) {
      resultingRanges.forEach(({ kind }, idx) => {
        if (dest) {
          resultingRanges[idx].kind = dest;
        }
      });

      const mode = line.split(":").shift();
      const [_source, _dest] = mode.split(" ").shift().split("-to-");
      source = _source;
      dest = _dest;
      continue;
    }

    const [destStart, sourceStart, groupLength] = line.split(" ").map(Number);
    resultingRanges = applyRange(
      resultingRanges,
      { source, dest },
      destStart,
      sourceStart,
      groupLength
    );
  }

  return resultingRanges.reduce(
    (acc, range) => Math.min(acc, range.start),
    Number.MAX_SAFE_INTEGER
  );
}

function applyRange(
  ranges,
  { source, dest },
  dStart,
  sStart,
  gLength
) {
  const newRanges = [];

  const sEnd = sStart + gLength;

  ranges.forEach(({ start, end, kind }) => {
    if (kind !== source || (end < sStart) || (start > sEnd)) {
      newRanges.push({ start, end, kind });
      return;
    }

    const intersection = {
      start: Math.max(start, sStart),
      end: Math.min(end, sEnd),
    };

    if (start < intersection.start) {
      newRanges.push({
        start,
        end: intersection.start,
        kind,
      });
    }

    if (end > intersection.end) {
      newRanges.push({
        start: intersection.end,
        end,
        kind,
      });
    }

    const offset = dStart - sStart;
    newRanges.push({
      start: intersection.start + offset,
      end: intersection.end + offset,
      kind: dest
    });
  });
  return newRanges;
}

async function loadPuzzle() {
  const sampleData = `
  seeds: 79 14 55 13

  seed-to-soil map:
    50 98 2
  52 50 48

  soil-to-fertilizer map:
    0 15 37
  37 52 2
  39 0 15

  fertilizer-to-water map:
    49 53 8
  0 11 42
  42 0 7
  57 7 4

  water-to-light map:
    88 18 7
  18 25 70

  light-to-temperature map:
    45 77 23
  81 45 19
  68 64 13

  temperature-to-humidity map:
    0 69 1
  1 0 69

  humidity-to-location map:
    60 56 37
  56 93 4
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
