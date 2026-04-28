import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    s = input()
    res = []
    i = 0
    n = len(s)

    while i < n:
        if s[i] == ' ':
            i += 1
            continue

        start = 0
        while i < n and s[i] == "'":
            start += 1
            i += 1

        w = i
        while i < n and s[i].isalpha():
            i += 1
        word = s[w:i]

        end = 0
        while i < n and s[i] == "'":
            end += 1
            i += 1

        r = word[start:len(word) -end]
        res.append(r)
    print(''.join(res))


if __name__ == '__main__':
    main()
