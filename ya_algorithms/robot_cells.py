from collections import defaultdict

line = input()
x, y = (0,0)
field = {}
field[(x,y)] = 1
for c in line:
    if c == 'U':
        y +=1
    elif c == 'R':
        x += 1
    elif c == 'L':
        x -= 1
    elif c == 'D':
        y -= 1

    field[(x,y)] = field.get((x, y), 0) + 1

ans = sum(1 for v in field.values() if v > 1)
print(ans)
