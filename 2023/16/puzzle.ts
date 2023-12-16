#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {

  if (partTwo) {
    return followAllBeams(data)
      .reduce((a, b) => Math.max(a, b), 0);;
  }

  const grid = parseGrid(data);

  followBeams(grid);

  return computeEnergized(grid);
}

enum Direction {
  Up = "^",
  Down = "v",
  Left = "<",
  Right = ">",
}

const movement = {
  [Direction.Up]: [0, -1],
  [Direction.Down]: [0, 1],
  [Direction.Left]: [-1, 0],
  [Direction.Right]: [1, 0],
};

function followAllBeams(data) {
  const results = [];
  const ys = [0, data.length];
  const xs = [0, data[0].length];

  // top
  for (let x = 0; x < xs[1]; x++) {
    let tGrid = parseGrid(data);
    let beamStartT = {
      x,
      y: ys[0] - 1,
      d: Direction.Down,
    };

    followBeams(
      tGrid,
      [beamStartT],
    );

    results.push(computeEnergized(tGrid));

    let bGrid = parseGrid(data);
    let beamStartB = {
      x,
      y: ys[1],
      d: Direction.Up,
    };

    followBeams(
      bGrid,
      [beamStartB],
    );

    results.push(computeEnergized(bGrid));
  }

  for (let y = 0; y < ys[1]; y++) {
    let lGrid = parseGrid(data);
    let beamStartL = {
      x: xs[0] - 1,
      y,
      d: Direction.Right,
    };

    followBeams(
      lGrid,
      [beamStartL],
    );

    results.push(computeEnergized(lGrid));

    let rGrid = parseGrid(data);
    let beamStartR = {
      x: xs[1],
      y,
      d: Direction.Left,
    };
    followBeams(
      rGrid,
      [beamStartR],
    );

    results.push(computeEnergized(rGrid));
  }

  return results;
}

function computeEnergized(grid) {
  return grid.map(
    row => row.filter(
      item => item.visited.length > 0
    ).length
  ).reduce((a, b) => a + b, 0);
}

function followBeams(grid, beams = [{ x: -1, y: 0, d: Direction.Right }]) {
  while (beams.length) {

    const { x, y, d } = beams.shift();

    const [dx, dy] = movement[d];
    const [nx, ny] = [x + dx, y + dy];

    if (ny < 0 || ny >= grid.length || nx < 0 || nx >= grid[0].length) {
      continue;
    }

    const point = grid[ny][nx];
    if (point.visited.includes(d)) {
      continue;
    }

    point.visited.push(d);
    const kind = point.kind;
    let nd = d;

    if (["/","\\"].includes(kind)) {
      if (
        (kind === "/" && d === Direction.Up)
      || (kind === "\\" && d === Direction.Down)
      ) {
        nd = Direction.Right;
      } else if (
        (kind === "/" && d === Direction.Down)
      || (kind === "\\" && d === Direction.Up)
      ) {
        nd = Direction.Left;
      } else if (
        (kind === "/" && d === Direction.Left)
      || (kind === "\\" && d === Direction.Right)
      ) {
        nd = Direction.Down;
      } else if (
        (kind === "/" && d === Direction.Right)
      || (kind === "\\" && d === Direction.Left)
      ) {
        nd = Direction.Up;
      }
    } else if (kind === "|" && [Direction.Left, Direction.Right].includes(d)) {
      beams.push(
        {
          x: nx,
          y: ny,
          d: Direction.Up,
        },
        {
          x: nx,
          y: ny,
          d: Direction.Down,
        },
      );
      continue;
    } else if (kind === "-" && [Direction.Up, Direction.Down].includes(d)) {
      beams.push(
        {
          x: nx,
          y: ny,
          d: Direction.Left,
        },
        {
          x: nx,
          y: ny,
          d: Direction.Right,
        },
      );
      continue;
    }

    beams.push({
      x: nx,
      y: ny,
      d: nd,
    });
  }
}

function printGrid(grid) {
  grid.map((row) =>
    row.map(
      ({ visited, kind }) => {
        let pchar = kind;
        let cchar = white;
        if (visited.length > 1) {
          if (kind === ".") {
            pchar = visited.length;
          }
          cchar = blue;
        } else if (visited.length > 0) {
          if (kind === ".") {
            pchar = visited[0];
          }
          cchar = green;
        }

        return `${cchar}${pchar}${white}`;
      }
    ).join("")
  )
  .map(row => console.log(row));
}

function parseGrid(data) {
  return data.map(
    (row, y) =>
      row.split("")
        .map(
          (val, x) => ({
            x,
            y,
            visited: [],
            kind: val
          })
        )
  );
}

async function loadPuzzle() {
  const sampleData = `
  .|...\\....
  |.-.\\.....
  .....|-...
  ........|.
  ..........
  .........\\
  ..../.\\\\..
  .-.-/..|..
  .|....-|.\\
  ..//.|....
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

const black = "\x1b[30m";
const red = "\x1b[31m";
const green = "\x1b[32m";
const yellow = "\x1b[33m";
const blue = "\x1b[34m";
const magenta = "\x1b[35m";
const cyan = "\x1b[36m";
const white = "\x1b[37m";
const bold = "\033[1m";
const underline = "\033[4m";
const normal = "\033[0m";

await main({ data: await loadPuzzle() })
