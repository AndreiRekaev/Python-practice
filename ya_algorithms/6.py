import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    l = list(map(int, input().split()))
    street = [0] * len(l)
    market = -100
    for i in range(len(l)):
        if l[i] == 2:
            market = i
        if l[i] == 1:
            street[i] = i - market

    ans = 0
    market = 100
    for k in range(len(l) - 1, -1, -1):
        if l[k] == 2:
            market = k
        if l[k] == 1:
            street[k] = min(street[k], market - k)
            ans = max(ans, street[k])

    print(ans)


if __name__ == '__main__':
    main()
