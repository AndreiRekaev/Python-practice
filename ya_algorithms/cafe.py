cases = int(input())

for _ in range(cases):
    n, d = map(int, input().split())
    T = []
    K = []

    for _ in range(n):
        ti, ki = map(int, input().split())
        T.append(ti)
        K.append(ki)

    wait = [0] * n
    for i in range(1, n):
        wait[i] = wait[i - 1] + K[i - 1]

    terp = [T[i] - wait[i] for i in range(n)]

    suf = [0] * n
    suf[-1] = terp[-1]
    for i in range(n - 2, -1, -1):
        suf[i] = min(terp[i], suf[i + 1])

    ans = n + 1
    for pos in range(n):
        if suf[pos] >= d:
            ans = pos + 1
            break

    print(ans)