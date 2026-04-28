import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    s = input()
    l = 0
    ans = 0
    for i in range(len(s)):
        if s[i] not in ('a', 'h'):
            l = 0
            continue

        if l == 0:
            l = 1
        else:
            if s[i] != s[i - 1]:
                l += 1
            else:
                l = 1
        if l > ans:
            ans = l
    print(ans)

    print(ans)


if __name__ == '__main__':
    main()
