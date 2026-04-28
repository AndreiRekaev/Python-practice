

n = int(input())
a = list(map(int, input().split()))

forbidden = [False] * n

for i in range(n):
    val = a[i]
    shift = (val - (i + 1)) % n
    forbidden[shift] = True

for j in range(n):
    if not forbidden[j]:
        print(j)
        break
else:
    print(-1)