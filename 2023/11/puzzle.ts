#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const universe = data.map(
    line => line.split("")
  );

  const galaxies = universe.map(
    (row, y) => row.map((char, x) => char === "#" ? x : undefined)
      .filter(x => !isNaN(x))
      .map(x => ([x, y]))
  ).reduce((acc, a) => acc.concat(a), []);

  const expandedGalaxies = expand(universe, galaxies, partTwo ? 1000000 : 2);

  const distances = calculateDistances(expandedGalaxies);

  return distances.reduce((a, b) => a + b, 0);
}

function calculateDistances(galaxies) {
  const distances = []
  for (let i = 0; i < galaxies.length; i++) {
    for (let j = i + 1; j < galaxies.length; j++) {
      distances.push(Math.abs(galaxies[i][0] - galaxies[j][0]) + Math.abs(galaxies[i][1] - galaxies[j][1]));
    }
  }

  return distances;

}

function expand(map, galaxies, distance = 2) {
  const newGalaxies = JSON.parse(JSON.stringify(galaxies));

  let blankRows = 0;
  for (let y = 0; y < map.length; y++) {
    if (map[y].every(c => c === ".")) {
      blankRows++;

      galaxies.forEach(([gx, gy], idx) => {
        if (y < gy) {
          newGalaxies[idx][1] += distance - 1;
        }
      });
    }
  }

  let blankColumns = 0;
  for (let x = 0; x < map[0].length; x++) {
    if (map.map(row => row[x]).every(c => c === ".")) {
      blankColumns++;

      galaxies.forEach(([gx, gy], idx) => {
        if (x < gx) {
          newGalaxies[idx][0] += distance - 1;
        }
      });
    }
  }

  return newGalaxies;
}

async function loadPuzzle() {
  const sampleData = `
  ...#......
  .......#..
  #.........
  ..........
  ......#...
  .#........
  .........#
  ..........
  .......#..
  #...#.....
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
