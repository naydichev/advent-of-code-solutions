#!bun

import * as fs from "fs";

const USE_SAMPLE_DATA = process.argv[2] === "sample";

async function main(args) {
  const tree = parseTree(args.data);

  calculateSize(tree);

  printTree(tree);

  console.log(`Part One: ${solvePuzzle(tree)}`);
  console.log(`Part Two: ${solvePuzzle(tree, true)}`);
}

function parseTree(input) {
  const root = {
    path: "/",
    name: "/",
    children: {},
    size: null,
    type: "dir",
    desc: "dir",
  };

  let cwd = "/";
  let cwdPointer = root;

  input.forEach(el => {
    const parts = el.split(" ");
    if (el.startsWith("$")) {
      const cdParts = parts.slice(1);
      if (cdParts[0] === "cd") {
        if (cdParts[1] === "/") {
          cwd = "/";
          cwdPointer = root;
        } else if (cdParts[1] === "..") {
          cwdPointer = cwdPointer.parent;
          cwd = cwdPointer.path;
        } else {
          if (!cwdPointer.children[cdParts[1]]) {
            cwdPointer.children[cdParts[1]] = {
              parent: cwdPointer,
              name: cdParts[1],
              path: `${cwdPointer.path}${cdParts[1]}/`,
              children: {},
              size: null,
              type: "dir",
              desc: "dir",
            };
          }
          cwdPointer = cwdPointer.children[cdParts[1]];
        }
      }
    } else {
      // ignore dirs because they're handled by cd?
      if (parts[0] !== "dir") {
        cwdPointer.children[parts[1]] = {
          parent: cwdPointer,
          name: parts[1],
          path: `${cwdPointer.path}${parts[1]}`,
          size: parseInt(parts[0]),
          type: "file",
          desc: `file, size=${parts[0]}`,
        };
      }
    }
  });

  return root;
}

function solvePuzzle(tree, partTwo = false) {
  function recurseOne(tree) {
    if (tree.type === "file") {
      return 0;
    }

    let size = 0;
    if (tree.size <= 100000) {
      size += tree.size;
    }

    return size + Object.values(tree.children)
      .reduce((acc, x) => acc + recurseOne(x), 0);
  }

  if (!partTwo) {
    return recurseOne(tree);
  }

  const totalSize = 70000000;
  const currentAvailable = totalSize - tree.size;
  const target = 30000000;
  const requiredSize = target - currentAvailable;

  function recurseTwo(tree) {
    if (tree.type === "file") {
      return [];
    }

    let options = [];
    if (tree.size >= requiredSize) {
      options.push(tree);
    }

    return Object.values(tree.children)
      .reduce((acc, x) => acc.concat(recurseTwo(x)), options);
  }

  return recurseTwo(tree)
    // .map(i => {
    //   console.log(`possible option for deletion: ${i.path} - ${i.size}`)
    //   return i;
    // })
    .sort((a, b) => a.size > b.size)[0]
    .size;

}

function calculateSize(tree) {
  if (tree.type === "file") {
    return tree.size;
  }

  tree.size = Object.values(tree.children)
    .reduce((acc, x) => acc + calculateSize(x), 0);
  tree.desc = `dir, size=${tree.size}`;

  return tree.size;
}

function printTree(tree, indent = 0) {
  console.log(`${"  ".repeat(indent)} - ${tree.name} (${tree.desc})`);
  if (tree.type === "dir") {
    Object.values(tree.children)
      .sort((a, b) => a.name > b.name)
      .forEach((dir) => printTree(dir, indent + 1));
  }
}

async function loadPuzzle() {
  const sampleData = `
  $ cd /
  $ ls
  dir a
  14848514 b.txt
  8504156 c.dat
  dir d
  $ cd a
  $ ls
  dir e
  29116 f
  2557 g
  62596 h.lst
  $ cd e
  $ ls
  584 i
  $ cd ..
  $ cd ..
  $ cd d
  $ ls
  4060174 j
  8033020 d.log
  5626152 d.ext
  7214296 k
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
