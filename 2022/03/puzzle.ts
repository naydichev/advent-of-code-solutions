#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  let subject = [];
  if (partTwo) {
    subject = data.reduce((acc, x, i) => {
      const chunkNum = Math.floor(i / 3);
      if (!acc[chunkNum]) {
        acc[chunkNum] = [];
      }

      acc[chunkNum].push(x.whole);

      return acc;
    }, []);
  } else {
    data.forEach(d => subject.push([d.first, d.second]));
  }

  return subject.map(d => {
    return d.reduce((acc, x) => acc.filter(i => x.includes(i)), d[0])[0];
  })
  .map(c => {
    let i = c.charCodeAt(0);
    if (c.toUpperCase() === c) {
      return i - 38;
    } else {
      return i - 96;
    }
  })
  .reduce((acc, x) => acc + x, 0);
}

async function loadPuzzle() {
  const sampleData = `
    vJrwpWtwJgWrhcsFMMfFFhFp
    jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
    PmmdzqPrVvPwwTWBwg
    wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
    ttgJtRGJQctTZtZT
    CrZsJsPPZsGzwwsLwLmpwMDw
  `;
  const data = (
    USE_SAMPLE_DATA ?
      sampleData :
      fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
  .trim()
  .split("\n")
  .map(s => s.trim())
  .map(s => {
    const len = s.length / 2;
    return {
      whole: s.split(""),
      first: s.slice(0, len).split(""),
      second: s.slice(len).split(""),
    }
  });

  const processed = data;

  return processed;
}

await main({ data: await loadPuzzle() })
