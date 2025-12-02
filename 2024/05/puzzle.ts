#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function isCorrect(pages, rules) {
  for (let i = 0; i < pages.length; i++) {
    let page = pages[i];
    if (rules[page]) {
      let indexes = rules[page].map(p => pages.indexOf(p)).filter(n => n !== -1);
      if (!indexes.every(n => n > i)) {
        return false;
      }
    }
  }

  return true;
}

function fixPages(pages, rules) {
  let fixedOrder = [];
  fixedOrder.push(pages[0])

  for (let i = 1; i < pages.length; i++) {
    let page = pages[i];
    let indexes = (rules[page] ?? []).map(p => fixedOrder.indexOf(p)).filter(n => n !== -1);
    if (indexes && !indexes.length) {
      fixedOrder.push(page);
    } else {
      let before = indexes.sort()[0];
      fixedOrder.splice(before, 0, page);
    }
  }

  if (!isCorrect(fixedOrder, rules)) {
    // this is terrible and I hate it.
    return fixPages(fixedOrder, rules)
  }

  return fixedOrder;
}

function solvePuzzle({ rules, pages }, partTwo = false) {
  const correctMiddleValues = [];
  for (let page of pages) {
    let correct = isCorrect(page, rules)
    if (correct && !partTwo) {
      correctMiddleValues.push(page[Math.floor(page.length / 2)]);
    } else if (!correct && partTwo) {
      let fixed = fixPages(page, rules);
      correctMiddleValues.push(fixed[Math.floor(fixed.length / 2)]);
    }
  }

  return correctMiddleValues.reduce(
    (acc, x) => {
      return acc + x;
    },
    0
  );
}

async function loadPuzzle() {
  const sampleData = `
  47|53
  97|13
  97|61
  97|47
  75|29
  61|13
  75|53
  29|13
  97|29
  53|29
  61|53
  97|53
  61|29
  47|13
  75|47
  97|75
  47|61
  75|61
  47|29
  75|13
  53|13

  75,47,61,53,29
  97,61,53,29,13
  75,29,13
  75,97,47,61,53
  61,13,29
  97,13,75,29,47
  `;
  const data = (
    USE_SAMPLE_DATA ?
    sampleData :
    fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
  )
    .trim()
    .split("\n")
    .map(s => s.trim());


  let firstSection = true;
  let rules = [];
  let pages = [];
  for (let line of data) {
    if (firstSection && line === "") {
      firstSection = false;
      continue;
    } else if (firstSection) {
      let [first, second] = line.split("|").map(n => parseInt(n));
      rules.push({ first, second });
    } else {
      pages.push(line.split(",").map(n => parseInt(n)));
    }
  }

  return {
    rules: processRules(rules),
    pages,
  };
}

function processRules(originals) {
  const processed = {};

  for (let { first, second } of originals) {
    if (!processed[first]) {
      processed[first] = [];
    }
    processed[first].push(second);
  }

  return processed;
}

await main({ data: await loadPuzzle() })
