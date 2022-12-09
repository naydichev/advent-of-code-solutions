#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const visited = [];
  let numKnots = 2;
  if (partTwo) {
    numKnots = 10;
  }

  const knots = Array.from({ length: numKnots })
    .map(_ => ({ x: 0, y: 0 }));

  const head = knots[0];
  const tail = knots[knots.length - 1];


  data.forEach(move => {
    let n = move.distance;

    while (n > 0) {
      // move head
      Object.assign(
        head,
        nextCoordinate(head, move.direction)
      );

      knots.slice(1)
        .forEach((knot, i) => {
          Object.assign(
            knot,
            follow(knots[i], knot)
          );
        });

      visited.push(`(${tail.x}, ${tail.y})`);

      n--;
    }

  });

  return new Set(visited).size;
}

function follow(head, tail) {
  const updated = {
    x: tail.x,
    y: tail.y,
  };

  const yDiff = head.y - tail.y;
  const xDiff = head.x - tail.x;
  const ySign = Math.sign(yDiff);
  const xSign = Math.sign(xDiff);

  if (xDiff === 0 && Math.abs(yDiff) === 2) {
    // take a step in y
    updated.y += ySign;
  } else if (yDiff === 0 && Math.abs(xDiff) === 2) {
    // take a step in x
    updated.x += xSign;
  } else if ((Math.abs(yDiff) + Math.abs(xDiff)) > 2) {
    updated.y += ySign;
    updated.x += xSign;
  }

  return updated;
}

function nextCoordinate(coord, direction) {
  const updatedCoord = {
    x: coord.x,
    y: coord.y,
  };

  if (direction === "U") {
    updatedCoord.y++;
  } else if (direction === "D") {
    updatedCoord.y--;
  } else if (direction === "R") {
    updatedCoord.x++;
  } else {
    updatedCoord.x--;
  }

  return updatedCoord;
}

async function loadPuzzle() {
  const sampleData = `
  R 4
  U 4
  L 3
  D 1
  R 4
  D 1
  L 5
  R 2
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data.
    map(d => {
      const [direction, distance] = d.split(" ");
      return {
        direction,
        distance: parseInt(distance),
      };
    });

  return processed;
}

await main({ data: await loadPuzzle() })
