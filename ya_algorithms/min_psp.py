
n = int(input())
w = input()
s = input()

closing = {
    ')':'(',
    ']': '['
}

def min_psp(n, w, s):
    result = list(s)
    stack = []

    for c in s:
        if c in closing:
            stack.pop()
        else:
            stack.append(c)


    for i in range(n - len(s)):
        for c in w:
            if c in closing and len(stack) > 0 and stack[-1] == closing[c]:
                result.append(c)
                stack.pop()
                break
            elif c not in closing and n - len(s) - i > len(stack):
                result.append(c)
                stack.append(c)
                break

    print(''.join(result))


min_psp(n, w, s)