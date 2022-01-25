import os
import csv
try:
    import statistics
except:
    #error code instead
    import statistics_standin_for_py2 as statistics

from file_111 import Purchase

def main():
    print_header()
    filename = get_data_file()
    data = load_file(filename)
    query_data(data)


def print_header():
    print('----------------------------------')
    print('    REAL ESTATE DATA MINING APP')
    print('----------------------------------')
    print()


def get_data_file():
    base_folder = os.path.dirname(__file__)
    return os.path.join(base_folder, 'data', '#yourfile.csv')

def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as fin:

        reader = csv.DictReader(fin)
        for row in reader:
            print(type(row), row)
            print("Bed count: {}, type: {}".format(row['beds'], type(row['beds'])))

        # header = fin.readline().strip()
        # reader = csv.reader(fin, delimiter='|')
        # for row in reader:
        #     print(type(row), row)
        #     beds = row[4]



# def load_file_basic(filename):
#     with open(filename, 'r', encoding='utf-8') as fin:
#         header = fin.readline()
#         print('found header: ' + header)
#
#         lines = []
#         for line in fin:
#             line_data = line.strip().split(',')
#             bed_count = line_data[4]
#             lines.append(line_data)
#
#         print(lines[:5])

def get_price(p):
    return p.price


def query_data(data): #: list[Purchase]):
    # if data was sorted by price
    data.sort(key= lambda p: p.price)

    # most expensive house
    high_purchase = data[-1]
    print(high_purchase.price)

    # least expensive house
    low_purchase = data[0]
    print(low_purchase.price)

    #average price house
    # prices = []
    # for pur in data:
    #     if pur.beds == 2:
    #         prices.append(pur.price)
    # prices = [
    #     p.price, p.beds, p.state
    #     for p in data
    # ]
    # print(prices)
    # return


    two_bed_homes = (
        p
        for p in data
        if announce(p, '2-bedrooms, found {}'.format(p.beds)) and p.beds == 2
    )

    homes = []
    for h in two_bed_homes:
        if len(homes) > 5:
            break
        homes.append(h)

    ave_price = statistics.mean((announce(p.price, 'price') for p in two_bed_homes))
    ave_bath = statistics.mean((p.baths for p in two_bed_homes))
    ave_sqft = statistics.mean((p.sq__ft for p in two_bed_homes))
    print("The average price of a 2-bedroom home is ${:,}, baths = {}, sq ft={:,}".format(int(ave_price), round(ave_bath, 1), round(ave_sqft, 1)))

    #average price of 2 bedroom houses
    # prices = []
    # for pur in data:
    #     if pur.beds == 2:
    #         prices.append(pur.price)

def announce(item, msg):
    print("Pulling item {} for {}".format(item, msg))
    return item

if __name__ == '__main__':
    main()
