#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  // console.log(`Part One: ${solvePartOne(args.data)}`);
  console.log(`Part Two: ${solvePartTwo(args.data)}`);
}

function solvePartOne(data) {
  const targetY = USE_SAMPLE_DATA ?
    10 :
    2000000;

  const grid = {};

  data
    .map(({ sensor, beacon }) => [sensor, beacon])
    .reduce((acc, x) => acc.concat(x), [])
    .filter(({x, y}) => y === targetY)
    .map(({ x }) => x)
    .forEach(x => grid[x] = "X");

  data.forEach(({ sensor, distance }) => {
    const distanceToY = dist(
      sensor,
      {
        x: sensor.x,
        y: targetY
      }
    );

    const diff = distance - distanceToY;
    if (diff < 0) {
      return;
    }


    for (let x = sensor.x - diff; x <= sensor.x + diff; x++) {
      if (!!grid[x]) {
        continue;
      }

      if (dist(sensor, { x, y: targetY }) <= distance) {
        grid[x] = "#";
      }
    }
  });

  return Object.values(grid)
    .filter(p => p === "#")
    .length;
}

function solvePartTwo(data) {
  const maxBound = USE_SAMPLE_DATA ?
    20 :
    4000000;

  const grid = defaultdict(() => defaultdict(() => "."));

  const inBounds = (v) => v >= 0 && v <= maxBound;

  data.forEach(({ sensor, beacon, distance }, i) => {
    grid[sensor.y][sensor.x] = "S";
    grid[beacon.y][beacon.x] = "B";

    const { x: sx, y: sy } = sensor;

    for (
      let y = Math.max(0, sy - distance);
      inBounds(y) && y <= sy + distance;
      y++
    ) {
      const yDiff = Math.abs(y - sy);
      const yDistDiff = Math.abs(yDiff - distance);
      for (
        let x = Math.max(0, sx - yDistDiff);
        inBounds(x) && x <= sx + yDistDiff;
        x++
      ) {
          if (grid[y][x] !== ".") {
            grid[y][x] = "#";
          }
      }
    }
  });

  return Object.keys(grid)
    .map(y => ({ y, row: grid[y] }))
    .filter(({ row }) => row.includes("."))
    .map(({ y, row }) => (row.indexOf(".") * 4000000) + y);
}

function dist(a, b) {
  return Math.abs(a.y - b.y) + Math.abs(a.x - b.x);
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



async function loadPuzzle() {
  const sampleData = `
  Sensor at x=2, y=18: closest beacon is at x=-2, y=15
  Sensor at x=9, y=16: closest beacon is at x=10, y=16
  Sensor at x=13, y=2: closest beacon is at x=15, y=3
  Sensor at x=12, y=14: closest beacon is at x=10, y=16
  Sensor at x=10, y=20: closest beacon is at x=10, y=16
  Sensor at x=14, y=17: closest beacon is at x=10, y=16
  Sensor at x=8, y=7: closest beacon is at x=2, y=10
  Sensor at x=2, y=0: closest beacon is at x=2, y=10
  Sensor at x=0, y=11: closest beacon is at x=2, y=10
  Sensor at x=20, y=14: closest beacon is at x=25, y=17
  Sensor at x=17, y=20: closest beacon is at x=21, y=22
  Sensor at x=16, y=7: closest beacon is at x=15, y=3
  Sensor at x=14, y=3: closest beacon is at x=15, y=3
  Sensor at x=20, y=1: closest beacon is at x=15, y=3
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
    .map(line => {
      const [_, sx, sy, bx, by] = line
        .match(
          /Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)/
        );

      const sensor = {
        x: Number(sx),
        y: Number(sy),
      };

      const beacon = {
        x: Number(bx),
        y: Number(by),
      };

      return {
        sensor,
        beacon,
        distance: dist(sensor, beacon),
      };
    });

    return processed;
}

await main({ data: await loadPuzzle() })
