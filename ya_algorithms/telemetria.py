

n,m,k = map(int, input().split())
windows = ['']*n
cur = 0
buffer = ''

for _ in range(m):
    l = input()
    if l == 'Copy':
        windows[cur] = windows[cur]
        buffer = windows[cur][-k:]
    elif l == 'Paste':
        windows[cur] += buffer
    elif l == 'Backspace':
        if windows[cur]:
            windows[cur] = windows[cur][:-1]
    elif l == 'Next':
        cur = (cur +1)%n
    else:
        windows[cur] +=l

res = windows[cur][-k:]
if res:
    print(res)
else:
    print('Empty')
