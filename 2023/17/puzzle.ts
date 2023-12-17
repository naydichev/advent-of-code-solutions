#!bun

import * as fs from "fs";
import Heap from "heap-js";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const grid = data.map(
    (row) => row.split("").map(Number)
  );

  const filterFunc = (s, d) => ([nx, ny, nd]) => {
    if (partTwo) {
      if (s < 4) {
        return d === nd;
      } else if (s > 9) {
        return d !== nd;
      }
      return true;
    }

    return s > 2 ? d !== nd : true;
  };

  const checkFunc = (s) => partTwo ? s >= 4 : true;

  return traverse(grid, filterFunc, checkFunc);
}

enum D {
  N = "N",
  E = "E",
  W = "W",
  S = "S",
};

const DDelta = {
  [D.N]: [0, -1],
  [D.E]: [1, 0],
  [D.W]: [-1, 0],
  [D.S]: [0, 1],
};


function traverse(grid, filterFunc, checkFunc) {
  let current = [0, 0];
  let endX = grid.at(-1).length - 1;
  let endY = grid.length - 1;

  const heap = new Heap(
    ({ z: a }, { z: b }) => a - b
  );
  const visited = new Set();

  [D.S, D.E].forEach(d => {
    const obj = {
      x: 0,
      y: 0,
      d,
      v: 0,
      s: 0,
      z: 0,
    };

    heap.push(obj);

    visited.add(toStr(obj));
  });

  while (heap.size() > 0) {
    const { x, y, d, v, s } = heap.pop();

    if (x === endX && y === endY) {
      if (checkFunc(s)) {
        return v;
      }
    }

    const adjacents = getAdjacent([x, y], d)
      .filter(filterFunc(s, d))
      // .filter(([nx, ny, nd]) => s > 2 ? d !== nd : true)
      .filter(([nx, ny]) => nx >= 0 && nx <= endX && ny >= 0 && ny <= endY);


    adjacents.forEach(([nx, ny, nd]) => {
      const obj = {
        x: nx,
        y: ny,
        d: nd,
        v: grid[ny][nx] + v,
        s: d === nd ? s + 1 : 1,
        z: grid[ny][nx] + v + (endX - nx) + (endY - ny),
      };

      const str = toStr(obj);
      if (!visited.has(str)) {
        visited.add(str);
        heap.push(obj);
      }
    });

  }

  return -1;
}

function toStr({ x, y, d, s }) {
  return `[${x},${y}]${d}|${s}`;
}

function getAdjacent([x, y], dir: D) {
  let exclude = D.S;
  switch (dir) {
    case D.E:
      exclude = D.W;
      break;
    case D.W:
      exclude = D.E;
      break;
    case D.S:
      exclude = D.N;
      break;
  }

  return Object.entries(DDelta)
    .filter(([key]) => key !== exclude)
    .map(([d, [dx, dy]]) => ([x + dx, y + dy, d]));
}


async function loadPuzzle() {
  const sampleData = `
  2413432311323
  3215453535623
  3255245654254
  3446585845452
  4546657867536
  1438598798454
  4457876987766
  3637877979653
  4654967986887
  4564679986453
  1224686865563
  2546548887735
  4322674655533
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
