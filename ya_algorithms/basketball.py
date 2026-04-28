import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    players = []
    scores = {}
    prev_a, prev_b = 0, 0
    for i in range(n):
        name = input()
        players.append(name)
        scores[name] = 0

    m = int(input())
    for j in range(m):
        line = input()
        score, name = line.split()
        a,b = map(int, score.split(':'))

        delta = (a - prev_a) + (b - prev_b)

        scores[name] += delta

        prev_a, prev_b = a, b

    best_name = ""
    best_score = -1
    for p in players:
        if scores[p] > best_score:
            best_score = scores[p]
            best_name = p

    print(best_name, best_score)



if __name__ == '__main__':
    main()
