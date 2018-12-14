#!/usr/bin/python

def main():
    scores = [3, 7]
    p_1 = 0
    p_2 = 1

    n = 825401
    nlist = [int(s) for s in str(n)]

    while scores[-len(nlist):] != nlist and scores[-len(nlist)-1:-1] != nlist:
        score = scores[p_1] + scores[p_2]

        if score < 10:
            scores.append(score)
        else:
            s1 = score // 10
            s2 = score % 10

            scores.append(s1)
            scores.append(s2)

        scores_len = len(scores)
        p_1 = (p_1 + scores[p_1] + 1) % scores_len
        p_2 = (p_2 + scores[p_2] + 1) % scores_len

        i = scores_len

#        print_scores(scores, p_1, p_2)

    sub = 0
    if scores[-len(nlist):] != nlist:
        sub = 1

    print(len(scores) - len(nlist) - 1)
    print("".join(str(s) for s in scores[n:n+10]))

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
