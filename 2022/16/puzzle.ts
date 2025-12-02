#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePartOne(data, time = 29, current = "AA", state = {}, seen = {}) {
  let m = Object.keys(state)
    .map(key => {
      state[key] =
    })
}
function solvePuzzle(data, partTwo = false) {
  if (partTwo) { return ; }

  const keys = Object.keys(data)
    .filter(key => data[key].flowRate > 0);

  for (let start of keys.concat(["AA"])) {
    for (let end of keys) {
      data[start].paths[end] = bfs(data, data[start].connections, end);
    }
  }

  best = 0;
  findPath(data, new Set("AA"), 0, "AA", 29);
  return best;
}

let best = 0;
function findPath(data, open, flowed, current, remaining) {
  if (flowed > best) {
    best = flowed;
  }

  if (remaining <= 0) {
    return;
  }

  if (!open.has(current)) {
    const next = new Set(open);
    open.add(current);

    findPath(data, next, flowed + (data[current].flowRate * remaining), current, remaining - 1);
  } else {
    const paths = Object.keys(data[current].paths)
      .filter(key => !open.has(key));
    for (let path of paths) {
      findPath(data, opened, path, remaining - data[current].paths[path])
    }
  }
}

function bfs(data, options, destination) {
  let depth = 1;
  while (true) {
    let next = new Set();

    for (let option of options) {
      if (option === destination) {
        return depth;
      }

      for (let possible of data[option].connections) {
        next.add(possible);
      }
    }

    options = next;
    depth++;
  }
}

async function loadPuzzle() {
  const sampleData = `
  Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
  Valve BB has flow rate=13; tunnels lead to valves CC, AA
  Valve CC has flow rate=2; tunnels lead to valves DD, BB
  Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
  Valve EE has flow rate=3; tunnels lead to valves FF, DD
  Valve FF has flow rate=0; tunnels lead to valves EE, GG
  Valve GG has flow rate=0; tunnels lead to valves FF, HH
  Valve HH has flow rate=22; tunnel leads to valve GG
  Valve II has flow rate=0; tunnels lead to valves AA, JJ
  Valve JJ has flow rate=21; tunnel leads to valve II
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = {};
  data.forEach(line => {
      const [_, valve, flowRate, conns] = line
        .match(/Valve ([A-Z]{2}) has flow rate=(\d+); tunnel(?:s)? lead(?:s)? to valve(?:s)? ((?:(?:[A-Z]{2}(?:, )?))+)/);

      processed[valve] = {
        valve,
        connections: conns.split(/,/).map(s => s.trim()),
        flowRate,
        paths: {},
      }
    });

  return processed;
}

await main({ data: await loadPuzzle() })
