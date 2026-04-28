line = input()

pairs = {
    '(': ')',
    '[': ']',
    '{': '}'
}

def is_valid(s):
    stack = []
    for c in s:
        if c in pairs:
            stack.append(c)
        else:
            if not stack:
                return False
            if pairs[stack.pop()] != c:
                return False
    return not stack


n = len(line)

for i in range(n):
    shifted = line[i:] + line[:i]
    if is_valid(shifted):
        print("YES")
        break
else:
    print("NO")