def solve(n, comp):
    if n == 1:
        return [1]
    now_sum = comp[0]
    first_winner = n
    last_loser = 0
    for i in range(1, n-1):
        now_sum += comp[i]
        if comp[i] > comp[i - 1] and now_sum > comp[i + 1]:
            if first_winner == n:
                first_winner = i
        if now_sum <= comp[i + 1]:
            last_loser = i
    winner_pos = max(first_winner, last_loser + 1)
    ans = [0] * winner_pos + [1] * (n - winner_pos)
    if comp[n - 1] > comp[n - 2]:
        ans[n - 1] = 1
    return ans



n = int(input())
comp = list(map(int, input().split()))
print(*solve(n, comp))


