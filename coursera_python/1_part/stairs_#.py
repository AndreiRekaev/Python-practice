import sys

digit_string = int(sys.argv[1])

for step in range(1, digit_string+1):
    print(' '*(digit_string - step) + '#'*(step))
