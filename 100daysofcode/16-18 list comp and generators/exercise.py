# Look at your code and see if you can refactor it to use list comprehensions. Same for generators. Are you building up a list somewhere where you could potentially use a generator?

# And/or exercise here, take this list of names:

# NAMES = ['arnold schwarzenegger', 'alec baldwin', 'bob belderbos',
#          'julian sequeira', 'sandra bullock', 'keanu reeves',
#          'julbob pybites', 'bob belderbos', 'julian sequeira',
#          'al pacino', 'brad pitt', 'matt damon', 'brad pitt']
# Can you write a simple list comprehension to convert these names to title case (brad pitt -> Brad Pitt). Or reverse the first and last name?

# Then use this same list and make a little generator, for example to randomly return a pair of names, try to make this work:

# pairs = gen_pairs()
# for _ in range(10):
#     next(pairs)

# Should print (values might change as random):

# Arnold teams up with Brad
# Alec teams up with Julian

# Have fun!

import itertools
import random

NAMES = ['arnold schwarzenegger', 'alec baldwin', 'bob belderbos',
         'julian sequeira', 'sandra bullock', 'keanu reeves',
         'julbob pybites', 'bob belderbos', 'julian sequeira',
         'al pacino', 'brad pitt', 'matt damon', 'brad pitt']

# list comprehensions
list1 = [name.title() for name in NAMES]

# reverse
def reverse_list(list1):
    first, last = list1.split()
    # ' '.join(last, first)
    return f"{last} {first}"

rev = [reverse_list(list1) for list1 in NAMES]

def gen_pairs():
    first_names = [list1.split()[0].title() for list1 in NAMES]
    while True:
        first, second = None, None
        while first == second:
            first, second = random.sample(first_names, 2)

        yield f'{first} teams up with {second}'


pairs = gen_pairs()
for _ in range(10):
    print(next(pairs))

# Another way
first_ten = itertools.islice(pairs, 10)

