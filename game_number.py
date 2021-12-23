import random


print('________________________________________')
print('       GUESS THAT NUMBER GAME')
print('________________________________________')
print()

the_number = random.randint(0, 100)
guess = -1

name = input('Player what is your name? ')

while guess != the_number:
    guess_text = input('Guess a number between 0 and 100: ')
    guess = int(guess_text)
    if guess < the_number:
        #print('Your guess of' + guess + 'too LOW')
        print('Sorry {1}, your guess of {0} was too LOW.'.format(guess, name))
    elif guess > the_number:
        print('Sorry {1}, your guess of {0} was too HIGH.'.format(guess, name))
    else:
        print('Excellent work {1}, you won, it was {0}!'.format(guess, name))
print('done')




