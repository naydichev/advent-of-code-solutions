#!/usr/bin/python

from copy import deepcopy

def main():
    with open("instructions.pi") as f:
        raw_steps = f.read().split("\n")

    steps = parse_steps(raw_steps)

    print("Time\tW1\t\tW2\t\tW3\t\tW4\t\tW5\t\tIn-Prog\tDone")
    time_taken = determine_step_order(steps)

    print("it took the elves {} seconds".format(time_taken))


def parse_steps(raw_steps):
    steps = {chr(k): set() for k in range(ord('A'), ord('Z') + 1)}

    for step in raw_steps:
        parts = step.split()
        steps[parts[-3]].add(parts[1])

    return steps

def determine_step_order(steps):
    my_steps = deepcopy(steps)
    letters = []
    workers = [NoneWorker() for i in range(5)]
    working_on = set()
    time_taken = 0

    while len(my_steps):

        # first check for done workers
        for i, worker in enumerate(workers):
            if worker.done and not isinstance(worker, NoneWorker):
                l = worker.letter
                letters.append(l)
                working_on.discard(l)

                del my_steps[l]
                for key in my_steps.keys():
                    my_steps[key].discard(l)

                workers[i] = NoneWorker()

        next_steps = sorted([key for key, val in my_steps.items() if len(val) == 0 and not any([key == w.letter for w in workers])])

        for i, worker in enumerate(workers):
            if isinstance(worker, NoneWorker):
                if len(next_steps):
                    l = next_steps.pop()
                    workers[i] = Worker(l)
                    working_on.add(l)
            else:
                worker.tick()

        print_status(time_taken, workers, working_on, letters)
        time_taken += 1

    return time_taken - 1

def print_status(time_taken, workers, working_on, letters):
    items = [time_taken]
    items.extend([w.status for w in workers])
    items.append("".join(working_on))
    items.append("".join(letters))
    print " {:03d}\t{}\t{}\t{}\t{}\t{}\t{:5}\t{}".format(*items)


class NoneWorker:
    @property
    def done(self):
        return True

    @property
    def letter(self):
        return None

    @property
    def status(self):
        return ".     "

class Worker:
    def __init__(self, letter):
        self.letter = letter
        self.time = 60 + ord(letter) - ord('A')

    @property
    def done(self):
        return self.time <= 0

    def tick(self):
        self.time -= 1

    @property
    def status(self):
            return "{} ({:02d})".format(self.letter, self.time)

if __name__ == "__main__":
    main()
