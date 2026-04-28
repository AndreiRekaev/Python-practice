import sys


def folds(a, b):
    cnt = 0
    while a > b:
        a = (a+1) // 2
        cnt += 1
    return cnt


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n, m, h, w = map(int, input().split())

    if (n <= h and m <= w) or (n <= w and m <= h):
        print(0)
        return

    cnt1 = folds(n, h) + folds(m, w)
    cnt2 = folds(n, w) + folds(m, h)

    print(min(cnt1, cnt2))


if __name__ == '__main__':
    main()
