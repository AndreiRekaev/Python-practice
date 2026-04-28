
def gen(X0, N, Q):
    X = [X0]
    res = []
    for i in range(1, 2*Q):
        X.append((11173 * X[i - 1] + 1) % 1000000007)
    for q in range(Q):
        L = min(X[2 * q] % N, X[2*q + 1] % N)
        R = max(X[2*q] % N, X[2*q + 1] % N)
        res.append((L,R))
    return res


N = int(input())
A = list(map(int,input().split()))
Q = int(input())
X0 = int(input())
seq = gen(X0, N, Q)
prefixes = [A[0]]
for i in range(1,N):
    prefixes.append(prefixes[i - 1] + A[i])
ans = 0
for j in seq:
    ans += prefixes[j[1]] - prefixes[j[0]]
    print(ans)
print(ans % 1000000007)






