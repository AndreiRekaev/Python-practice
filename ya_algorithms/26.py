from collections import defaultdict

n,k = map(int, input().split())
a = list(map(int, input().split()))

count = defaultdict(int)
unique = 0
best_len = n + 1
best_l = best_r = 0

r=0
for l in range(n):
    while r < n and unique < k:
        count[a[r]] += 1
        if count[a[r]] == 1:
            unique += 1
        r += 1

    if unique == k:
        curr_len = r - l
        if curr_len < best_len:
            best_len = curr_len
            best_l = l + 1
            best_r = r

    count[a[l]] -= 1
    if count[a[l]] == 0:
        unique -= 1

print(best_l, best_r)