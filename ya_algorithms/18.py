
n = int(input())
pr_sum = []
nums = input().split()
for i in range(len(nums)):
    if i == 0:
        pr_sum.append(int(nums[i]))
    else:
        pr_sum.append(int(nums[i]) + int(pr_sum[i - 1]))

print(*pr_sum)


