

n, r = map(int, input().split())
d = list(map(int, input().split()))
j = 0
count = 0
for i in range(n):
    while j < n and d[j] - d[i] <= r:
        j += 1
    count += n - j
    print(count)
print(count)


