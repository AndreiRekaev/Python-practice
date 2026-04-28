import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(*sorted(set(a).intersection(b)))


if __name__ == '__main__':
    main()
