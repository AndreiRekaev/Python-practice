

N = int(input())
nums = list(map(int, input().split()))
i = 0
stack = []
expected = 1
while i < N:
    stack.append(nums[i])
    while stack and stack[-1] == expected:
        stack.pop()
        expected += 1
    i += 1

if expected == N + 1:
    print('YES')
else:
    print('NO')