import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    for i in range(n):
        a,b,c,d,e,f,g,h = list(map(int, input().split()))
        if (abs(c - e) == abs(a - g) and abs(d -f) == abs(b - h)) or (abs(a - c) == abs(e - g) and abs(b - d) == abs(f - h)):
            print('YES')
        else:
            print('NO')


if __name__ == '__main__':
    main()
