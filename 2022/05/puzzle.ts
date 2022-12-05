#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const { moves } = data;
  const crates = {};
  Object.keys(data.crates).forEach(k => {
    crates[k] = Object.assign([], data.crates[k]);
  });

  moves.forEach(({ num, fromIdx, toIdx }) => {
    const items = crates[fromIdx].splice(0, num);
    if (!partTwo) {
      items.reverse();
    }
    crates[toIdx].unshift(...items);
  });

  const result = [];
  Object.keys(crates).sort().forEach(k => {
    if (crates[k].length > 0) {
      result.push(crates[k][0]);
    }
  });

  return result.join("");
}

async function loadPuzzle() {
  const sampleData = `    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

 move 1 from 2 to 1
 move 3 from 1 to 3
 move 2 from 2 to 1
 move 1 from 1 to 2
  `;

  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .split("\n")
    .slice(0, -1);

  let finishedCrates = false;

  const processed = {
    crates: {},
    moves: [],
  };

  data.forEach((line) => {
    if (line === "") {
      finishedCrates = true;
      return;
    }

    if (finishedCrates) {
      const parts = line.split(" ");
      if (USE_SAMPLE_DATA) {
        parts.shift();
      }

      const [move, num, _from, fromIdx, _to, toIdx] = parts;

      processed.moves.push({
        num: parseInt(num),
        // offset by 1 because arrays are 0 indexed
        fromIdx: parseInt(fromIdx) - 1,
        toIdx: parseInt(toIdx) - 1,
      });

      return;
    }

    for (let i = 0; i < line.length; i++) {
      if (line[i] === "[") {
        let char = line[i + 1];
        let row = i / 4;
        if (!processed.crates.hasOwnProperty(row)) {
          processed.crates[row] = [];
        }

        processed.crates[row].push(char);

        i += 3;
      }
    }

  });

  return processed;
}

await main({ data: await loadPuzzle() })
