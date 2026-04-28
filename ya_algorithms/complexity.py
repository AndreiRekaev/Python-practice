import sys


def main(p, v, q, m):
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    s_v = p - v
    e_v = p + v
    s_m = q - m
    e_m = q + m

    if max(s_v, s_m) <= min(e_v, e_m):
        print(max(e_v, e_m) - min(s_v, s_m) + 1)
    else:
        print((e_v - s_v + 1) + (e_m - s_m + 1))




if __name__ == '__main__':
    p, v = map(int, input().split())
    q, m = map(int, input().split())
    main(p, v, q, m)