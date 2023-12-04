#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

function solvePuzzle(data, partTwo = false) {
  const cards = processCards(data);

  findWins(cards);

  if (!partTwo) {
    return cards.map(({ numWon }) => Math.floor(Math.pow(2, numWon - 1)))
      .reduce((a, b) => a + b, 0);
  }

  cards.forEach(({ numWon, copies }, n) => {
    while (numWon > 0) {
      cards[n + numWon].copies = copies + cards[n + numWon].copies;
      numWon--;
    }
  });

  return cards.map(({ copies }) => copies).reduce((a, b) => a + b, 0);
}

function findWins(cards) {
  cards.forEach(card => {
    card.numWon = card.ownedNumbers
    .filter(
      n => card.winningNumbers.includes(n)
    )
    .length;
  });
}

const cardRegex = new RegExp(/Card\W+(\d+):\W+([^\|]+)\|\W+(.+)/);

function processCards(data) {
  const cards = [];
  data.forEach(line => {
    const [_, cardNum, winning, owned] = cardRegex.exec(line);
    const card = {
      cardNum: Number(cardNum),
      winningNumbers: toNumbers(winning),
      ownedNumbers: toNumbers(owned),
      copies: 1,
    };

    cards.push(card);

  });

  return cards;
}

function toNumbers(line) {
  return line.trim()
    .split(" ")
    .filter(n => n)
    .map(Number);
}

async function loadPuzzle() {
  const sampleData = `
  Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
  Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
  Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
  Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
  Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
  Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
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
