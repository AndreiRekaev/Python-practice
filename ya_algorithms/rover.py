import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    INF = 10 ** 18
    l, r = -INF, INF
    for _ in range(n):
        x, d = map(int, input().split())
        left = x - d
        right = x + d

        l = max(l,left)
        r = min(r, right)
    if l > r:
        print(-1)
    else:
        print(r)



if __name__ == '__main__':
    main()
