import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    a = int(input())
    b = int(input())
    c = int(input())
    d = int(input())
    res = []
    if a > 0 and c > 0:
        res.append([b + 1, d + 1])

    if b > 0 and d > 0:
        res.append([a + 1, c + 1])

    if a > 0 and b > 0:
        res.append([max(a, b) + 1, 1])
    if c > 0 and d > 0:
        res.append([1, max(c, d) + 1])
    res = min(res, key=sum)

    print(*res)


if __name__ == '__main__':
    main()
