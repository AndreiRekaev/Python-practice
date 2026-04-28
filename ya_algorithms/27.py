from collections import defaultdict

n,k = map(int, input().split())
s = input()

m = defaultdict(int)
best_len = 0
best_l = 0
r = 0

for l in range(n):
    while r < n and m[s[r]] < k:
        m[s[r]] += 1
        r += 1

    if best_len < r - l:
        best_len = r - l
        best_l = l

    m[s[l]] -= 1

print(best_len, best_l + 1)



