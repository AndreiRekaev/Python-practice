import sys


def main():
    """
    Пример ввода и вывода числа n, где -10^9 < n < 10^9:
    n = int(input())
    print(n)
    """
    bank = {}
    with open('input.txt', 'r', encoding='utf8') as fin:
        for line in fin:
            op = line.split()
            if 'DEPOSIT' in line:
                if op[1] not in bank:
                    bank[op[1]] = 0
                bank[op[1]] += int(op[2])
            elif 'WITHDRAW' in line:
                if op[1] not in bank:
                    bank[op[1]] = 0
                bank[op[1]] -= int(op[2])
            elif 'BALANCE' in line:
                if op[1] in bank:
                    print(bank[op[1]])
                else:
                    print('ERROR')
            elif 'TRANSFER' in line:
                if op[1] not in bank:
                    bank[op[1]] = 0
                if op[2] not in bank:
                    bank[op[2]] = 0
                bank[op[1]] -= int(op[3])
                bank[op[2]] += int(op[3])
            elif 'INCOME' in line:
                for k,v in bank.items():
                    if v > 0:
                        bank[k] = v + v * int(op[1]) // 100


if __name__ == '__main__':
    main()