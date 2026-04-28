import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    a = int(input())
    b = int(input())
    c = int(input())
    if c < 0:
        print('NO SOLUTION')
    elif a == 0:
        if b == c * c:
            print('MANY SOLUTIONS')
        else:
            print('NO SOLUTION')
    else:
        if (c * c - b) % a == 0:
            print((c ** 2 - b) // a)
        else:
            print('NO SOLUTION')


if __name__ == '__main__':
    main()
