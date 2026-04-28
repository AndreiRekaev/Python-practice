import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    t = set()
    for i in range(n):
        a, b = map(int, input().split())
        if a + b == n - 1:
            t.add((a,b)) 
    print(len(t))

if __name__ == '__main__':
    main()
