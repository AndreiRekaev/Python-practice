s = input()
n = len(s)
s += '**'
ans = []
now_pos = 0
while now_pos < n:
    if s[now_pos + 2] == '#':
        num = s[now_pos:now_pos + 2]
        now_pos += 3
    else:
        num = s[now_pos]
        now_pos += 1
    ans.append(chr(ord('a') + int(num) - 1))
print(''.join(ans))
