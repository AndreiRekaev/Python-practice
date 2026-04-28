import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    un = set()
    first = set()
    langs = set()
    for i in range(n):
        m = int(input())
        for j in range(m):
            l = input()
            langs.add(l)
            if l not in un:
                un.add(l)
        if i == 0:
            first = langs
        first = first.intersection(langs)
        langs.clear()
    print(len(first))
    for item in first:
        print(str(item))
    print(len(un))
    for item in un:
        print(str(item))






if __name__ == '__main__':
    main()
