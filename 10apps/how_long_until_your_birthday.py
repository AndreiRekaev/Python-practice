import datetime


def print_header():
    print('___________________________________')
    print('          BIRTHDAY APP')
    print('___________________________________')
    print()


def get_birthday_from_user():
    print('When were you born? ')
    year = int(input("YEAR [YYYY]: "))
    month = int(input("MONTH [MM]: "))
    day = int(input("DAY [DD]: "))

    birthday = datetime.date(year, month, day)
    return birthday


def compute_days_between_dates(original_date, target_date):
    this_year = datetime.date(target_date.year, original_date.month, original_date.day)
    dt = this_year - target_date
    return dt.days


def print_birthday_information(days):
    if days < 0:
        print('You had your birthday {} days ago this year.'.format(-days))
    elif days > 0:
        print('Your birthday is in {} days!'.format(days))
    else:
        print('Happy birthday!!!')


def main():
    print_header()
    bday = get_birthday_from_user()
    now = datetime.date.today()
    number_of_days = compute_days_between_dates(bday, now)
    print(number_of_days)
    print_birthday_information(number_of_days)


main()
