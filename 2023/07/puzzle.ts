#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  console.log(`Part One: ${solvePuzzle(args.data)}`);
  console.log(`Part Two: ${solvePuzzle(args.data, true)}`);
}

enum HandKind {
  FiveOfAKind = 7,
  FourOfAKind = 6,
  FullHouse = 5,
  ThreeOfAKind = 4,
  TwoPair = 3,
  OnePair = 2,
  HighCard = 1,
};

type Hand = {
  cards: string;
  bid: number;
  kind: HandKind;
  k: string;
};

function solvePuzzle(data, partTwo = false) {
  const hands = data.map(line => {
    const [cards, bid] = line.split(" ");
    const kind = calculateHandKind(cards, partTwo);
    return {
      cards,
      bid: parseInt(bid),
      kind,
      k: HandKind[kind]
    };
  });

  const sortedHands = hands.sort((a, b) => compareHands(a, b, partTwo ? RankOrderPartTwo : RankOrderPartOne));

  return sortedHands
    .map(({ bid }, i) => bid * (i + 1))
    .reduce((a, b) => a + b, 0);;

}

function compareHands(handA: Hand, handB: Hand, rankOrder: Array<string>): number {
  return (handA.kind - handB.kind) || compareCards(handA.cards, handB.cards, rankOrder);
}

const RankOrderPartOne = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"];
const RankOrderPartTwo = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"];

function compareCards(cardsA: string, cardsB: string, rankOrder: Array<string>): number {
  for (let i = 0; i < cardsA.length; i++) {
    if (cardsA[i] !== cardsB[i]) {
      for (const rank of rankOrder) {
        if (cardsA[i] === rank) {
          return 1;
        } else if (cardsB[i] === rank) {
          return -1;
        }
      }
    }
  }
}

function calculateHandKind(cards: string, partTwo: boolean): HandKind {
  const counts = {}
  cards.split("").forEach(card => {
    if (!(card in counts)) {
      counts[card] = 0;
    }

    counts[card]++;
  });

  let jCount = 0;
  if (partTwo) {
    jCount = counts["J"];
    delete counts["J"];
  }

  const values = Object.values(counts);
  const highest = values.reduce((a, b) => Math.max(a, b), 0);

  if (values.includes(5) || highest + jCount === 5) {
    return HandKind.FiveOfAKind;
  } else if (values.includes(4) || highest + jCount === 4) {
    return HandKind.FourOfAKind;
  } else if ((values.includes(3) && values.includes(2)) || (values.filter(v => v === 2).length === 2 && jCount === 1)) {
    return HandKind.FullHouse;
  } else if (values.includes(3) || highest + jCount == 3) {
    return HandKind.ThreeOfAKind;
  } else if (values.filter(v => v === 2).length === 2) {
    return HandKind.TwoPair;
  } else if (values.includes(2) || highest + jCount === 2) {
    return HandKind.OnePair;
  }

  return HandKind.HighCard;
};

async function loadPuzzle() {
  const sampleData = `
  32T3K 765
  T55J5 684
  KK677 28
  KTJJT 220
  QQQJA 483
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
