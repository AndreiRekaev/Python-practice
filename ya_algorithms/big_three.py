# def main():
#     s = input().strip()
#
#     digits = list(map(int, s))
#     digits.sort()
#
#     groups = {0: [], 1: [], 2: []}
#
#     for d in digits:
#         groups[d % 3].append(d)
#
#     total = sum(digits)
#
#     def remove_digits(rem, count):
#         if len(groups[rem]) >= count:
#             for _ in range(count):
#                 groups[rem].pop(0)
#             return True
#         return False
#
#     r = total % 3
#
#     if r == 1:
#         if not remove_digits(1, 1):
#             remove_digits(2, 2)
#     elif r == 2:
#         if not remove_digits(2, 1):
#             remove_digits(1, 2)
#
#     # собираем все цифры обратно
#     res = groups[0] + groups[1] + groups[2]
#
#     # сортируем по убыванию
#     res.sort(reverse=True)
#
#     print(''.join(map(str, res)))
#
#
# if __name__ == '__main__':
#     main()
import sys

def dec_cnt_digits(digits_cnt, digits):
    for digit in digits:
        if digits_cnt.get(digit, 0) > 0:
            digits_cnt[digit] -= 1
            return True, digits_cnt
    return False, digits_cnt

digits = list(map(int, input()))
digits_sum = sum(digits)
digits_cnt = {}
for digit in digits:
    digits_cnt[digit] = digits_cnt.get(digit, 0) + 1

mod1_digits = (1, 4, 7)
mod2_digits = (2,5,8)

if digits_sum % 3 == 1:
    flag, digits_cnt = dec_cnt_digits(digits_cnt, mod1_digits)
    if not flag:
        flag, digits_cnt = dec_cnt_digits(digits_cnt, mod2_digits)
        flag, digits_cnt = dec_cnt_digits(digits_cnt, mod2_digits)
if digits_sum % 3 == 2:
    flag, digits_cnt = dec_cnt_digits(digits_cnt, mod2_digits)
    if not flag:
        flag, digits_cnt = dec_cnt_digits(digits_cnt, mod1_digits)
        flag, digits_cnt = dec_cnt_digits(digits_cnt, mod1_digits)

ans = []
for digit in range(9, -1, -1):
    ans.append(str(digit)* digits_cnt.get(digit, 0))
print(''.join(ans))