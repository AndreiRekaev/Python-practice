import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    d = {}
    for i in range(n):
        k, v = input().split()
        d[k] = v
    q = input()
    for k, v in d.items():
        if v == q:
            print(k)
        if k == q:
            print(v)

if __name__ == '__main__':
    main()
