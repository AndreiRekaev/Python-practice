import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    db = {}
    with open('input.txt', 'r', encoding='utf8') as fin:
        for line in fin:
            c, p, q = line.split()
            q = int(q)

            if c not in db:
                db[c] = {p: q}
            else:
                if p in db[c]:
                    db[c][p] += q
                else:
                    db[c][p] = q

    for cu in sorted(db.keys()):
        print(f'{cu}:')
        for product in sorted(db[cu].keys()):
            print(f'{product} {db[cu][product]}')



if __name__ == '__main__':
    main()
