stack = []
with open('input.txt', 'r', encoding='utf8') as fin:
    for line in fin:
        op = line.split()

        if op[0] == 'push':
            stack.append(int(op[1]))
            print('ok')
        elif op[0] == 'size':
            print(len(stack))
        elif op[0] == 'back':
            if stack:
                print(stack[-1])
            else:
                print('error')
        elif op[0] == 'pop':
            if stack:
                print(stack.pop())
            else:
                print('error')
        elif op[0] == 'clear':
            stack.clear()
            print('ok')
        elif op[0] == 'exit':
            print('bye')
            break