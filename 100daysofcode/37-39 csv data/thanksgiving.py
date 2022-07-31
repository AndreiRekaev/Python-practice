import os
import csv
import re



def init():
    income = 0
    error = 0
    dishes = set()
    base_folder = os.path.dirname(__file__)
    filename = os.path.join(base_folder, 'thanksgiving-2015-poll-data.csv')

    region = input('Input your region: ')
    salary = input('What is your income range?: ')
    try:
        income = int(salary)
    except ValueError:
        error = 1
        print('Invalid input. Try again!')

    if error == 0:

        with open(filename, 'r', encoding='utf-8') as fin:
            reader = csv.reader(fin)
            next(reader)

            for row in reader:
                nlist = re.findall(r'\d+', row[63])
                nlist = ''.join(nlist[:-2])
                if nlist == '':
                    continue
                elif income >= int(nlist) and region == row[64]:
                    for i in range(65):
                        if i >= 2 and i < 4:
                            dishes.add(row[i])
                        if i >= 11 and i < 24:
                            dishes.add(row[i])
                        if i >= 26 and i < 36:
                            dishes.add(row[i] + ' pie')
                        if i >= 39 and i < 48:
                            dishes.add(row[i])
        dishes.discard('')
        dishes.discard('Other (please specify)')
    return dishes





def main():
    print("Thanksgiving menu")
    print()

    dishes = init()

    if len(dishes):
        print("5 dishes for you on Thanksgiving day: ")

        for idx, d in enumerate(list(dishes)[:5]):
            print(f"{idx + 1}. {d}")

        print('Bon appetit!')
    else:
        print('No data. Try again!')


if __name__ == '__main__':
    main()
