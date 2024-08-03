import argparse


def process_string(string: str) -> str:
    word: str = ''
    split_strings: list[str] = string.split()
    for i in split_strings:
        word += i[0]
    return word


def decypher() -> None:
    my_parser: any = argparse.ArgumentParser()
    my_parser.add_argument("init_string", help="add cyphered string")
    args: any = my_parser.parse_args()
    print(process_string(args.init_string))


def main():
    decypher()


if __name__ == "__main__":
    main()
