
MOD = 1000000007

n = int(input())
a = list(map(int, input().split()))
sum_three_mul = sum(a) % MOD
left_sum = 0
ans = 0
for i in range(n):
    sum_three_mul = (sum_three_mul - a[i]) % MOD
    ans = (ans + a[i] * left_sum * sum_three_mul) % MOD
    left_sum = (left_sum + a[i]) % MOD
print(ans)

