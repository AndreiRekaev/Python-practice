from collections import defaultdict

def happy(K, nums):


    prefix_sum = 0
    count = defaultdict(int)
    count[0] = 1
    ans = 0

    for num in nums:
        prefix_sum += num
        ans += count[prefix_sum - K]
        count[prefix_sum] += 1

    return ans


N, K = list(map(int,input().split()))
nums = list(map(int,input().split()))
print(happy(K,nums))

