n = int(input())
correct = input()
m = int(input())
answers = [input() for _ in range(m)]


correct_count = [0] * m
for i in range(m):
    for j in range(n):
        if answers[i][j] == correct[j]:
            correct_count[i] += 1

pairs = []
for i in range(m):
    for j in range(i + 1, m):
        common_correct = 0
        common_wrong = 0

        for k in range(n):
            if answers[i][k] == correct[k] and answers[j][k] == correct[k]:
                common_correct += 1
            elif (answers[i][k] != correct[k] and answers[j][k] != correct[k]
                  and answers[i][k] == answers[j][k]):
                common_wrong += 1

        if (common_correct * 2 > correct_count[i] and
                common_correct * 2 > correct_count[j] and
                common_wrong * 2 > (n - correct_count[i]) and
                common_wrong * 2 > (n - correct_count[j])):
            pairs.append((i + 1, j + 1))

print(len(pairs))
for i, j in pairs:
    print(i, j)