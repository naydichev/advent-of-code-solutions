#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  // only 12 red cubes, 13 green cubes, and 14 blue cubes
  let maxCubes = {
    red: 12,
    green: 13,
    blue: 14,
  };

  const processed = processData(
    data,
    partTwo ? null : maxCubes
  );

  if (!partTwo) {
    return processed.reduce(
      (acc, gameDetails) => acc + gameDetails.id,
      0
    );
  }

  const mins = processed.map(
    ({ rounds }) => {
      const _mins = { red: 0, green: 0, blue: 0 };
      rounds.forEach(pulls => {
        pulls.forEach(({ num, color }) => {
          _mins[color] = Math.max(num, _mins[color]);
        });
      });

      return _mins;
    }
  );

  return mins.reduce(
    (acc, _mins) => {
      const computed = Object.values(_mins)
        .reduce(
          (minacc, n) => minacc * n,
          1
        );

      return acc + computed;
    },
    0
  );
}

function processData(
  data: Array<string>,
  maxCubes?: { red: number, green: number, blue: number }
): Array<{ id: number, rounds: Array<{ num: number, color: string }> }> {
  return data.map(
    line => {
      try {
        const [gameWithNum, rest] = line.split(": ");
        const [_, gameId] = gameWithNum.split(" ");
        const pulls = rest.split("; ");

        const rounds = pulls.map(
          pull => {
            const colors = pull.split(", ");
            return colors.map(c => {
              const [num, color] = c.split(" ");
              if (maxCubes && num > maxCubes[color]) {
                throw Error("too many " + color);
              }

              return {
                num,
                color
              };
            });
          }
        );

        return {
          id: parseInt(gameId),
          rounds,
        };
      } catch (error) {
        return null;
      }
    }
  )
  .filter(game => game);
}

async function loadPuzzle() {
  const sampleData = `
  Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
  Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
  Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
  Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
  Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
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
