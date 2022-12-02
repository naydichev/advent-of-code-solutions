#!bun

import * as fs from "fs";

const THROW_MAP = {
    A: "ROCK",
    B: "PAPER",
    C: "SCISSORS",
    X: "ROCK",
    Y: "PAPER",
    Z: "SCISSORS",
};

const PLAY_MAP = {
    X: "LOSE",
    Y: "DRAW",
    Z: "WIN",
};

const POINTS = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3
};

const WIN_MAP = {
    ROCK: "PAPER",
    PAPER: "SCISSORS",
    SCISSORS: "ROCK",
};

const LOSE_MAP = {
    ROCK: "SCISSORS",
    PAPER: "ROCK",
    SCISSORS: "PAPER",
};


function calculatePoints(data, partTwo = false) {
    let points = 0;

    data.forEach(match => {
        let { mine, opponent, play } = match;
        if (partTwo) {
            if (play === "LOSE") {
                mine = LOSE_MAP[opponent];
            } else if (play === "DRAW") {
                mine = opponent;
            } else {
                mine = WIN_MAP[opponent];
            }
            // console.log(match, play, opponent, mine);
        }

        if (opponent === mine) {
            points += 3;
        } else if (mine === WIN_MAP[opponent]) {
            points += 6;
        }

        points += POINTS[mine];
    });

    return points;
}

async function main(args) {

    console.log(`Part One: ${calculatePoints(args.data)}`);
    console.log(`Part Two: ${calculatePoints(args.data, true)}`);
}

async function loadPuzzle() {
    const data = fs.readFileSync(`${__dirname}/input.aoc`, "utf8")
    // const data = "A Y\nB X\nC Z\n"
        .trim()
        .split("\n")
        .map(s => s.trim());

    const processed = data
        .map(i => {
            const [opponent, mine] = i.split(" ");

            return {
                opponent: THROW_MAP[opponent],
                mine: THROW_MAP[mine],
                play: PLAY_MAP[mine],
            };
        });

    return processed;
}

await main({ data: await loadPuzzle() })
