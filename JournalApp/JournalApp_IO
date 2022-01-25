import journal
import os

def print_header():
    print('___________________________________')
    print('          JOURNAL APP')
    print('___________________________________')

def run_event_loop():
    print('What do you want to do with your journal?')
    cmd = 'EMPTY'
    journal_name = 'default'
    journal_data = journal.load(journal_name)  # list()

    while cmd != 'x' and cmd:
        cmd = input('[L]ist entries, [A]dd an entry, E[x]it: ')
        cmd = cmd.lower().strip()

        if cmd == 'l':
            list_entries(journal_data)
        elif cmd == 'a':
            add_entry(journal_data)
        elif cmd != 'x' and cmd:
            print("Sorry, we don't understand '{}'.".format(cmd))
    print('Done, goodbye.')
    journal.save(journal_name, journal_data)

def list_entries(data):
    print('Your journal entries: ')
    entries = reversed(data)
    for idx, entry in enumerate(entries):
        print('* [{}] {}'.format(idx+1, entry))

def add_entry(data):
    text = input('Type your entry, <enter> to exit: ')
    journal.add_entry(text, data)
    #data.append(text)

print("__file__" + __file__)
print("__name__" + __name__)

if __name__ == '__main__':
    main()

print('1. About to import journal_main')
import journal_main

print('2. Journal_main imported')
print('3. Printing header!')

journal_main.print_header()
print('3. Done with journal_main')
'''
This is the journal module.
'''


def load(name):
    '''
    This method creates and loads a new journal.

    :param name: This base name of the journal to load.
    :return: A new journal data structure populated with the file data.
    '''
    data = []
    filename = get_full_pathname(name)

    if os.path.exists(filename):
        with open(filename) as fin:
            for entry in fin.readlines():
                data.append(entry.rstrip())


    return data

def save(name, journal_data):
    filename = get_full_pathname(name)
    print("...........saving to: {}".format(filename))


    with open(filename, 'w') as fout:
        for entry in journal_data:
            fout.write(entry + '\n')


def get_full_pathname(name):
    filename = os.path.abspath(os.path.join('.', 'journals', name + '.jrl'))
    return filename


def add_entry(text, journal_data):
    journal_data.append(text)

def main():
    print_header()
    run_event_loop()
