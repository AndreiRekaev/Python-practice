
n = int(input())
a = list(map(int, input().split()))

pref = [0] * (n + 1)
for i in range(n):
    pref[i + 1] = pref[i] + a[i]

total = pref[n]

best_diff = float('inf')
best_l = best_r = 0

r = n
for l in range(1, n):

    while r > l + 1:
        cur = abs(pref[l] - (total - pref[r - 1]))
        next_val = abs(pref[l] - (total - pref[r - 2]))
        if next_val <= cur:
            r -= 1
        else:
            break

    diff = abs(pref[l] - (total - pref[r - 1]))
    if diff < best_diff:
        best_diff = diff
        best_l = l
        best_r = r

    if r > l + 1:
        diff2 = abs(pref[l] - (total - pref[r - 2]))
        if diff2 < best_diff:
            best_diff = diff2
            best_l = l
            best_r = r - 1


print(best_diff, best_l, best_r)