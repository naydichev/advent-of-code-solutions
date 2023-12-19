#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const [workflows, parts] = parseData(data);

  if (partTwo) {
    const possibles = computeAllPossible(workflows);
    return countPossibles(possibles);
  }
  const accepted = parts.filter(part => runWorkflows(part, workflows));

  return sum(
    accepted.map(
      part => sum(Object.values(part))
    )
  );
}

const copy = x => JSON.parse(JSON.stringify(x));

function countPossibles(possibles) {
  const options = possibles.map(({ values }) => values);

  return sum(
    options.map(
      xmas => Object.values(xmas)
      .reduce(
        (acc, { min, max }) => acc * (max - min + 1),
        1
      )
    )
  );
}


function computeAllPossible(workflows) {
  const paths = [{
    values: {
      x: { min: 1, max: 4000 },
      m: { min: 1, max: 4000 },
      a: { min: 1, max: 4000 },
      s: { min: 1, max: 4000 },
    },
    path: ["in"],
  }];

  const approved = [];

  while (paths.length) {
    const path = paths.shift();
    const { rules } = workflows[path.path.at(-1)];
    const mypath = copy(path);
    rules.forEach(rule => {

      const localpath = copy(mypath);
      if (rule.key) {
        if (rule.mode === "<") {
          localpath.values[rule.key].max = Math.min(mypath.values[rule.key].max, rule.desired - 1);
          mypath.values[rule.key].min = Math.max(mypath.values[rule.key].min, rule.desired);
        } else {
          localpath.values[rule.key].min = Math.max(mypath.values[rule.key].min, rule.desired + 1);
          mypath.values[rule.key].max = Math.min(mypath.values[rule.key].max, rule.desired);
        }
      }

      if (rule.rejected) {
        return;
      }

      if (rule.approved) {
        approved.push(localpath);
        return;
      }

      localpath.path.push(rule.redirected);
      paths.push(localpath);
    });
  }

  return approved;
}

function runWorkflows(part, workflows) {
  let curr = "in";
  let path = [curr];
  while (true) {
    let [approved, rejected, redirected] = runWorkflow(part, workflows[curr]);
    if (approved) {
      return true;
    } else if (rejected) {
      return false;
    }

    curr = redirected;
    path.push(curr);
  }
}

function runWorkflow(part, { rules }) {
  for (let i = 0; i < rules.length; i++) {
    const rule = rules[i];
    if (rule.check(part)) {
      return [rule.approved, rule.rejected, rule.redirected];
    }
  }
}

const sum = (list) => list.reduce((a, b) => a + b, 0);

function parseData(data) {
  const workflows = {};
  const parts = [];

  let partsMode = false;
  data.forEach(line => {
    if (line === "") {
      partsMode = true;
      return;
    }

    if (!partsMode) {
      const [_, name, criteria] = line.match(/(\w+)\{([^}]+)\}/);
      const rules = parseCriteria(criteria);
      workflows[name] = {
        name,
        rules,
      };
    } else {
      let pieces = line.substring(1, line.length - 1).split(",")
        .map(piece => piece.split("="));

      parts.push(
        Object.fromEntries(
          pieces.map(
            ([k, v]) => ([k, parseInt(v)])
          )
        )
      );
    }
  });

  return [workflows, parts]
}

function parseCriteria(criteria) {
  const rawRules = criteria.split(",");

  return rawRules.map(
    rule => {
      let check = null;
      let result = null;
      let key = null;
      let desired = null;
      let mode = null;
      if (!rule.includes(":")) {
        check = () => true;
        result = rule;
        key = null;
        desired = null;
        mode = null;
      } else {
        const [condition, _result] = rule.split(":");
        result = _result;
        key = condition.substring(0, 1);
        desired = parseInt(condition.substring(2));
        mode = condition.substring(1, 2);
        if (mode === "<") {
          check = ({ [key]: value }) => value < desired;
        } else {
          check = ({ [key]: value }) => value > desired;
        }
      }

      let approved = result === "A";
      let rejected = result === "R";
      let redirected = (approved || rejected) ? null : result;

      return {
        check,
        approved,
        rejected,
        redirected,
        desired,
        mode,
        key,
      };
    }
  );
}

async function loadPuzzle() {
  const sampleData = `
  px{a<2006:qkq,m>2090:A,rfg}
  pv{a>1716:R,A}
  lnx{m>1548:A,A}
  rfg{s<537:gd,x>2440:R,A}
  qs{s>3448:A,lnx}
  qkq{x<1416:A,crn}
  crn{x>2662:A,R}
  in{s<1351:px,qqz}
  qqz{s>2770:qs,m<1801:hdj,R}
  gd{a>3333:R,R}
  hdj{m>838:A,pv}

  {x=787,m=2655,a=1222,s=2876}
  {x=1679,m=44,a=2067,s=496}
  {x=2036,m=264,a=79,s=2244}
  {x=2461,m=1339,a=466,s=291}
  {x=2127,m=1623,a=2188,s=1013}
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
