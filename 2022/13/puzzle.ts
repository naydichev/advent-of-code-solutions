#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

enum Order {
  UNKNOWN = "UNKNOWN",
  CORRECT = "CORRECT",
  WRONG = "WRONG",
}

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePartTwo(args.data)}`);
}

function solvePuzzle(data) {
  const correctIndexes = [];

  data.forEach(({ left, right }, idx) => {

    const _left = JSON.parse(left);
    const _right = JSON.parse(right);
    const order = verifyOrder(_left, _right);
    if (order === Order.CORRECT) {
      correctIndexes.push(idx + 1);
    }
  });

  return correctIndexes.reduce((acc, x) => acc + x, 0);
}

function solvePartTwo(data) {
  const allPackets = data
    .map(p => [p.left, p.right])
    .reduce((acc, x) => acc.concat(x), []);

  allPackets.push("[[2]]");
  allPackets.push("[[6]]");

  allPackets.sort((_a, _b) => {
    const a = JSON.parse(_a);
    const b = JSON.parse(_b);

    const result = verifyOrder(a, b);
    if (result === Order.CORRECT) {
      return -1;
    } else if (result === Order.WRONG) {
      return 1;
    } else {
      return 0;
    }
  });

  const p1 = allPackets.indexOf("[[2]]") + 1;
  const p2 = allPackets.indexOf("[[6]]") + 1;

  return p1 * p2;
}

function verifyOrder(left, right): Order {
  while(left.length && right.length) {
    const leftItem = left.shift();
    const rightItem = right.shift();

    const leftType = typeof leftItem;
    const rightType = typeof rightItem;

    if (leftType === "number" && rightType === "number") {
      if (leftItem === rightItem) {
        continue;
      }

      return (leftItem - rightItem) > 0 ?
        Order.WRONG :
        Order.CORRECT;
    } else {
      let correctedLeftItem = leftItem;
      let correctedRightItem = rightItem;

      if (leftType !== "object") {
        correctedLeftItem = [leftItem];
      } else if (rightType !== "object") {
        correctedRightItem = [rightItem];
      }

      const result = verifyOrder(correctedLeftItem, correctedRightItem);
      if (result !== Order.UNKNOWN) {
        return result;
      }
    }
  }

  if (left.length === right.length) {
    return Order.UNKNOWN;
  }

  return (left.length - right.length) > 0 ?
    Order.WRONG :
    Order.CORRECT;
}

async function loadPuzzle() {
  const sampleData = `
  [1,1,3,1,1]
  [1,1,5,1,1]

  [[1],[2,3,4]]
  [[1],4]

  [9]
  [[8,7,6]]

  [[4,4],4,4]
  [[4,4],4,4,4]

  [7,7,7,7]
  [7,7,7]

  []
  [3]

  [[[]]]
  [[]]

  [1,[2,[3,[4,[5,6,7]]]],8,9]
  [1,[2,[3,[4,[5,6,0]]]],8,9]
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n\n")
    .map(s => s.trim());

  const processed = data
    .map(p => {
      const [left, right] = p.split("\n")
        .map(s => s.trim());

      return {
        left,
        right
      };
    });;

  return processed;
}

await main({ data: await loadPuzzle() })
