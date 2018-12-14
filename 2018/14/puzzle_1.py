#!/usr/bin/python

def main():
    start = [3, 7]
    p_1 = 0
    p_2 = 1

    n = 825401
    i = 0

    print_scores(start, p_1, p_2)
    while i < n + 10:
        score = start[p_1] + start[p_2]

        if score < 10:
            start.append(score)
        else:
            s1 = score // 10
            s2 = score % 10

            start.append(s1)
            start.append(s2)

        start_len = len(start)
        p_1 = (p_1 + start[p_1] + 1) % start_len
        p_2 = (p_2 + start[p_2] + 1) % start_len

        i = start_len

#        print_scores(start, p_1, p_2)

    print("".join(str(s) for s in start[n:n+10]))

def print_scores(scores, p1, p2):
    l = []
    for i, s in enumerate(scores):
        if i == p1:
            l.append("({})".format(s))
        elif i == p2:
            l.append("[{}]".format(s))
        else:
            l.append(str(s))

    print(" ".join(l))


if __name__ == "__main__":
    main()
