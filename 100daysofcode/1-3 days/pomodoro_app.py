# Pomodoro?
# What's a Pomodoro Timer? We're glad you asked! (If you didn't ask, you can read anyway!)

# A Pomodoro Timer is a countdown timer that enables you to focus on a given task. You set the timer for a specific duration, 20 minutes for example, and for that duration you are completely offline and focused. No email, no phone, no texts, no kids (a man can dream!)... no interruptions. Just pure, focus. This is the Pomodoro Technique.

# At the end of the timer, you're back online.

# The idea is that the minutes of focus time allow you to achieve more than you otherwise would given the usual swathe of interruptions we all suffer.

# The real fanatics will do a set period of the Pomodoro Technique followed by a short break, then another Pomodoro set and repeat.

import datetime
import time


def header():
    print('------------------------')
    print('    POMODORO TIMER')
    print('------------------------')

def user_choice():
    choice = input("Choose your timeout: "
                   "[1] Pomodoro 25 min; "
                   "[2] Short break 5 min; "
                   "[3] Long break 10 min; "
                   "[4] Exit: ")
    if choice == '1':
        pomodoro()
    elif choice == '2':
        short_break()
    elif choice == '3':
        long_break()
    elif choice == '4':
        print('good luck!')
        quit()
    else:
        print('Please, try again!')


def pomodoro():
    timer = datetime.timedelta(minutes=25)
    while timer:
        print(f'Pomodoro timer {str(timer)}')
        time.sleep(1)
        timer -= datetime.timedelta(seconds=1)
    print('Time is up!')

def short_break():
    timer = datetime.timedelta(minutes=5)
    while timer:
        print(f'Short break timer {str(timer)}')
        time.sleep(1)
        timer -= datetime.timedelta(seconds=1)
    print('Time is up!')

def long_break():
    timer = datetime.timedelta(minutes=10)
    while timer:
        print(f'Long break timer {str(timer)}')
        time.sleep(1)
        timer -= datetime.timedelta(seconds=1)
    print('Time is up!')



if __name__ == '__main__':
    header()
    user_choice()
