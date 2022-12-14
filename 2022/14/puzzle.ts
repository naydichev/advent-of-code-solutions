#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  let _grid = generateGrid(data);
  let grid = _grid;
  const { x, y } = getBounds(grid);
  let [minY, maxY] = y;

  if (partTwo) {
    const myMaxY = maxY + 2;
    grid = new Proxy(_grid, {
      get: (target, name) => {
        if (parseInt(name) === (myMaxY)) {
          target[name] = defaultdict(() => "#")
        }

        return target[name];
      }
    });

    maxY = myMaxY;
  }

  grid[0][500] = "+";

  let iterations = 0;

  while (true) {
    let [sx, sy] = [500, 0];
    let inMotion = true;

    while (inMotion && sy <= maxY) {
      const [osx, osy] = [sx, sy];

      // first try to move down one
      if (grid[sy + 1][sx] === ".") {
        sy++;
      // then try down and to the left
      } else if (grid[sy + 1][sx - 1] === ".") {
        sy++;
        sx--;
      // then try down and to the right
      } else if (grid[sy + 1][sx + 1] === ".") {
        sy++;
        sx++;
      }


      if (osx !== sx || osy !== sy) {
        if (grid[osy][osx] !== "+") {
          grid[osy][osx] = ".";
        }

        grid[sy][sx] = "o";
      } else {
        inMotion = false;
      }

    }


    if (inMotion) {
      grid[sy][sx] = ".";
      break;
    } else {
      if (partTwo && (sx === 500 && sy === 0)) {
        grid[500][0] = "o";
        break;
      }
      inMotion = true;
    }

    iterations++;
  }

  return countSand(grid);
}


function getBounds(grid) {
  const yVals = Object.keys(grid);
  const minY = Math.min(...yVals, 0);
  const maxY = Math.max(...yVals);

  const xVals = yVals.map(y => grid[y])
    .map(g => Object.keys(g))
    .reduce((acc, x) => acc.concat(x), []);

  const minX = Math.min(...xVals);
  const maxX = Math.max(...xVals);

  return {
    y: [minY, maxY],
    x: [minX, maxX],
  };
}

function countSand(grid) {
  const {
    y: [minY, maxY],
    x: [minX, maxX],
  } = getBounds(grid);

  let sand = 0;
  for (let y = minY; y <= maxY; y++) {
    for (let x = minX; x <= maxX; x++) {
      if (grid[y][x] === "o") {
        sand++;
      }
    }
  }

  return sand;
}

function printGrid(grid, partTwo) {
  let {
    y: [minY, maxY],
    x: [minX, maxX],
  } = getBounds(grid);

  if (partTwo) {
    minX += 100;
    maxX -= 100;
  }


  for (let y = minY; y <= maxY; y++) {
    const row = [];
    for (let x = minX; x <= maxX; x++) {
      if (grid[y] && grid[y][x]) {
        row.push(grid[y][x]);
      } else {
        row.push(".");
      }
    }

    console.log(row.join(""));
  }

}

function defaultdict(defaultValue) {
  return new Proxy({}, {
    get: (target, name) => {
      if (!(name in target)) {
        target[name] = defaultValue();
      }

      return target[name];
    }
  });
}

function generateGrid(data) {
  const grid = defaultdict(
    () => defaultdict(
      () => "."
    )
  );

  data.forEach(points => {
    const _points = [...points];

    let previous = _points.shift();

    grid[previous[1]][previous[0]] = "#";

    _points.forEach(point => {
      const [nx, ny] = point;
      const [px, py] = previous;

      let minX = Math.min(nx, px);
      let maxX = Math.max(nx, px);

      let minY = Math.min(ny, py);
      let maxY = Math.max(ny, py);

      for (let y = minY; y <= maxY; y++) {
        for (let x = minX; x <= maxX; x++) {
          grid[y][x] = "#";
        }
      }

      previous = point;
    });
  });

  return grid;
}


async function loadPuzzle() {
  const sampleData = `
  498,4 -> 498,6 -> 496,6
  503,4 -> 502,4 -> 502,9 -> 494,9
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data
  .map(l =>
   l.split("->")
    .map(c => c.trim())
    .map(c => c.split(",").map(Number))
  );

  return processed;
}

await main({ data: await loadPuzzle() })
