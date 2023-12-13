#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const patterns = data.map(
    lines => lines.trim().split("\n").map(v => v.trim())
  );
  if (partTwo) {
    return patterns.map(p => {
      const [originalRows, originalColumns] = findMirrorsInPattern(p);
      const singleLine = p.join("\n").split("");
      for (let idx = 0; idx < singleLine.length; idx++) {
        if (singleLine[idx] === "\n") {
          continue;
        }

        const copy = [...singleLine];
        copy.splice(
          idx,
          1,
          copy[idx] === "#" ? "." : "#"
        );

        let [rows, columns] = findMirrorsInPattern(copy.join("").split("\n"));
        rows = rows.filter(value => !originalRows.includes(value));
        columns = columns.filter(value => !originalColumns.includes(value));
        if (rows.length || columns.length) {
          return (rows[0] ?? 0) * 100 + (columns[0] ?? 0);
        }
      }
    })
    .reduce((a, b) => a + b, 0);
  }

  return patterns.map(p => {
    const [rows, columns] = findMirrorsInPattern(p);
    return (rows[0] ?? 0) * 100 + (columns[0] ?? 0);
  })
  .reduce((a, b) => a + b, 0);
}

function findMirrorsInPattern(pattern) {
  const columns = pattern[0].split("")
    .map(
      (_, i) => pattern.map(line => line[i])
      .join("")
    );

  return [pattern, columns].map(d => findMirrorsInStrings(d));
}

function findMirrorsInStrings(strings) {
  const result = [];
  for (let idx = 1; idx < strings.length; idx++) {
    const length = Math.min(idx, strings.length - idx);
    const left = strings.slice(idx - length, idx);
    const right = strings.slice(idx, idx + length);
    if (left.reverse().join("*") === right.join("*")) {
      result.push(idx);
    }
  }

  return result;
}

async function loadPuzzle() {
  const sampleData = `
  #.##..##.
  ..#.##.#.
  ##......#
  ##......#
  ..#.##.#.
  ..##..##.
  #.#.##.#.

  #...##..#
  #....#..#
  ..##..###
  #####.##.
  #####.##.
  ..##..###
  #....#..#
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n\n")
    .map(s => s.trim());

  const processed = data;

  return processed;
}

await main({ data: await loadPuzzle() })
