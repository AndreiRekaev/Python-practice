import math

def round_correct(x):
    frac = x - math.floor(x)
    if frac <= 0.5:
        return math.floor(x)
    else:
        return math.ceil(x)

s = input()

grades = [ord(c) - 64 for c in s]

average = sum(grades) / len(s)

average = round_correct(average)

worst = max(grades)

average = max(worst - 1, average)

print(chr(average + 64))