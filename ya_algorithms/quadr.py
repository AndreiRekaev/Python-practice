

n, m = map(int,input().split())
snapshot = []
for _ in range(n):
    snapshot.append(input())

ans = 0
for i in range(n):
    for j in range(m):
        if snapshot[i][j] == '#':
            d = (i == n - 1 or snapshot[i + 1][j] == '.')
            r = (j == m - 1 or snapshot[i][j + 1] == '.')
            if d and r:
                ans += 1

print(ans)