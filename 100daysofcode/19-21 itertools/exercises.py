import itertools
import sys
import time 

symbols = itertools.cycle('-\|/')

while True:
    sys.stdout.write('\r' + next(symbols))
    sys.stdout.flush()
    time.sleep(0.5)
    
    
for i in product('andrei', repeat=2):
    print(i)

    
    
friends = 'mike bob julian'.split()
# note that we get a generator so using list to consume it
print(list(combinations(friends, 2)))

# what if order matters?
print(list(permutations(friends, 2)))


# Traffic lights


colours = 'red yellow green'.split()
rotation = itertools.cycle(colours)

def timer():
    return random.randint(3, 7)

def light_rotation(rotation):
    for colour in rotation:
        if colour == 'yellow':
            print('Caution! The light is %s' % colour)
            sleep(3)
        elif colour == 'red':
            print('STOP! The light is %s' % colour)
            sleep(timer())
        else:
            print('Go! The light is %s' % colour)
            sleep(timer())
        
if __name__ == '__main__':
    light_rotation(rotation)
