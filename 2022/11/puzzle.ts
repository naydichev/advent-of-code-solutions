#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main() {
  const lines = getPuzzleLines();
  const data = await loadPuzzle(lines);
  const lcd = data.reduce((acc, { testNum: x }) => acc * x, 1n);
  console.log(`Part One: ${solvePuzzle(data, lcd)}`);
  console.log(`Part Two: ${solvePuzzle(await loadPuzzle(lines), lcd, true)}`);
}

function solvePuzzle(data, lcd, partTwo = false) {
  let rounds = partTwo ?
    10000 :
    20;

  const worryRelief = partTwo ?
    1n :
    3n;

  while (rounds--) {
    data.forEach(monkey => {
      while (monkey.items.length) {
        const item = (monkey.operation(monkey.items.shift()) / worryRelief) % lcd;
        let idx = monkey.testPass;
        if (!monkey.test(item)) {
          idx = monkey.testFail;
        }

        data[idx].items.push(item);
        monkey.inspected++;
      }
    });
  }

  const inspections = data.map(m => m.inspected)
    .sort((a, b) => b - a)
    .slice(0, 2)
    .reduce((acc, x) => acc * x, 1);

  return inspections;
}

function getPuzzleLines() {
  const sampleData = `
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
  `;

  return (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());
}

async function loadPuzzle(data) {
  const processed = [];

  let current = null;

  data.forEach(line => {
    const monkeyMatch = line.match(/Monkey (\d+):/);
    if (monkeyMatch) {
      const idx = parseInt(monkeyMatch[1]);
      processed[idx] = {
        monkeyNumber: idx,
        inspected: 0,
      };
      current = processed[idx];
      return;
    }

    const startingMatch = line.match(/Starting items:/);
    if (startingMatch) {
      const items = line.split(/:/)[1]
        .trim()
        .split(",")
        .map(BigInt);
      current.items = items;
      return;
    }

    const operationMatch = line.match(/Operation:/)
    if (operationMatch) {
      const operation = line.split(/:/)[1]
        .trim()
        .split(/=/)[1]
        .trim()
        .split(/ /);


      const op = (operation[2] === "old") ?
        (
          (operation[1] === "+") ?
            (old) => old + old :
            (old) => old * old
        ) :
        (
          (operation[1] === "+") ?
            (old) => old + BigInt(operation[2]) :
            (old) => old * BigInt(operation[2])
        ) ;

      current.operation = op;
      return;
    }

    const testMatch = line.match(/Test:/);
    if (testMatch) {
      const test = line.split(/:/)[1]
        .trim()
        .split(/ /)[2];
      const testNum = BigInt(test);

      current.testNum = testNum;
      current.test = (num) => num % testNum === 0n;
      return;
    }

    const trueMatch = line.match(/If true:/);
    if (trueMatch) {
      const [_throw, _to, _monkey, monkeyNum] = line.split(/:/)[1]
        .trim()
        .split(/ /);

      current.testPass = parseInt(monkeyNum);
      return;
    }

    const falseMatch = line.match(/If false:/);
    if (falseMatch) {
      const [_throw, _to, _monkey, monkeyNum] = line.split(/:/)[1]
        .trim()
        .split(/ /);

      current.testFail = parseInt(monkeyNum);
      return;
    }
  });

  return processed;
}

await main()
