
line = input()
stack = []
pairs = {
        '(': ')',
        '[': ']',
        '{': '}'
    }
for p in line:
    if p in pairs:
        stack.append(p)
    else:
        if not stack:
            stack.append(p)
            break
        else:
            top = stack.pop()
            if pairs[top] != p:
                stack.append(p)
                break

if not stack:
    print('yes')
else:
    print('no')