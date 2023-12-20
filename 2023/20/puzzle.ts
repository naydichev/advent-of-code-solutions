#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const modules = parseInput(data);

  return pushButton(modules, partTwo);
}

function pushButton(modules, partTwo) {
  let c = 0;
  let high = 0;
  let low = 0;
  let num = 1000;
  while (partTwo ? true : c < num) {
    c++;
    const pulses = [{ dest: "broadcaster", signal: "low", source: "button" }];
    const [_high, _low, rx] = processPulses(modules, pulses, partTwo);
    if (partTwo && rx) {
      return [null, null, rx];
    }
    high += _high;
    low += _low;
  }

  if (partTwo) {
    return c;
  } else {
    return high * low;
  }
}

function processPulses(modules, pulses, partTwo) {
  let high = 0;
  let low = 0;

  while (pulses.length) {
    const { dest, signal, source } = pulses.shift();
    if (signal === "low") {
      low++;
    } else {
      high++;
    }

    if (partTwo && dest === "rx" && signal == "low") {
      return [null, null, true];
    }

    if (!(dest in modules)) {
      continue;
    }

    const d = modules[dest];
    let outSignal = null;
    if (d.kind === "flip-flop") {
      if (signal === "low") {
        outSignal = "high";
        let dstate = "on";
        if (d.state === "on") {
          dstate = "off";
          outSignal = "low";
        }

        d.state = dstate;
      }
    } else if (d.kind === "conjunction") {
      d.state[source] = signal;
      if (Object.values(d.state).every(s => s === "high")) {
        outSignal = "low";
      } else {
        outSignal = "high";
      }
    } else if (d.kind === "broadcaster") {
      outSignal = signal;
    }

    if (outSignal) {
      d.outputs.forEach(o => {
        pulses.push({
          source: d.name,
          dest: o,
          signal: outSignal,
        });
      });
    }

  }

  return [high, low, false];
}

function parseInput(data) {
  const modules = {};

  data.forEach(line => {
    let [name, dest] = line.split(" -> ");
    let kind = "broadcaster";
    let state = null;
    if (name.startsWith("%")) {
      kind = "flip-flop";
      name = name.substring(1);
      state = "off";
    } else if (name.startsWith("&")) {
      kind = "conjunction";
      name = name.substring(1);
      state = {};
    }

    const outputs = dest.split(", ");

    modules[name] = {
      name,
      kind,
      state,
      outputs,
    };
  });

  Object.values(modules)
    .forEach(m => {
      m.outputs.forEach(o => {
        if ((o in modules) && modules[o].kind === "conjunction") {
          modules[o].state[m.name] = "low";
        }
      });
    });

  return modules;
}

async function loadPuzzle() {
  const sampleData = `
  broadcaster -> a
  %a -> inv, con
  &inv -> b
  %b -> con
  &con -> output
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
