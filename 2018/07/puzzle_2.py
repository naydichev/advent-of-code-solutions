#!/usr/bin/python

from collections import defaultdict

def main():
    with open("instructions.pi") as f:
        raw_steps = f.read().split("\n")

    steps = parse_steps(raw_steps)

    print("Time\tW1\t\tW2\t\tW3\t\tW4\t\tW5\t\tIn-Prog\tDone")
    time_taken = determine_step_order(steps)

    print("it took the elves {} seconds".format(time_taken))


def parse_steps(raw_steps):
    steps = defaultdict(set)

    for step in raw_steps:
        parts = step.split()
        steps[parts[-3]].add(parts[1])
        steps[parts[1]]

    return steps

def determine_step_order(steps):
    letters = []
    workers = [Worker(None) for i in range(5)]
    working_on = set()
    time_taken = 0

    while len(steps) or any(not w.done for w in workers):


        for i, worker in enumerate(workers):
            worker.tick()
            if worker.done and worker.letter is not None:
                l = worker.letter
                letters.append(l)
                working_on.discard(l)

                [steps[key].discard(l) for key in steps.keys()]
                worker.letter = None

        next_steps = sorted([key for key in steps.keys() if len(steps[key]) == 0 and key not in working_on], reverse=True)

        for i, worker in enumerate(workers):
            if worker.letter is None:
                if len(next_steps):
                    l = next_steps.pop()
                    workers[i] = Worker(l)
                    working_on.add(l)
                    steps.pop(l)

        print_status(time_taken, workers, working_on, letters)
        time_taken += 1

    return time_taken - 1

def print_status(time_taken, workers, working_on, letters):
    items = [time_taken]
    items.extend([w.status for w in workers])
    items.append("".join(working_on))
    items.append("".join(letters))
    print " {:03d}\t{}\t{}\t{}\t{}\t{}\t{:5}\t{}".format(*items)


class Worker:
    def __init__(self, letter):
        self.letter = letter

        if letter is not None:
            self.time = 60 + ord(letter) - ord('A') + 1
        else:
            self.time = 0

    @property
    def done(self):
        return self.time <= 0

    def tick(self):
        self.time -= 1

    @property
    def status(self):
        if self.letter is None:
            return "{:6}".format(".")
        else:
            return "{} ({:02d})".format(self.letter, self.time)

if __name__ == "__main__":
    main()
