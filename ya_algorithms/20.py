

n = int(input())
a = list(map(int, input().split()))
s = a[0]
ans = a[0]
for i in range(1,n):
    s = max(a[i], a[i] + s)
    ans = max(ans, s)
print(ans)

