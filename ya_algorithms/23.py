

N = int(input())
t_shirts = list(map(int, input().split()))
M = int(input())
pants = list(map(int, input().split()))

i, j = 0, 0
best_diff = abs(t_shirts[0] - pants[0])
best_i, best_j = 0, 0

while i < N and j < M:
    diff = abs(t_shirts[i] - pants[j])

    if diff < best_diff:
        best_i = i
        best_j = j
        best_diff = diff

    if t_shirts[i] < pants[j]:
        i += 1
    else:
        j += 1

print(t_shirts[best_i], pants[best_j])


