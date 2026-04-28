import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n, m = map(int, input().split())
    events = []
    for i in range(n):
        l, r, x = map(int, input().split())
        events.append((l,r,x))

    for i in range(m):
        num = int(input())
        ans = 0
        for l,r,x in events:
            if l <= num and num <= r:
                if (num - l) % 2 == 0:
                    ans += x
                else:
                    ans -= x
        print(ans)

if __name__ == '__main__':
    main()
