#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

class OpCode {
  constructor(
    private readonly code: string,
    private readonly func: Function,
    private readonly cycleDuration,
  ) {}

  public invoke(...args: any[]): any {
    return this.func(...args);
  }

  public get duration(): number {
    return this.cycleDuration;
  }
}

const OPCODES = {
  addx: new OpCode(
    "addx",
    (registers, value, ...junk) => {
      registers.x += parseInt(value)
    },
    2,
  ),
  noop: new OpCode(
    "noop",
    (...args) => {},
    1,
  ),
};



async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  solvePuzzle(args.data, true);
}

function solvePuzzle(data, partTwo = false) {
  const probeCycles = [20, 60, 100, 140, 180, 220];
  const probeValues = [];
  const registers = { x: 1 };
  let cycle = 0;

  const display = [];
  let row = [];

  data.forEach(instr => {
    let n = instr.opcode.duration;

    while (n > 0) {
      cycle++;
      n--;

      if (probeCycles.includes(cycle)) {
        probeValues.push(cycle * registers.x);
      }

      let { x } = registers;
      let width = [ x - 1, x, x + 1];
      if (width.includes(row.length)) {
        row.push("#");
      } else {
        row.push(".");
      }

      if (cycle % 40 === 0) {
        display.push(row);
        row = [];
      }
    }

    instr.opcode.invoke(registers, instr.args);
  });

  if (partTwo) {
    display.forEach(r => {
      console.log(r.join(""));
    });
  }

  return probeValues.reduce((acc, x) => acc + x, 0);
}

async function loadPuzzle() {
  const data = (
    USE_SAMPLE_DATA ?
    SAMPLE_DATA :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());

  const processed = data
    .map(instr => {
      const [code, ...args] = instr.split(" ");

      return {
        opcode: OPCODES[code],
        args: args.map(Number),
      };
    });

  return processed;
}

const SAMPLE_DATA = `
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop`;

await main({ data: await loadPuzzle() })
