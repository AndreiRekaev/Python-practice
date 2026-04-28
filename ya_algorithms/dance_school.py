
n = int(input())


count = {0: 1}
prefix_sum = 0
ans = 0

for ch in input():
    if ch == 'a':
        prefix_sum += 1
    else:
        prefix_sum -= 1

    ans += count.get(prefix_sum, 0)

    count[prefix_sum] = count.get(prefix_sum, 0) + 1

print(ans)