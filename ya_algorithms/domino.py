import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n, m = map(int, input().split())
    if n < 0 or m < 0:
        print(-2)
        return

    field = [input().strip() for _ in range(n)]

    ans = 0
    for i in range(n):
        for j in range(m):
            if j < m - 1:
                if field[i][j] == '.' and field[i][j+1] == '.':
                    ans += 1
            if i < n - 1:
                if field[i][j] == '.' and field[i + 1][j] == '.':
                    ans += 1
    print(ans)


if __name__ == '__main__':
    main()
