import math


def main():
    n = int(input())

    ans = 10**12
    check = [n, 2*n -1, 2*n, 2*n + 1]

    for c in check:
        for x in range(1, int(math.sqrt(c)) + 1):
            if c % x == 0:
                ans = min(ans, abs(x - (n + x -1) // x))

    print(ans)


if __name__ == '__main__':
    main()