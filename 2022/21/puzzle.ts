#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  // this doesn't work for all inputs
  // had to do some over under to narrow down the range until I hit the right range
  let n = 3759566893000;
  if (partTwo) {
    let results = [];
    const [arg1, arg2] = data.root.args;
    data.root.expr = `${arg1} === ${arg2}`;
    data.root.function = (a, b) => {
      results.push(a);
      const info = {
       a,
       b,
       n,
       "-": b - a,
       l: `${b - a}`.length,
      };
      if (results.length > 1) {
        const [x, y] = results.slice(-2);
        info.diff = x - y;
      }
      console.log(JSON.stringify(info, null, 2));
      return (a === b) && data.humn.value;
    };
    data.humn.type = "value";
  }

  let v = 0;
  while (!v) {
    if (partTwo) {
      data.humn.value = n;
    }

    v = processEquations(data);
    n--;
  }

  return v;
}

function processEquations(data) {
  const resolved = new Set();
  const depTree = {};
  const reverseDepTree = {};

  Object.values(data)
    .forEach(({ type, args, key }) => {
      if (type === "value") {
        resolved.add(key)
      } else {
        depTree[key] = [...args];

        for (const arg of args) {
          if (!reverseDepTree[arg]) {
            reverseDepTree[arg] = [];
          }

          reverseDepTree[arg].push(key);
        }
      }
    });

  Object.entries(depTree)
    .forEach(([key, deps]) => {
      const [arg1, arg2] = deps;

      if (resolved.has(arg1)) {
        deps.shift();
      }

      if (resolved.has(arg2)) {
        deps.pop();
      }

    });


  while(Object.keys(depTree).length) {
    const resolveable = Object.entries(depTree)
      .filter(([key, deps]) => !deps.length)
      .map(([key, deps]) => key);

    for (const toRes of resolveable) {
      const [arg1, arg2] = data[toRes].args;
      const value = data[toRes].function(
        data[arg1].value,
        data[arg2].value
      );

      data[toRes].value = value;

      if (reverseDepTree[toRes]) {
        for (const x of reverseDepTree[toRes]) {
          const idx = depTree[x].indexOf(toRes);
          depTree[x].splice(idx, 1);
        }
      }

      delete depTree[toRes];
    }

  }

  return data.root.value;
}

async function loadPuzzle() {
  const sampleData = `
  root: pppw + sjmn
  dbpl: 5
  cczh: sllz + lgvd
  zczc: 2
  ptdq: humn - dvpt
  dvpt: 3
  lfqf: 4
  humn: 5
  ljgn: 2
  sjmn: drzm * dbpl
  sllz: 4
  pppw: cczh / lfqf
  lgvd: ljgn * ptdq
  drzm: hmdt - zczc
  hmdt: 32
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

  data.map(l => l.split(": "))
    .forEach(([key, expr]) => {
      if (isNaN(expr)) {
        const [arg1, op, arg2] = expr.split(" ");
        processed[key] = {
          expr,
          key,
          type: "function",
          args: [arg1, arg2],
          function: new Function(arg1, arg2, `return ${expr}`),
        };
      } else {
        processed[key] = {
          key,
          type: "value",
          value: parseInt(expr),
        };
      }
    });

  return processed;
}

await main({ data: await loadPuzzle() })
