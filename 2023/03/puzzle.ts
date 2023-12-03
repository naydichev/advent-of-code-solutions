#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

const DIRECTIONS = [
  [0, -1],
  [0, 1],
  [-1, 0],
  [1, 0],
  [-1, -1],
  [-1, 1],
  [1, 1],
  [1, -1],
];

function solvePuzzle(data, isPartTwo = false) {
  const matrix = data.map(line => line.split(""));
  let numbersToSum;
  if (!isPartTwo) {
    numbersToSum = partOne(matrix);
  } else {
    numbersToSum = partTwo(matrix);
  }

  return numbersToSum.reduce((a, b) => a + b, 0);
}

function partOne(matrix) {
  const numbersToSum = [];
  matrix.forEach((line, y) => {
    let currentDigit = [];
    let hasSymbol = false;

    line.forEach((element, x) => {
      if (isNaN(element)) {
        if (!currentDigit.length) { return; }
        if (currentDigit.length && hasSymbol) {
          numbersToSum.push(parseInt(currentDigit.join("")));
        }

        currentDigit = [];
        hasSymbol = false;

        return;
      }

      currentDigit.push(element);
      if (!hasSymbol) {
        [-1, 0, 1].forEach(dx => {
          [-1, 0, 1].forEach(dy => {
            let nX = x + dx;
            let nY = y + dy;
            if (nX < 0 || nY < 0 || nX >= matrix.length || nY >= line.length) {
              return;
            }

            const value = matrix[nX][nY];
            if (value !== "." && isNaN(value)) {
              hasSymbol = true;
            }
          });
        });
      }
    });

    if (hasSymbol && currentDigit.length) {
      numbersToSum.push(parseInt(currentDigit.join("")));
    }
  });

  return numbersToSum;
}

function partTwo(matrix) {
  const numbersToSum = [];

  matrix.forEach((line, y) => {
    line.forEach((element, x) => {
      if (element !== "*") { return; }

      const adjacentNumbers = findAdjacentNumbers(matrix, x, y);
      if (adjacentNumbers.length === 2) {
        numbersToSum.push(adjacentNumbers.reduce((a, b) => a * b, 1));
      }
    });
  });

  return numbersToSum;
}

function findAdjacentNumbers(matrix, x, y) {
  const numbers = new Set();
  [-1, 0, 1].forEach((dx) => {
    [-1, 0, 1].forEach((dy) => {
      const nx = x + dx;
      const ny = y + dy;
      if (ny < 0 || ny >= matrix.length || nx < 0 || nx >= matrix[ny].length) {
        return;
      }

      if (!isNaN(matrix[ny][nx])) {
        // look left, and look right
        let xmin = nx;
        let xmax = nx;
        while (!isNaN(matrix[ny][xmin])) {
          xmin--;
        }

        while (!isNaN(matrix[ny][xmax])) {
          xmax++;
        }

        const num = parseInt(matrix[ny].slice(xmin + 1, xmax).join(""));
        numbers.add(num);
      }
    });
  });

  return Array.from(numbers);
}

async function loadPuzzle() {
  const sampleData = `
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
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
