#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  if (partTwo) {
    return computeFocalValue(
      arrangeBoxes(
        data[0].split(",")
      )
    );
  }

  return data[0]
    .split(",")
    .map(computeHash)
    .reduce((a, b) => a + b, 0);
}

function computeHash(data) {
  let currentValue = 0;

  for (let i = 0; i < data.length; i++) {
    const asciiValue = data.charCodeAt(i);
    currentValue += asciiValue;
    currentValue *= 17;
    currentValue %= 256;
  }

  return currentValue;
}

function computeFocalValue(boxes) {
  return boxes.map(
    ({ lenses }, bIdx) => lenses.map(
      ({ fl }, lIdx) =>
        [bIdx + 1, lIdx + 1, fl].reduce(
          (a, b) => a * b,
          1
        )
    )
  )
  .reduce((a, b) => a.concat(b), [])
  .filter(n => !isNaN(n))
  .reduce((a, b) => a + b, 0);
}

function arrangeBoxes(data) {
  const boxes = Array.from(
    new Array(256),
    (_, i) => ({ box: i, lenses: [] }),
  );

  data.forEach(raw => {
    let operation;
    let focalLength;
    if (raw.includes("=")) {
      operation = "=";
      focalLength = parseInt(
        raw.slice(
          raw.indexOf(operation) + 1
        )
      );
    } else if (raw.endsWith("-")) {
      operation = "-"
    }

    const label = raw.slice(0, raw.indexOf(operation));;
    const boxIdx = computeHash(label);
    const box = boxes[boxIdx];

    const lenseIdx = box.lenses.findIndex(({ id }) => label === id);
    if (operation === "-") {
      if (lenseIdx >= 0) {
        box.lenses.splice(lenseIdx, 1);
      }
    } else if (operation === "=") {
      if (lenseIdx >= 0) {
        box.lenses[lenseIdx].fl = focalLength;
      } else {
        box.lenses.push({
          id: label,
          fl: focalLength,
        });
      }

    }
  });

  return boxes;
}

async function loadPuzzle() {
  const sampleData = `
  rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
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
