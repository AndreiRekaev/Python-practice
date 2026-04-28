import sys

def get_pair(k, words):
    cnt = {}
    for w in words:
        prefix = w[:k]
        if prefix not in cnt:
            cnt[prefix] = 0
        cnt[prefix] += 1
    for v in cnt.values():
        if v % 2 != 0:
            return False
    return True


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    n = int(input())
    words = []
    for _ in range(n):
        words.append(input())
    l, r = 0, len(words[0])
    ans = 0

    while l <= r:
        mid = (l + r) // 2
        if get_pair(mid, words):
            ans = mid
            l = mid + 1
        else:
            r = mid - 1
    print(ans)



if __name__ == '__main__':
    main()
