import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    s = input()
    d = {}
    r = ''
    for i in s:
        if i not in d:
            d[i] = 0
        d[i] += 1

    keys = sorted(list(d.keys()))
    center = ''
    for k in keys:
        if d[k] % 2 != 0 and not center:
            center = k
        r = r + k * (d[k] // 2)
    r = r + center + r[::-1]
    print(r)



if __name__ == '__main__':
    main()
