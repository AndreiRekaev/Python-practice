from collections import defaultdict

n = int(input())
p = list(map(int, input().split()))

mem = defaultdict(int)
l = 0
ans = 0

for r in range(n):
    mem[p[r]] += 1

    while len(mem) > 2:
        mem[p[l]] -= 1
        if mem[p[l]] == 0:
            del mem[p[l]]
        l += 1

    if len(mem) == 2:
        ans = max(ans, r - l + 1)

print(ans)