#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

enum D {
  N = "N",
  E = "E",
  W = "W",
  S = "S",
}


function solvePuzzle(data, partTwo = false) {
  const grid = data.map(
    (line, y) =>
      line
        .split("")
        .map(
          (shape, x) => ({
            shape,
            possibleConnections: getPossibleConnections(shape),
            path: false,
            x,
            y,
          })
        )
  );

  const [_, [x, y]] = grid.map(
    (line) => line.map(
      ({ shape, x, y }) => ([shape, [x, y]])
    )
  )
  .reduce((acc, row) => acc.concat(row), [])
  .find(([ shape ]) => shape === "S");

  const start = grid[y][x];

  [
    [[0, -1], D.S, D.N],
    [[0,  1], D.N, D.S],
    [[-1, 0], D.E, D.W],
    [[ 1, 0], D.W, D.E],
  ].forEach(([[dx, dy], needle, orelse]) => {
    const el = grid[y + dy][x + dx];
    const idx = start.possibleConnections.indexOf(orelse);
    if (el && !el.possibleConnections.includes(needle)) {
      if (idx > -1) {
        start.possibleConnections.splice(
          idx, 1
        );
      }
    }
  });


  calculateDistanceFrom(grid, x, y);

  if (partTwo) {
    markInsideCells(grid);
    return grid.map(
      row => row.filter(cell => cell.inside)
    )
    .reduce((acc, v) => acc.concat(v), [])
    .length;
  } else {
    return grid.map(
      line => line.map(el => el.dist)
      .filter(dist => dist >= 0)
    ).reduce((acc, v) => acc.concat(v), [])
    .reduce((a, b) => Math.max(a, b), 0);
  }
}


function markInsideCells(grid) {
  let inside = false;
  for (let y = 0; y < grid.length; y++) {
    let prevBendOut;
    for (let x = 0; x < grid[y].length; x++) {
      const el = grid[y][x];
      const northSouthConnections = el
        .possibleConnections
        .filter(v => [D.N, D.S].includes(v));
      const westEastConnections = el
        .possibleConnections
        .filter(v => [D.W, D.E].includes(v));

      const isWallPiece = northSouthConnections.length > 1;
      const isBend = northSouthConnections.length > 0
        && westEastConnections.length > 0;

      const isOnPath = el.path;

      el.inside = isOnPath ? false : inside;
      // el.inside = inside;

      if (isOnPath) {
        if (isBend) {
          if (prevBendOut) {
            if (
              prevBendOut[0] !== westEastConnections[0]
                && prevBendOut[1] !== northSouthConnections[0]
            ) {
              inside = !inside;
            }

            prevBendOut = undefined;
          } else {
            prevBendOut = [
              westEastConnections[0],
              northSouthConnections[0],
            ];
          }
        } else if (isWallPiece) {
          inside = !inside;
        }
      }

    }
  }

  printGrid(grid);
  return grid;
}

function printGrid(grid) {
  console.log(
    grid.map(
      line => line.map(
        ({ shape, dist, possibleConnections, inside }) => {
          const topRow = [];
          const bottomRow = [];

          if (possibleConnections.includes(D.N)) {
            topRow.push(`/${magenta} ^^ ${white}\\`);
          } else {
            topRow.push(`${white}/ -- \\`);
          }

          if (possibleConnections.includes(D.S)) {
            bottomRow.push(`\\ ${magenta}vv ${white}/`);
          } else {
            bottomRow.push(`${white}\\ -- /`);
          }

          let printingChar = shape;
          let printingColor = inside ? bold + underline : normal;
          const result = [];
          if (possibleConnections.includes(D.W)) {
            result.push(`${magenta}<${white}`);
          } else {
            result.push(`${white}|`);
          }

          result.push(`${printingColor}${spaced(dist ? dist : printingChar, 4)}${white}${normal}`);

          if (possibleConnections.includes(D.E)) {
            result.push(`${magenta}>${white}`);
          } else {
            result.push(`${white}|`);
          }

          return [
            topRow,
            result.join(""),
            bottomRow,
          ];
        }
      ).reduce(
      (acc, x) => ([
        acc[0] + x[0],
        acc[1] + x[1],
        acc[2] + x[2],
      ]),
      ["", "", ""]
      ).reduce((acc, x) => acc.concat(x), [])
    ).reduce((acc, x) => acc.concat(x), [])
    .join("\n")
  );
}

function spaced(l, size = 3) {
  let i = 0;
  while(`${l}`.length < size) {
    if (i % 2 === 0) {
      l = " " + l;
    } else {
      l += " ";
    }
    i++;
  }

  return l;
}


function getPossibleConnections(shape) {
  switch (shape) {
    case "-": return [D.E, D.W];
    case "|": return [D.N, D.S];
    case "F": return [D.S, D.E];
    case "7": return [D.S, D.W];
    case "L": return [D.N, D.E];
    case "J": return [D.N, D.W];
    case "S": return [D.N, D.E, D.W, D.S];
    case ".": return [];
  }
}

function calculateDistanceFrom(grid, x, y, current = 0) {
  const el = grid[y][x];
  if (!isNaN(el.dist) && current >= el.dist) {
    return;
  }

  grid[y][x].dist = current;
  grid[y][x].path = true;

  findAdjacents(grid, x, y, grid[y][x])
  .forEach(
    ([d, [nx, ny]]) => {
      const newEl = grid[ny][nx];

      if (
        newEl.shape === "."
      || !newEl.possibleConnections.includes(opposite(d))
      ) {
        return;
      }

      return calculateDistanceFrom(grid, nx, ny, current + 1);
    }
  );
}

function opposite(d) {
  if (d === D.N) {
    return D.S;
  } else if (d === D.E) {
    return D.W;
  } else if (d === D.W) {
    return D.E;
  } else if (d === D.S) {
    return D.N;
  }

  throw new Error(d);
}


function findAdjacents(grid, x, y, el) {
  return [
    [D.N, [0, -1]],
    [D.E, [1, 0]],
    [D.W, [-1, 0]],
    [D.S, [0, 1]],
  ]
  .filter(([d]) => el.possibleConnections.includes(d))
  .map(([d, [dx, dy]]) => ([d, [x + dx, y + dy]]))
    .filter(
      ([d, [nx, ny]]) => ny >= 0
      && ny < grid.length
      && nx >= 0
      && nx < grid[ny].length
      && grid[ny][nx].possibleConnections.includes(opposite(d))
    );
}

async function loadPuzzle() {
  const sampleData = samples[1];
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

const samples = [
  `
  ...........
  .S-------7.
  .|F-----7|.
  .||.....||.
  .||.....||.
  .|L-7.F-J|.
  .|..|.|..|.
  .L--J.L--J.
  ...........
  `,
  `
  .F----7F7F7F7F-7....
  .|F--7||||||||FJ....
  .||.FJ||||||||L7....
  FJL7L7LJLJ||LJ.L-7..
  L--J.L7...LJS7F-7L7.
  ....F-J..F7FJ|L7L7L7
  ....L7.F7||L7|.L7L7|
  .....|FJLJ|FJ|F7|.LJ
  ....FJL-7.||.||||...
  ....L---J.LJ.LJLJ...
  `,
];


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
