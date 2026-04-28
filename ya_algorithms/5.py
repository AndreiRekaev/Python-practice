import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    troom, tcond = map(int, input().split())
    mode = input()
    if mode == 'heat':
        if troom > tcond:
            print(troom)
        else:
            print(tcond)
    if mode == 'freeze':
        if troom > tcond:
            print(tcond)
        else:
            print(troom)
    if mode == 'auto':
        print(tcond)
    if mode == 'fan':
        print(troom)

if __name__ == '__main__':
    main()
