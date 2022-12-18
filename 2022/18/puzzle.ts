#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePartOne(args.data)}`);
  console.log(`Part Two: ${solvePartTwo(args.data)}`);
}

function solvePartOne(data) {
  let sides = 0;

  data.forEach(cube => {
    sides += countExposedSides(data, cube);
  });

  return sides;
}

function solvePartTwo(data) {
  const bounds = getBounds(data);

  const queue = [{x: bounds.minX, y: bounds.minY, z: bounds.minZ}];
  const visited = new Set();

  const allCubes = new Set();
  data.forEach(cube => add(allCubes, cube));

  let sides = 0;

  while (queue.length) {
    const current = queue.shift();

    if (has(visited, current)) {
      continue;
    }

    add(visited, current);

    for (const diff of [-1, 1]) {
      const directions = [
        [0, 0, diff],
        [0, diff, 0],
        [diff, 0, 0],
      ];

      for (const direction of directions) {
        const newCube = {
          x: current.x + direction[0],
          y: current.y + direction[1],
          z: current.z + direction[2],
        }

        if (has(allCubes, newCube)) {
          sides++;
        } else if (!has(visited, newCube) && inBounds(bounds, newCube)) {
          queue.push(newCube);
        }
      }
    }

  }

  return sides;
}

function inBounds(bounds, cube) {
  return (
    (cube.x >= bounds.minX && cube.x <= bounds.maxX) &&
    (cube.y >= bounds.minY && cube.y <= bounds.maxY) &&
    (cube.z >= bounds.minZ && cube.z <= bounds.maxZ)
  );
}

function toS(value) {
  return `(${value.x},${value.y},${value.z})`;
}

function add(_set, value) {
  _set.add(toS(value));
}

function has(_set, value) {
  return _set.has(toS(value));
}

function getBounds(cubes) {
  let [minX, minY, minZ] = [
    Number.MAX_SAFE_INTEGER,
    Number.MAX_SAFE_INTEGER,
    Number.MAX_SAFE_INTEGER
  ];

  let [maxX, maxY, maxZ] = [
    -Number.MAX_SAFE_INTEGER,
    -Number.MAX_SAFE_INTEGER,
    -Number.MAX_SAFE_INTEGER
  ];

  for (const cube of cubes) {
    minX = Math.min(minX, cube.x);
    minY = Math.min(minY, cube.y);
    minZ = Math.min(minZ, cube.z);

    maxX = Math.max(maxX, cube.x);
    maxY = Math.max(maxY, cube.y);
    maxZ = Math.max(maxZ, cube.z);
  }

  return {
    minX: minX - 1,
    minY: minY - 1,
    minZ: minZ - 1,

    maxX: maxX + 1,
    maxY: maxY + 1,
    maxZ: maxZ + 1,
  };
}

function countExposedSides(cubes, cube) {
  let exposed = 6;
  for (const _cube of cubes) {
    if (_cube === cube) {
      continue;
    }

    if (
      (
        Math.abs(_cube.x - cube.x) == 1 && _cube.y === cube.y && _cube.z === cube.z
      ) || (
        _cube.x === cube.x && Math.abs(_cube.y - cube.y) === 1 && _cube.z === cube.z
      ) || (
        _cube.x === cube.x && _cube.y === cube.y && Math.abs(_cube.z - cube.z) === 1
      )
    ) {
      exposed--;
    }

  }

  return exposed;
}

async function loadPuzzle() {
  const sampleData = `
    2,2,2
    1,2,2
    3,2,2
    2,1,2
    2,3,2
    2,2,1
    2,2,3
    2,2,4
    2,2,6
    1,2,5
    3,2,5
    2,1,5
    2,3,5
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data.map(cube => {
    const [x, y, z] = cube.split(/,/).map(Number)
    return {
      x,
      y,
      z,
    }
  });

  return processed;
}

await main({ data: await loadPuzzle() })
